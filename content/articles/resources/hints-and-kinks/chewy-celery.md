Title: Celery to Chew On
Date: 2020-05-06
Slug: chewy-celery
Tags: Django, MySQL, HAProxy, Celery, Python
Summary: Asynchronous Celery tasks that manipulate a MySQL/Galera database from a Django application can produce very interesting behavior when HAProxy is involved.

Asynchronous Celery tasks that manipulate a MySQL/Galera database from
a Django application can produce very interesting behavior when
HAProxy is involved.

<!--break-->

# Some basics

When you’re running a [Django](https://www.djangoproject.com/)
application, the following things are all pretty commonplace:

* You use [MySQL](https://en.wikipedia.org/wiki/MySQL) or
  [MariaDB](https://en.wikipedia.org/wiki/MariaDB) as your [Django
  database
  backend](https://docs.djangoproject.com/en/3.0/ref/databases/#mariadb-notes).
* You don’t run a single standalone MySQL/MariaDB instance, but a
  [Galera](https://galeracluster.com/) cluster.
* You run asynchronous tasks in [Celery](https://docs.celeryproject.org/en/stable/).

This way, if you have a complex operation in your application, you
don’t necessarily have to handle it in your latency-critical request
codepath. Instead, you can have something like this:

```python
from celery import Task

class ComplexOperation(Task)
   """Task that does very complex things"""

   def run(self, **kwargs):
      # ... lots of interesting things
```

... and then from your view (or management command, or whatever), you
can invoke this like so:

```python
from .tasks import ComplexOperation

def some_path(request):
   """/some_path URL that receives a request for an asynchronous ComplexOperation"""
   # ...
   
   # Asynchronously process ComplexOperation
   ComplexOperation.delay(pk=request.GET['id'])

   # ...
```

What this means is that the code defined in `ComplexOperation`’s
`run()` method can run asynchronously, while the HTTP request to
`/some_path` can immediately return a response. You can then fetch the
asynchronous task’s result in a later request, and present it to the
user.

(Note that there are other ways to [invoke Celery
tasks](https://docs.celeryproject.org/en/stable/userguide/calling.html);
getting into those in detail is not the point of this article.)

# MySQL/Galera via HAProxy

Now, let’s inject another item into the setup. Suppose your
application doesn’t talk to your Galera cluster directly, but via
[HAProxy](https://www.haproxy.org/). That’s not exactly unheard of; in
fact it’s [an officially documented HA
option](https://galeracluster.com/library/documentation/ha-proxy.html)
for Galera.

If you run a Django application against an HAProxyfied Galera cluster,
and you have rather long-running Celery tasks, you may see occurrences
of `OperationalError` exceptions that map to MySQL error 2013, `Lost
connection to MySQL server during query`.

Error 2013 means that the connection between the client and the server
dropped in the middle of executing a query. This is different from
error 2006, `MySQL server has gone away`, which means that the server
has gracefully torn down the connection. 2013 is really an
out-of-nowhere connection drop, which normally only occurs if your
network has gone very wonky.

With HAProxy however, *that* service may be your culprit. An HAProxy
service sets four different **timeout** values:

* `timeout connect`: the time in which a backend server must accept a
  TCP connection, default 5s.
* `timeout check`: the time in which a backend server must respond to
  a recurring health check, default 5s.
* `timeout server`: how long the server is allowed to take before it
  answers a request, default 50s.
* `timeout client`: how long the client is allowed to take before it
  sends the next request, default 50s.

# Distilling the timeout problem

If you have access to `manage.py shell` for your Django application,
here’s a really easy way for you to trigger an adverse effect of this
default configuration. All you have to do is create an object from a
model, so that it fetches data from the database, then wait a bit,
then try to re-fetch. Like so:

```python-doctest
./manage.py shell
[...]
(InteractiveConsole)
>>> from time import sleep
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> me = User.objects.get(username='florian')
>>> sleep(40)
>>> me.refresh_from_db()
>>> sleep(55)
>>> me.refresh_from_db()
Traceback (most recent call last):
[...]
OperationalError: (2013, 'Lost connection to MySQL server during query')
```

So what happens here?

* I open a session to the database with the `User.objects.get()` call
  that populates the `me` object.
* Then I wait 40 seconds. That’s comfortably short of the 50-second
  HAproxy timeout.
* Now when I run `me.refresh_from_db()`, the session is still alive
  and the call completes without error. The timeout clock resets at
  this stage, and I could keep going like this ad infinitum, as long
  as I `sleep()` (or keep busy) for less than 50 seconds.
* However, I next wait *55* seconds, causing HAProxy to terminate the
  connection.
* And then, `refresh_from_db()` breaks immediately with the 2013
  error.

Note that if I run `refresh_from_db()` — or any other operation that
touches the database – **again**, I get a different error (2016,
expected at this point), but I don’t get my database connection back:

```python-doctest
>>> me.refresh_from_db()
Traceback (most recent call last):
[...]
OperationalError: (2006, 'MySQL server has gone away')
```

What I have to do instead is *close* my `connection` first:

```python-doctest
>>> from django.db import connection
>>> connection.close()
```

... and then, when I run anything else that requires a database query,
Django will happily reconnect for me.

```python-doctest
>>> me.refresh_from_db()
```

# HAProxy timeouts getting in the way of your Celery tasks

Now how does this relate to a real-world application? Suppose you have
a long-running Celery task with database updates or queries at the
beginning and end of something complicated, like so:

```python
from celery import Task
from model import Thing

class ComplexOperation(Task)
   """Task that does very complex things"""
   
   def run(self, **kwargs):
     thing = Thing.objects.get(pk=kwargs['pk'])
     do_something_really_long_and_complicated()
     thing.save()
```

In this case, 

* we retrieve data from the database into memory, populating our
  `thing` object,
* then we do something very complex with it — suppose this can
  take on the order of minutes, in the extreme,
* and finally, we take the modified data for our in-memory object, and
  persist it back to the database.

So far, so simple. However, now assume that while you’re executing the
`do_something_really_long_and_complicated()` method, something bad
happens to your database. Say you restarted one of your MySQL or
MariaDB processes, or one of your nodes died altogether. Your database
*cluster* is still alive, but your *session*, which was very much
alive during the call that populated `thing`, is dead by the time you
want to make the `thing.save()` call.

Depending on what actually happened, you’d see one of the following
two `OperationalError` instances:

* Either an immediate `2006, MySQL server has gone away` — this is is
  what you’d see if the MySQL server was shut down or
  restarted. That’s a graceful session teardown, and it’s **not** what
  I want to focus on in this article.

* Or, and this is what I want to discuss further here, `2013, Lost
  connection to MySQL server during query`. You normally *don’t* get
  this as a result of something breaking at the other *end* of the
  connection, but rather in between. In our case, that would be
  HAProxy. Let’s look at our code snippet with a few extra comments:

```python
from celery import Task
from model import Thing

class ComplexOperation(Task)
   """Task that does very complex things"""
   
   def run(self, **kwargs):
     thing = Thing.objects.get(pk=kwargs['pk'])
     # Right here (after the query is complete) is where HAproxy starts its
     # timeout clock

     # Suppose this takes 60 seconds (10 seconds longer than the default 
	 # HAProxy timeout)
	 
     do_something_really_long_and_complicated()

     # Then by the time we get here, HAProxy has torn down the connection,
     # and we get a 2013 error.
     thing.save()
```

So now that we’ve identified the problem, how do we solve it? Well
that depends greatly on the following questions:

* Are you the developer, meaning you can fix this in code, but you
  can’t change much in the infrastructure?
  
* Or are you a systems person, who can control all aspects of the
  infrastructure, but you don’t have leverage over the code?

If you have control over neither code nor infrastructure, you’re out
of luck. If you call all the shots about both, you get to pick and
choose. But here are your options.


# Fixing this in code

If it’s your codebase, and you want to make it robust so it runs in
any MySQL/Galera environment behind HAProxy, no matter its
configuration, you have a couple of ways to do it.


## Keep connections shorter

One way to do it is do keep your database connections alive for such a
short time that you practically never hit the HAProxy
timeouts. Thankfully, Django auto-reconnects to your database any time
it needs to do something, so the only thing you need to worry about
here is _closing_ connections — _reopening_ them is automatic. For
example:

```python
from django.db import connection
from model import Thing

class ComplexOperation(Task)
   """Task that does very complex things"""
   
   def run(self, **kwargs):
     thing = Thing.objects.get(pk=kwargs['pk'])
     # Close connection immediately
     connection.close()

     # Suppose this takes 60 seconds.
     do_something_really_long_and_complicated()

     # Here, we just get a new connection.
     thing.save()
```

## Catch OperationalErrors

The other option is to just wing it, and catch the errors. Here’s a
deliberately overtrivialized example:

```python
from django.db import connection
from django.db.utils import OperationalError
from model import Thing

class ComplexOperation(Task)
   """Task that does very complex things"""
   
   def run(self, **kwargs):
     thing = Thing.objects.get(pk=kwargs['pk'])
     # Right here (after the query is complete) is where HAproxy starts its
     # timeout clock

     # Suppose this takes 60 seconds.
     do_something_really_long_and_complicated()

     # Then by the time we get here, HAProxy has torn down the connection,
     # and we get a 2013 error, which we’ll want to catch.
     try:
       thing.save()
     except OperationalError:
       # It’s now necessary to disconnect (and reconnect automatically),
       # because if we don’t then all we do is turn a 2013 into a 2006.
       connection.close()
       thing.save()
```

Now of course, you’d never _actually_ implement it this way, because
the one-time retry is far too trivial, so you probably want to retry
up to _n_ times, but with exponential backoff or some such — in
detail, this becomes complicated really quickly. 

You probably also want some logging to catch this. 

In short, you probably don’t want to hand-craft this, but instead rely
on something like the `retry()` decorator from
[tenacity](https://tenacity.readthedocs.io/en/latest/), which can
conveniently provide all those things, plus the reconnect, without
cluttering your code too much.

# Fixing this in infrastructure

You may be unable to control this sort of thing in your code — because, for
example, it’s a codebase you’re not allowed to touch, or you’re less
than comfortable with the idea of scouring or profiling your code for
long-running codepaths between database queries, and sprinkling
`connection.close()` statements around.

In that case, you can fix your HAProxy configuration instead. Again,
the variables you’ll want to set are

* `timeout server` and 
* `timeout client`.

You’ll probably want to set them to an identical value, which should
be the maximum length of your database-manipulating Celery task, and
then ample room to spare.

The maximum reasonable value that you can set here is that of your
backend server’s `wait_timeout` configuration variable, [which
defaults to 8
hours](https://mariadb.com/kb/en/server-system-variables/#wait_timeout). 

Careful though, while MySQL interprets timeout settings in _seconds_
by default, HAProxy [defaults to
_milliseconds._](https://cbonte.github.io/haproxy-dconv/1.7/configuration.html#2.4)
You’d thus need to translate the `28800` default value for MySQL’s
`wait_timeout` into a `timeout server|client` value of 28000000 for
HAProxy, or else you set the HAProxy timeout to a value of `28800s`
(or `8h`, if you prefer).

* * * 

Background research contribution credit for this post goes to my [City
Network](https://www.citynetwork.eu/) colleagues [Elena
Lindqvist](https://twitter.com/elenalindq) and [Phillip
Dale](https://twitter.com/pdale_se), plus [Zane
Bitter](https://twitter.com/zerobanana) for the tenacity suggestion.

Also, thanks to [Murat Koç](https://twitter.com/muratkochane) for
suggesting to clarify the supported time formats in HAProxy.
