Title: Finding out which OSDs currently store a specific RADOS object
Date: 2012-03-09 22:55:06 +0100
Slug: which-osd-stores-specific-rados-object
Tags: Ceph

Ever wanted to know just which of your OSDs a RADOS object is
currently stored in? Here's how.

Suppose you've got an RBD device, named `test`. Then you can use the
`rbd info` command to display which name prefix is used by the RADOS
objects that make up the RBD:

```
ceph04:~ # rbd info test
rbd image 'test':
    size 1024 MB in 256 objects
    order 22 (4096 KB objects)
    block_name_prefix: rb.0.0
    parent:  (pool -1)
```

In this example, the prefix we're looking for is `rb.0.0`.

What's the RBD currently made of?

```
ceph04:~ # rados -p rbd ls | grep "^rb.0.0."
rb.0.0.000000000000
rb.0.0.000000000020
rb.0.0.000000000021
rb.0.0.000000000040
rb.0.0.000000000042
rb.0.0.000000000060
rb.0.0.000000000063
rb.0.0.000000000080
rb.0.0.000000000081
rb.0.0.000000000082
rb.0.0.000000000083
rb.0.0.000000000084
rb.0.0.000000000085
rb.0.0.000000000086
rb.0.0.000000000087
rb.0.0.000000000088
rb.0.0.0000000000a0
rb.0.0.0000000000a5
rb.0.0.0000000000c0
rb.0.0.0000000000c6
rb.0.0.0000000000e0
rb.0.0.0000000000e7
rb.0.0.0000000000ff
```

Now suppose you're interested in where `rb.0.0.0000000000a5` is.

You first grab an OSD map:

```
ceph04:~ # ceph osd getmap -o /tmp/osdmap
2012-03-09 21:31:47.055376 mon <- [osd,getmap]
2012-03-09 21:31:47.056624 mon.1 -> 'got osdmap epoch 187' (0)
wrote 2273 byte payload to /tmp/osdmap
```

And now you can use `osdmaptool` to test an object name against the
mapfile:

```
ceph04:~ # osdmaptool --test-map-object rb.0.0.0000000000a5 /tmp/osdmap 
osdmaptool: osdmap file '/tmp/osdmap'
 object 'rb.0.0.0000000000a5' -> 0.7ea1 -> [2,0]
```

... meaning the object lives in Placement Group `0.7ea1`, of which
replicas currently exist in OSDs 2 and 0.

Why do you want to know this? Normally, really, you don't. All the
replication and distribution happens under the covers without your
intervention. But you can use this rather neatly if you want to watch
your data being redistributed as you take out OSDs temporarily, and
put them back in.

* * *

This article originally appeared on the `hastexo.com` website (now defunct).
