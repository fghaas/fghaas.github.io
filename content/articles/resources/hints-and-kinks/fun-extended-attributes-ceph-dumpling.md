Title: Fun with extended attributes in Ceph Dumpling
Date: 2014-02-24 16:50:17 +0100
Slug: fun-extended-attributes-ceph-dumpling
Tags: Ceph

This is a rather nasty bug in Ceph OSD, affecting 0.67 "Dumpling" and
earlier releases. It is fixed in versions later than 0.70, and a
simple workaround is available, but when it hits, this issue can be
pretty painful.

**Please read this post to the end.** This is by no means a punch
being thrown at Ceph, in fact it rather clearly illustrates a very
sane choice that the Ceph developers have made. If you run Ceph
Emperor or later, you are not affected by this issue, but it will be
an interesting read in data integrity in distributed systems anyway.

## Too much of a good thing: large extended attributes

Here is how to reproduce the problem in a very simple bit of Python
code, against Ceph Dumpling.

**Do not run this on a production system. Don't. Ever.**

```python
#!/usr/bin/python

# import rados
with rados.Rados(conffile='/etc/ceph/ceph.conf') as cluster:
    with cluster.open_ioctx('test') as ioctx:
        o = rados.Object(ioctx, 'onebyte')
        # Write one byte as the object content
        o.write('a')
        print('Wrote object')
        # Write an attribute of 8M
        o.set_xattr('val', 'a' * 8 * 1024**2)
        print('Set large attribute')
        # Retrieving an attribute by name should succeed
        a = o.get_xattr('val')
        print('Retrieved large attribute')
        # Walking the attribute list should fail
        try:
            alist = [ i for i in o.get_xattrs() ]
            print('Retrieved whole attribute list')
        except rados.Error:
            print('Failed to retrieve attribute list. '
                  'Congratulations, you probably just '
                  'corrupted one of your PGs.')
        raise
```
		
Removing the disabling comment character is left as an exercise for
the daring reader, just in case your cut & paste trigger finger is
itchy. **Do not run this against a production system.**

So what are we doing here? We're creating a single RADOS object named
`onebyte` in a pool called `test`. It is, as the name implies, only
one byte long (it contains just the letter a), but it has a very long
attribute named `val`, which is 8 Megabytes' worth of `a`'s.

(In case you're wondering: yes, there are applications that set very
large attributes on RADOS objects. radosgw is one of them.)

Since you've been able to set the attribute, you can also retrieve it,
which is why the call to `get_xattr('val')` succeeds just fine. But if
you fetch the entire attribute *list* (with `get_xattrs`), then you
run into an `E2BIG` error.

You can confirm that on the Linux command line, using the `rados`
utility, just the same. First, getting the object and getting an xattr
by name:

```
$ sudo rados -p test get onebyte -
a

$ sudo rados -p test getxattr onebyte val - 2>&1  | head -c 50
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Obviously, you're welcome to omit the head redirection if you prefer
to flood your screen. But for proving we can still retrieve the
attribute value, 50 characters is quite sufficient.

Let's try *listing* the attributes, though:

```
$ sudo rados -p test listxattr onebyte 
error getting xattr set test/onebyte: Argument list too long
```

Oops. `Argument list too long` is bash's way of translating the
`E2BIG` error for you, because that's what it usually means. In this
case, though, it's actually what we get from the rados utility, and
that gets it from the OSD it's talking to, and that gets it from the
filesystem.

## Digging deeper

Now let's take a look where this object is stored.

```
$ sudo ceph osd map test onebyte
$ osdmap e191 pool 'test' (3) object 'onebyte' -> pg 3.ed47d009 (3.1) -> up [0,2] acting [0,2]
So it's PG 3.1, currently mapped to OSDs 0 (primary) and 2 (replica). We happen to be on the very host where OSD 0 is running, so let's take a closer look:

$ sudo getfattr -d /var/lib/ceph/osd/ceph-0/current/3.1_head/onebyte__head_ED47D009__3 
/var/lib/ceph/osd/ceph-0/current/3.1_head/onebyte__head_ED47D009__3: Argument list too long
```

Same thing, E2BIG. Sure, if we can't enumerate the attributes
ourselves, the OSD can't either. But it's still fairly benign, because
we can still retrieve the object, right?

## Adding daemon failure

Well, not so much. Let's see what happens if one of our OSDs gets
restarted. This is a perfectly benign operation that Ceph is expected
to (and does) handle very gracefully.

```
$ sudo restart ceph-osd id=0
ceph-osd (ceph/0) start/running, process 7922
$ sudo rados -p test get onebyte -
a
```

The object is still there. What if, incidentally, the other OSD also
happens to go down some time later, and stays down?

```
$ sudo stop ceph-osd id=2
ceph-osd (ceph/2) stop/waiting
$ sudo ceph osd out 2
marked out osd.2.
```

Remember, *"at scale, something always fails"*. Ceph is built for
exactly that, and its algorithms deal with this type of failure in
stride. So at this point, we would expect Ceph to remap the PGs that
were previously on OSD 2 to OSD 1, and synchronize with OSD 0. And a
few minutes later, all hell breaks loose:

```
sudo ceph -s
  cluster bd70ea39-58fc-4117-ade1-03a4d429cb49
   health HEALTH_WARN 200 pgs degraded; 1 pgs recovering; 200 pgs stuck unclean; recovery 2/2 degraded (100.000%); 1/1 unfound (100.000%)
   monmap e4: 3 mons at {ubuntu-ceph1=192.168.122.201:6789/0,ubuntu-ceph2=192.168.122.202:6789/0,ubuntu-ceph3=192.168.122.203:6789/0}, election epoch 180, quorum 0,1,2 ubuntu-ceph1,ubuntu-ceph2,ubuntu-ceph3
   osdmap e237: 3 osds: 1 up, 1 in
    pgmap v1335: 200 pgs: 1 active+recovering+degraded, 199 active+degraded; 1 bytes data, 38684 KB used, 5071 MB / 5108 MB avail; 2/2 degraded (100.000%); 1/1 unfound (100.000%)
   mdsmap e1: 0/0/1 up
```

## Fighting a fire

Wow. We shut down only one OSD (OSD 2), the other one (OSD 0) was
merely restarted, but it has crashed in the interim. Its mon osd down
out interval has also expired, so it has been marked out as well. All
of our PGs are stuck degraded, one has an unfound object (that's the
one whose xattrs can no longer be enumerated). Yikes.

We scramble to bring our just-shutdown OSD back in.

```
$ sudo start ceph-osd id=2
ceph-osd (ceph/2) start/running, process 7426
$ sudo ceph osd in 2
marked in osd.2.
```

Does this make things better?

```
$ sudo ceph -w
 cluster bd70ea39-58fc-4117-ade1-03a4d429cb49
 health HEALTH_WARN 200 pgs degraded; 1 pgs recovering; 200 pgs stuck unclean; recovery 2/2 degraded (100.000%)
 monmap e4: 3 mons at {ubuntu-ceph1=192.168.122.201:6789/0,ubuntu-ceph2=192.168.122.202:6789/0,ubuntu-ceph3=192.168.122.203:6789/0}, election epoch 180, quorum 0,1,2 ubuntu-ceph1,ubuntu-ceph2,ubuntu-ceph3
 osdmap e243: 3 osds: 2 up, 2 in
  pgmap v1343: 200 pgs: 1 active+recovering+degraded, 199 active+degraded; 1 bytes data, 38812 KB used, 5071 MB / 5108 MB avail; 2/2 degraded (100.000%)
 mdsmap e1: 0/0/1 up

2014-02-11 19:09:56.868771 mon.0 [INF] osdmap e242: 3 osds: 2 up, 2 in
2014-02-11 19:09:56.895559 mon.0 [INF] pgmap v1342: 200 pgs: 1 active+recovering+degraded, 199 active+degraded; 1 bytes data, 38812 KB used, 5071 MB / 5108 MB avail; 2/2 degraded (100.000%)
2014-02-11 19:09:57.901188 mon.0 [INF] osdmap e243: 3 osds: 2 up, 2 in
2014-02-11 19:09:57.918612 mon.0 [INF] pgmap v1343: 200 pgs: 1 active+recovering+degraded, 199 active+degraded; 1 bytes data, 38812 KB used, 5071 MB / 5108 MB avail; 2/2 degraded (100.000%)
2014-02-11 19:09:59.920149 mon.0 [INF] osdmap e244: 3 osds: 1 up, 2 in
2014-02-11 19:09:59.931825 mon.0 [INF] pgmap v1344: 200 pgs: 1 active+recovering+degraded, 199 active+degraded; 1 bytes data, 38812 KB used, 5071 MB / 5108 MB avail; 2/2 degraded (100.000%)
2014-02-11 19:10:00.940319 mon.0 [INF] osd.2 192.168.122.203:6800/8362 boot
2014-02-11 19:10:00.940987 mon.0 [INF] osdmap e245: 3 osds: 2 up, 2 in
2014-02-11 19:10:00.954275 mon.0 [INF] pgmap v1345: 200 pgs: 1 active+recovering+degraded, 199 active+degraded; 1 bytes data, 38812 KB used, 5071 MB / 5108 MB avail; 2/2 degraded (100.000%)
2014-02-11 19:10:01.960942 mon.0 [INF] osdmap e246: 3 osds: 2 up, 2 in
2014-02-11 19:10:01.975509 mon.0 [INF] pgmap v1346: 200 pgs: 1 active+recovering+degraded, 199 active+degraded; 1 bytes data, 38812 KB used, 5071 MB / 5108 MB avail; 2/2 degraded (100.000%)
2014-02-11 19:10:03.982202 mon.0 [INF] osdmap e247: 3 osds: 1 up, 2 in
2014-02-11 19:10:03.994963 mon.0 [INF] pgmap v1347: 200 pgs: 1 active+recovering+degraded, 199 active+degraded; 1 bytes data, 38812 KB used, 5071 MB / 5108 MB avail; 2/2 degraded (100.000%)
2014-02-11 19:10:05.005162 mon.0 [INF] osd.2 192.168.122.203:6800/8483 boot
2014-02-11 19:10:05.005386 mon.0 [INF] osdmap e248: 3 osds: 2 up, 2 in
```

Hardly. OSDs flapping right and left. Ouch ouch ouch.

## Desperation: not your friend

OK, let's try to do something really terrible and get rid of that file manually.

```
$ sudo ceph osd map test onebyte
osdmap e254 pool 'test' (3) object 'onebyte' -> pg 3.ed47d009 (3.1) -> up [1] acting [1]
```

So it's mapped to OSD 1 now, which is expected. Let's take a look and see if we can find and remove it.

```
ceph@ubuntu-ceph2:~$ ls /var/lib/ceph/osd/ceph-1/current/3.1_head/
ceph@ubuntu-ceph2:~$
```

An empty directory. Well of course, they could never actually peer, so
the data never got synchronized. So there's pretty much one thing
left.

```
ceph@ubuntu-ceph3:~$ sudo stop ceph-osd id=2
stop: Unknown instance: ceph/2
ceph@ubuntu-ceph3:~$ sudo rm /var/lib/ceph/osd/ceph-2/current/3.1_head/onebyte__head_ED47D009__3
ceph@ubuntu-ceph3:~$ sudo start ceph-osd id=2
ceph-osd (ceph/2) start/running, process 9069

ceph@ubuntu-ceph1:~$ sudo stop ceph-osd id=0
stop: Unknown instance: ceph/0
ceph@ubuntu-ceph1:~$ sudo rm /var/lib/ceph/osd/ceph-0/current/3.1_head/onebyte__head_ED47D009__3 
ceph@ubuntu-ceph1:~$ sudo start ceph-osd id=0
ceph-osd (ceph/0) start/running, process 9485
```

There. Shut down the OSDs, nuked the files, brought the OSDs back up.

## A Fire Contained

And after a few more seconds, finally:

```
$ sudo ceph -s
  cluster bd70ea39-58fc-4117-ade1-03a4d429cb49
   health HEALTH_OK
   monmap e4: 3 mons at {ubuntu-ceph1=192.168.122.201:6789/0,ubuntu-ceph2=192.168.122.202:6789/0,ubuntu-ceph3=192.168.122.203:6789/0}, election epoch 180, quorum 0,1,2 ubuntu-ceph1,ubuntu-ceph2,ubuntu-ceph3
   osdmap e259: 3 osds: 3 up, 3 in
    pgmap v1367: 200 pgs: 200 active+clean; 1 bytes data, 122 MB used, 15204 MB / 15326 MB avail
   mdsmap e1: 0/0/1 up
```
   
Whew.

```
$ sudo rados -p test get onebyte -
error getting test/onebyte: No such file or directory
```

Now obviously the offending object is gone, which is ugly and we could
have manually recreated that file and set some magic user.ceph
attributes enabling us to keep the object, but in this case we just
didn't care and wanted our cluster back up and running as soon as
possible.

## Prevention

So we have a brutal cure for this problem that is roughly akin to
performing brain surgery with a fork and spoon. What could we have
done better?

LevelDB to the rescue. Ceph optionally (and in later versions, by
default) stores attributes that would overflow the filesystem xattr
store in a separate database called an omap, using Google's embedded
LevelDB database. And in Dumpling, this feature is disabled by default
-- with an exception for ext3/4, which have interesting attribute
limitations themselves.

This is the all-important option that needs to go in your ceph.conf:

```ini
filestore xattr use omap = true
```

You can enable this on a running cluster and this will retain and
preserve any xattrs previously set on RADOS objects. Attributes mapped
to file xattrs will simply be moved to the omap database (note however
that the opposite is not true, but you'll never want to disable this
option anymore, anyway).

As of
[this Ceph commit](https://github.com/ceph/ceph/commit/dc0dfb9e01d593afdd430ca776cf4da2c2240a20)
(which went into Ceph 0.70), the option is no longer available and is
always treated as if set to true, so those versions are not affected
by the issue described in this post.

* * *

This article originally appeared on the `hastexo.com` website (now defunct).
