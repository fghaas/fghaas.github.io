Title: Solid-state drives and Ceph OSD journals
Date: 2013-01-13 20:33:58 +0100
Slug: solid-state-drives-and-ceph-osd-journals
Tags: Ceph, Performance
Summary: Considerations for running Ceph OSD journals on SSDs.

Object Storage Daemons
([OSDs](http://ceph.com/docs/master/man/8/ceph-osd/)) are the Ceph
stack's workhorses for data storage. They're significantly smarter
than many of their counterparts in distributed block-storage solutions
(open source or not), and their design is instrumental in securing the
stack's reliability and scalability.

Among other things, OSDs are responsible for the decentralized
replication — which is highly configurable — of objects in the
store. They do so in a primary-copy fashion: every Ceph object (more
precisely, the Placement Group it is a part of) is written to the
primary OSD first, and from there replicates to one or several replica
OSDs to ensure redundancy. This replication is synchronous, such that
a new or updated object guarantees its availability (in the way
configured by the cluster administrator) before an application is
notified that the write has completed.

More specifically, in order for an OSD to acknowledge a write as
completed, the new object must have been written to the OSD's
journal. OSDs use a write-ahead mode for local operations: a write
hits the journal first, and from there is then being copied into the
backing filestore. (Note: if your filestore is using btrfs, the
journal is applied in parallel with the filestore write instead. Btrfs
still being experimental, however, this is not a configuration often
used in production.) Thus, for best cluster performance it is crucial
that the journal is fast, whereas the filestore can be comparatively
slow.

This, in turn, leads to a common design principle for Ceph clusters
that are both fast and cost-effective:

- Put your filestores on slow, cheap drives (such as SATA spinners),
- put your journals on fast drives (SSDs, Fusion-IO cards, whatever
  you can afford).

Another common design principle is that you create one OSD per
spinning disk that you have in the system. Many contemporary systems
come with only two SSD slots, and then as many spinners as you
want. That is not a problem for journal capacity — a single OSD's
journal is usually no larger than about 6 GB, so even for a 16-spinner
system (approx. 96GB journal space) appropriate SSDs are available at
reasonable expense.

Many operators are scared of an SSD suddenly dying a horrible death,
so they put their SSDs in a RAID-1. Many are also tempted to put their
OSD journal partitions onto the same RAID. Another option is to use,
say, one partition on each of your SSD in a RAID for the operating
system installation, and then chop up the rest of your SSDs as
non-RAIDed Ceph OSD journals.

This creates an interesting situation when you get to more than about
10-or-so OSDs (the exact number is hard to give). Now you have your OS
and several OSD journals on the same physical SSD. SSDs are much
faster than spinners, but they have neither infinite throughput nor
zero latency. Eventually, you might hit your SSD's physical limits for
random I/O all over the place. For example, if one of your hosts dies
and the rest now reshuffles data to restore the desired level of
redundancy, you may see relatively intensive I/O all over the other
OSDs — this is exacerbated in a system where you have few OSD hosts
which host many OSD disks.

Putting your journal SSDs in a RAID set looks like a good idea at
first. Specifically, Ceph OSDs currently cannot recover from a broken
SSD journal without reinitializing and recovering the entire
filestore. This means that as soon as SSD acting as journal backing
storage burns up, you've effectively lost those OSDs completely and
need to recover them from scratch.[^mkjournal]

Put them in a RAID-1, problem solved?  Well, not quite, because you've
now duplicated all of your journal writes and you're hitting two SSDs
all over the place. Thus it's generally a much better idea to put half
of your journals on one SSD, and half on the other. If one of your
SSDs burns up you'll still lose the OSDs whose journals it hosts — but
it'll only be half of the OSDs hosted on that node altogether.

Any such performance issues get worse if some of your OSDs are also
MONs: your OSD journals now compete with your operating system and
your MONs for I/O on the same SSDs. Once your SSDs get hit so hard
that your MONs can't do I/O, those MONs eventually die. This might not
harm your operations if you have sufficient backup MONs available, and
everything will be fine again once your recovery is complete, but it's
still a nuisance. This is remarkably common specifically in POCs, by
the way, where people often try to repurpose three of their old,
two-SSDs-plus-dozens-of-disks storage servers for a 3-node Ceph
cluster.

So, as you are considering your OSD journal and filestore layout, take
note of the following general guidelines:

- By and large, try to go for a relatively small number of OSDs per
  node, ideally not more than 8. This combined with SSD journals is
  likely to give you the best overall performance.

- If you do go with OSD nodes with a very high number of disks,
  consider dropping the idea of an SSD-based journal. Yes, in this
  kind of setup you might actually do better with journals on the
  spinners.

- Alternatively in the same scenario, consider putting your operating
  system install on one or a couple of the spinners (presumably
  smaller ones than the others), and use the (un-RAIDed) SSDs for OSD
  journals exclusively.

- Consider having a few dedicated MONs (MONs that are not also OSDs).

## Note on `ceph-osd --mkjournal`

[^mkjournal]:
	Since this article was originally published, a `--mkjournal`
	option was added to the `ceph-osd` command, allowing you to
	recreate a journal for an existing OSD. This mitigates the issue
	in that you don't need to recreate OSDs from scratch when a
	journal device breaks — but the OSDs will still be **temporarily**
	unavailable.

* * *

This article originally appeared on the `hastexo.com` website (now defunct).
