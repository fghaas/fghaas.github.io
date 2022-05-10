Title: Drizzle: the most influential software project you’ve (probably) never heard of
Date: 2022-05-10 17:15
Slug: drizzle
Summary: Drizzle aimed to rewrite the MySQL database server. It instead rewrote collaborative software development.
Tags: Development, CI, MySQL, OpenStack

**Drizzle** was an open-source project[^disclaimer] that, for all
intents and purposes, died in 2016. Its project web site is now
defunct, and the most recent snapshot from the Wayback Machine is
[that of September 2,
2016](https://web.archive.org/web/20160902091713/http://www.drizzle.org/).
In July of that year, Stewart Smith (one of the project’s core team)
[announced on the project mailing
list]((https://www.mail-archive.com/drizzle-discuss@lists.launchpad.net/msg09228.html).)
that neither he nor any other core team members had time to dedicate
to Drizzle anymore.


[^disclaimer]: Disclaimer: I was never a part of the Drizzle project
    in any role, which for the purposes of this article is probably a
    good thing as I am not talking about personal accomplishments or
    failures, in other words I have no skin in the game. This article
    also does not contain any information about the Drizzle project
    except that which was available via public channels at the time,
    or has become public since.

Prior to that, the project had been mostly dormant since 2012[^2013],
having been founded in 2008. So it was properly “active” for just 4
years, and then in limbo for 4 more before finally wrapping
up. Chances are, you’ve probably never run a Drizzle database server
in production, and quite possibly never spun one up for any purpose
either.

[^2013]: The project did participate in Google Summer of Code in 2013,
    which is what the [last tweets on the project’s Twitter
    account](https://twitter.com/drizzledb) are about. But the
    project’s development branch [had its last alpha release in
    September 2012](https://launchpad.net/drizzle/7.2).

And yet, if you’re an open source software developer, you’re probably
using something, every single day, that came out of Drizzle. And that
something isn’t even software.

## Drizzle’s history, a very brief summary

Drizzle started as an attempt to refactor MySQL, and was originally
driven by Brian Aker, together with a small team of engineers at Sun
(which had then-recently acquired MySQL), in the first half of 2008. A
skunk works project that flew under the radar — to put it charitably —
at Sun, Drizzle was publicly announced at O’Reilly OSCON of that year.
There are a couple of videos floating around from that event ([from
the keynotes](https://youtu.be/9DuJFUnxg7k), and [from a booth
presentation](https://youtu.be/2tO7_Ozr-9U)) that are both… well, go
and see for yourself. The aforementioned Stewart Smith did a very
entertaining talk at linux.conf.au some five years later that covers
those events, which you can watch from [the official Linux Australia
mirror](https://mirror.linux.org.au/pub/linux.conf.au/2014/Wednesday/28-Past_Present_and_future_of_MySQL_and_variants_-_Stewart_Smith.mp4),
or from a [YouTube
upload](https://www.youtube.com/watch?v=6Uv9vcb4SdA).

There’s also an interesting old blog post from MySQL co-founder Monty
Widenius, [written in late July of
2008](https://monty-says.blogspot.com/2008/07/what-if.html), which
outlines the state of affairs at the time.

Of course, in 2010 Oracle acquired Sun (and with it, the MySQL
database) — and Oracle was presumably less than keen on having an
*in-house* fork of the database technology it had just acquired. Thus,
the Drizzle engineers found a new home at Rackspace, with the goal of
getting Drizzle to a production-ready release. That *sort of*
happened, and the Drizzle package even got into Debian, but after [the
Drizzle 7.1 release in 2012](https://launchpad.net/drizzle/7.1),
adoption did not exactly skyrocket. Development on Drizzle stagnated
and eventually petered out.  The 7.2 release branch [never made it out
of the alpha stage](https://launchpad.net/drizzle/7.2).

Today, to the best of my knowledge, you can’t install a Drizzle
package on any contemporary operating system. There is [no official
Drizzle container image on Docker
Hub](https://hub.docker.com/search?q=drizzle), no DBaaS offering based
on Drizzle, nothing.

But Drizzle left a very important legacy.

## What did Drizzle do differently?

In 2008, it was already common for open source software to live in
public version-controlled repositories. But far from all of them used
[Git](https://git-scm.com/), like the vast majority do today: some
used [CVS](https://en.wikipedia.org/wiki/Concurrent_Versions_System)
or [Subversion](https://en.wikipedia.org/wiki/Apache_Subversion), some
used [Mercurial](https://en.wikipedia.org/wiki/Mercurial), and the
[Launchpad](https://launchpad.net/) platform (which Drizzle lived on)
used [Bazaar](https://en.wikipedia.org/wiki/GNU_Bazaar).

But most of them did have one thing in common, which is how changes
landed in the tree. You had a small group of “core committers”, who
had write access to the “official” code repository. They could (and
would) push changes to the codebase on their own volition and
authority. In smaller projects, the core committers “group” might be
just one person.  If someone *outside* the core committers group
wanted to make a contribution, they had to convince a core committer
to merge it.

Sometimes (though quite rarely at the time), projects had some form of
scripted unit testing — typically implemented with the then-popular
[Hudson](https://en.wikipedia.org/wiki/Hudson_(software)) server,
which was subsequently forked to become
[Jenkins](https://www.jenkins.io/).  But such unit tests would be seen
as merely advisory: breaking unit tests didn’t necessarily mean that a
patch couldn’t land, *specifically* if the patch originated with a
core committer. Unit tests would also not necessarily run
automatically when a patch was submitted, they might instead run only
if specifically kicked off by a core committer.

The Drizzle team, as Brian put it in a talk I recall attending (though
not exactly when and where), “took commit rights away from everybody.”
That meant that *nobody* could push changes directly to a central
repository, and *everything* had to flow through CI tests. The process
generally went like this:

* You submitted a patch to Drizzle, implementing a new feature.
  Immediately after your submission, an automated process (in Hudson,
  later Jenkins) would automatically run its complete suite of unit
  tests against the current code base, with your patch applied.

* Your patch would perhaps break an existing regression test. You
  would immediately be notified of the failure, giving you a chance to
  fix the problem that your change introduced.

* You submitted a new version of the patch, which would now pass the
  test suite.

* Humans would now review your patch. They would no longer have to
  worry that your patch broke anything pre-existing (a common question
  in patch reviews in many contemporary projects), and could instead
  focus on the merit of your feature addition.

* If your reviewers determined that your new feature should come with
  *additional* tests (and they usually should), they would recommend
  you implement a test for your new feature.

* You would then resubmit your patch with the added testing
  functionality, and — assuming everyone was happy with the
  implementation — your reviewers would give the go-ahead to merge
  your patch.

* At this stage of course, the rest of the codebase might have
  changed: some other patches might have landed before yours. So, the
  entire pipeline — including tests that predated your patch, the new
  tests your patch introduced, and the new tests that *other* patches
  might have added in the interim — would re-run with the current
  state of the codebase with your patch applied. If your patch broke
  things *now,* you would be asked to fix them once more.

* However, if your change *didn’t* break anything even now, then there
  would be no human blocking the merge anymore: as soon as the tests
  passed, *the thing that ran the tests* (I don’t recall if in 2008 we
  already had the term “CI pipeline” for that thing) would merge the
  patch on your behalf.

Much of this automation was brand new innovation at the time, largely
due to the work of Drizzle developer Monty Taylor — who later went on
to becoming a highly influential engineer in other projects, which
(among many other things) [landed him a profile in WIRED in
2013](https://www.wired.com/2013/04/new-hackers-taylor/).

The Drizzle team also was pretty diligent about what they considered
“breaking things:” for example, the Drizzle test suite contained
several performance benchmarks. If a patch made the server perform
worse, i.e. introduced a performance regression, that would be treated
the same as a functional regression. So you not only would be unable
to land a patch that actually broke functionality or made the database
server eat data; you would also be unable to land a patch that made
the server slower.

The Drizzle team is also where, to the best of my knowledge, a coinage
for this kind of approach originated: “gated commits”, or “gating” in
general.

## How is this relevant?

A substantial fraction on the Drizzle core team — which had moved to
Rackspace in 2010 — was instrumental in launching another project that
came out of that company (and NASA) that same year:
[OpenStack](https://openstack.org). And OpenStack took the gating
approach from its humble beginnings with Drizzle to an absolutely
massive scale in its hype years (2011 – 2015 or thereabouts) — so much
so that it established a new default in collaborative software
projects.  Many other projects that launched in that timeframe
(including [Kubernetes](https://kubernetes.io) and
[Terraform](https://www.terraform.io)) adopted this approach as well.

Today, having automated CI testing on every submitted patch is
considered par for the course in a collaborative software project.
[GitLab CI](https://docs.gitlab.com/ee/ci/) and [GitHub Actions
workflows](https://docs.github.com/en/actions/automating-builds-and-tests/about-continuous-integration)
have made these much more accessible than they used to be with Hudson
and Jenkins. It’s also exceedingly common to do detailed collaborative
reviews in a public forum before merging — GitHub’s PR review workflow
is ever more closely approaching the Gerrit review workflow that
OpenStack uses. GitHub’s [auto-merge
functionality](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request)
(which lands patches automatically once they have passed both
automated unit tests and human review) is more or less a direct copy
of the automated merge found in OpenStack’s [development
workflow](https://docs.opendev.org/opendev/infra-manual/latest/developers.html#development-workflow),
which itself can be directly traced back to Drizzle’s review process.

And all these things are found in open source software projects across
all sorts of communities. Kubernetes, Terraform,
[Django](https://www.djangoproject.com/),
[CPython](https://github.com/python/cpython), [Open
edX](https://openedx.org) — you name it, it probably uses an approach
first pioneered in Drizzle.

And that’s the real lasting legacy of a project that few people even
remember by name.

## Who do we owe this to?

I know some of the Drizzle developers personally, though certainly not
all. What follows is an incomplete list of people you can buy a meal
or a drink if you run into them, and you like the way you
collaboratively develop software today:

* Brian Aker
* Mark Atwood
* Aeva Black
* Patrick Crews
* Eric Day
* Patrick Galbraith
* Andrew Hutchings
* Jay Pipes
* David Shrewsbury
* Stewart Smith
* Pádraig O’Sullivan
* Monty Taylor

* * *

### Acknowledgements

Stewart Smith and Mark Atwood kindly [reviewed this
article](https://github.com/fghaas/fghaas.github.io/pull/7) and
provided valuable feedback on it. Thanks to both of you! All errors
and omissions are of course mine, and mine alone.
