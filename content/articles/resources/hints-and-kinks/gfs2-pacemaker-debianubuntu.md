Title: GFS2 in Pacemaker (Debian/Ubuntu)
Date: 2012-02-26 20:34:08 +0100
Slug: gfs2-pacemaker-debianubuntu
Tags: Pacemaker

Setting up GFS2 in Pacemaker requires configuring the Pacemaker DLM,
the Pacemaker GFS control daemon, and a GFS2 filesystem itself.

## Prerequisites

GFS2 with Pacemaker integration is supported on Debian
(`squeeze-backports` and up) and Ubuntu (10.04 LTS and up). You'll need
the `dlm-pcmk`, `gfs2-tools`, and `gfs-pcmk` packages.

Fencing is imperative. Get a proper fencing/STONITH configuration set
up and test it thoroughly.

## Pacemaker configuration

The Pacemaker configuration, shown here in `crm` shell syntax, normally
puts all the required resources into one cloned group. Have a look at
this configuration snippet:

```
primitive p_dlm_controld ocf:pacemaker:controld \
  params daemon="dlm_controld.pcmk" \
  op start interval="0" timeout="90" \
  op stop interval="0" timeout="100" \
  op monitor interval="10"
primitive p_gfs_controld ocf:pacemaker:controld \
  params daemon="gfs_controld.pcmk"\
  op start interval="0" timeout="90" \
  op stop interval="0" timeout="100" \
  op monitor interval="10"
primitive p_fs_gfs2 ocf:heartbeat:Filesystem \
  params device="<your device path>" \
    directory="<your mount point>" \
    fstype="gfs2" \
  op monitor interval="10"
group g_gfs2 p_dlm_controld p_gfs_controld p_fs_gfs2
clone cl_gfs2 g_gfs2 \
  meta interleave="true"
```

Then when that's done, your filesystem should happily mount on all nodes.
* * *

This article originally appeared on the `hastexo.com` website (now defunct).
