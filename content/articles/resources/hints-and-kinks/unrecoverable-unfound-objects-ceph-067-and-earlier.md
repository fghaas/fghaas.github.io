Title: Unrecoverable unfound objects in Ceph 0.67 and earlier
Slug: unrecoverable-unfound-objects-ceph-067-and-earlier
Date: 2014-01-28 18:52:02 +0100
Tags: Ceph

As [Ceph](http://ceph.com/) author [Sage
Weil](https://twitter.com/Liewegas) points out frequently, distributed
storage solutions for all their goodness [have a "dirty little
secret"](http://youtu.be/JfRqpdgoiRQ?t=36m20s): No matter just how
redundant and reliable they are by design, a bug in the storage
software itself can be a real issue.

And occasionally, the bug doesn't have to be in the storage software
itself.

Every self-respecting Linux file system supports [extended file
attributes
("xattrs")](http://en.wikipedia.org/wiki/Extended_file_attributes),
and XFS (commonly used with Ceph OSDs) is no exception. When OSDs
store RADOS objects in the OSD filestore, they make heavy use of
key-value pairs. To do so, they can employ two approaches:

- storing key-value pairs in filesystem xattrs directly (inline
  xattrs);
- storing them in a separate key-value store known as an object map or
  omap (based on [Google LevelDB](https://github.com/google/leveldb).

RADOS generally expects that the maximum xattr size on a file is
practically unlimited, so if your filestore is on a filesystem where
that is *not* the case (such as ext4), you would generally use omaps.

Enabling the use of omaps is easy enough. This goes in your ceph.conf:

```ini
[osd]
filestore xattr use omap = true
```

Ceph releases since 0.66 will
[enable this automatically](https://github.com/ceph/ceph/commit/6d90dad45e089447562e9a01fd9ca0f7a2aaf2b1)
if the filestore is determined to be running on ext4. But for the XFS
and BTRFS filesystem, the general recommendation (and default
behavior) remained to just use inline xattrs. This is also true for
the stable Ceph "Dumpling" release (0.67).

Since Ceph 0.70, the configuration option
[has been dropped](https://github.com/ceph/ceph/commit/dc0dfb9e01d593afdd430ca776cf4da2c2240a20)
and Ceph since always behaves as if `filestore xattr use omap` was set
to `true`. Now there is a reason for that, and it is a bit trickier
than you might expect.

When manipulating extended attributes, applications (including
ceph-osd) make use of the
[`getxattr()`, `setxattr()`, and `listxattr()` syscalls](http://man7.org/linux/man-pages/man2/fgetxattr.2.html). Expectedly,
these syscalls retrieve, set, and enumerate extended attributes set on
a file.

Now it is actually possible to set so many keys, or so large values,
that while `getxattr()` and `setxattr()` executed on a specific file
continue to work just fine, `listxattr()` returns with `-E2BIG`. Now
it turns out that

- radosgw can actually set attribute lists that large, and

- ceph-osd will fail if it cannot determine the file attributes for a
  file under its control.

When this happens, the object shows as `unfound` in `ceph health
detail`, and sadly, the documented operation to recover unfound
objects fails. The affected Placement Group (PG) also remains stuck,
again being reported as such in ceph health detail.

If you actually have run into this problem, you should really call
Inktank for support. (You can also give us a call, of course, and
we'll be happy to help you confirm the problem. But we will refer you
to Inktank for the actual fix -- we don't fiddle and mess around with
RADOS object internals, and neither should you.)

## How to avoid this in the first place?

If you're on Ceph 0.70 or later, congratulations. You should be safe,
as omaps are enabled and anything that would overflow your xattrs
instead gets stored in an omap.

If you're on any earlier version, including the currently
stable 0.67.x "Dumpling" series, enable filestore xattr use omap. Do
it now, regardless of what filesystem your OSDs run on. Then restart
your OSDs one by one; your existing xattrs won't get lost.

* * *

This article originally appeared on the `hastexo.com` website (now defunct).
