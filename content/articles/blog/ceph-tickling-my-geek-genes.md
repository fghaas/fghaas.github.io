Title: Ceph: tickling my geek genes
Date: 2012-03-08 20:12
Slug: ceph-tickling-my-geek-genes
Author: florian
Tags: Ceph

Haven't heard of [Ceph](http://ceph.com/), the open-source distributed
petascale storage stack? Well, you've really been missing out. It's not
just a filesystem. It's a filesystem, and a striped/replicated block
device provider, and a virtualization storage backend, and a cloud
object store, and then some.

Most of you will, by now, probably have heard of the Ceph filesystem, a
distributed, replicated, extremely scaleable filesystem that [went
upstream with the 2.6.34 kernel
release.](http://kernelnewbies.org/Linux_2_6_34#head-87b23f85b5bdd35c0ab58c1ebfdcbd48d1658eef) But
that filesystem is really just a client to something that happens server
side, which is much more than just file storage.

[RADOS](http://ceph.com/category/rados/), the reliable autonomic
distributed object store is a massively distributed, replicating,
rack-aware object store. It organizes storage in objects, where each
object has an identifier, a payload, and a number of attributes.

Objects are allocated to a Placement Group (PG), and each PG maps to one
or several Object Storage Devices or OSDs. OSDs are managed by a
userspace daemon – everything server-side in Ceph is in userspace,
really – and locally map to a simple directory. For local storage,
objects simply map to flat files, so OSDs don't need to muck around with
local block storage. And they can take advantage of lots of useful
features built into advanced filesystems, like extended attributes,
clones/reflinks, copy-on-write (with btrfs). Extra points for the effort
to *not* reinvent wheels.

The entire object store uses a deterministic placement algorithm, CRUSH
(Controlled Replication Under Scaleable Hashing). There's never a
central instance to ask on every access, instead, everything can work
out where objects are. That means the store scales out seamlessly, and
can expand and contract on the admin's whim.

And based on that basic architecture, there's a number of entry points
and deployment scenarios for the stack:

-   **radosgw** provides a RESTful API for dynamic cloud storage. And it
    includes an S3 and Swift frontend to act as object storage for
    AWS/Eucalyptus and OpenStack clouds, respectively.

-   **Qemu-RBD** is a storage driver for the Qemu/KVM hypervisor (fully
    integrated with libvirt) that allows the hypervisor to access
    replicated block devices that are also striped across the object
    store – with a configurable number of replicas, of course.

-   **RBD** is a Linux block device that, again, is striped and
    replicated over the object store.

-   **librados** (C) and **libradospp** (C++) are APIs to access the
    object store programmatically, and come with a number of scripting
    language bindings. As you've probably guessed, Qemu-RBD builds on
    librados.

-   **Ceph** (the filesystem) exposes POSIX filesystem semantics built
    on top of RADOS, where all POSIX-related metadata is again stored in
    the object store. This is a remarkably thin client layer at just
    17,000 LOC (compare to GFS2 at 26,000 and OCFS2 at 68,000).

In short: it's cool stuff. And it's 100% open source, it's all under the
LGPL 2.1, and the developers have made a point of not creating any
closed-source "enterprise" features – in short, they're not shipping
"open core".[^crippleware]

[^crippleware]: The original version used the term *crippleware* here,
  which I now consider highly inappropriate. (The term *open core*, to
  the best of my recollection, wasn't particularly current in 2012.) I
  would like to apologize for my use of the previous term. The article
  contains no other edits in comparison to the 2012 original.

We've recently started contributing to the Ceph project to improve its
high-availability cluster integration: we've submitted Pacemaker
agents [to monitor the Ceph daemons
proper](https://github.com/ceph/ceph/commit/92cfad42030889d52911814faa717bebbd4dd22f)
(a pretty trivial wrapper for a script that ships with Ceph, for now).
And we've also contributed [a resource agent to manage an RBD device
as a Pacemaker
resource](https://github.com/ceph/ceph/commit/c31b86963ab3c51b5c6d17f6e3222fe164ef3ee9).
The latter gives Pacemaker users the ability to use RBD devices as a
drop-in replacement for iSCSI devices, MD devices under Pacemaker
control, or DRBD. The Ceph community
has been exceptionally welcoming and has made contributing a
pleasure – there's no copyright assignment nonsense, no CLAs, just a
very positive attitude toward outside contributions.

And in case you want to use a Ceph filesystem as a generally available
file system in your Pacemaker cluster (as you would with NFS, GlusterFS,
GFS2, or OCFS2), you can [do that now,
too](https://github.com/ClusterLabs/resource-agents/commit/f93668b4b60682363a686a293810e34ad4088a47).
However, please be cautioned that that should be considered an
experimental feature: the Ceph devs have made it very clear on numerous
occasions that they're currently focusing on making RADOS and RBD rock
solid, and then they'll tackle the POSIX filesystem layer to get it out
of experimental mode.

* * *

This article originally appeared on my blog on the `hastexo.com` website (now defunct).
