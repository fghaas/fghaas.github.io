Title: OCFS2 in Pacemaker (Debian/Ubuntu)
Slug: ocfs2-pacemaker-debianubuntu
Tags: Pacemaker
Date: 2012-02-24 17:01:20 +0100

Setting up OCFS2 in Pacemaker requires configuring the Pacemaker DLM,
the O2CB lock manager for OCFS2, and an OCFS2 filesystem itself.

## Prerequisites

- OCFS2 with Pacemaker integration is supported on Debian
  (`squeeze-backports` and up) and Ubuntu (10.04 LTS and up). You'll
  need the `dlm-pcmk`, `ocfs2-tools`, `ocfs2-tools-pacemaker` and
  `openais` packages.

- Fencing is imperative. Get a proper fencing/STONITH configuration
  set up and test it thoroughly.

- Running OCFS2/Pacemaker integration requires that you load Corosync
  with the `openais_ckpt` service enabled. The service definition is in
  the file `/etc/corosync/service.d/ckpt-service` which the `openais`
  package installs by default. Make sure you did not accidentally
  delete or disable this file.

## Pacemaker configuration

The Pacemaker configuration, shown here in crm shell syntax, normally
puts all the required resources into one cloned group. Have a look at
this configuration snippet:

```
primitive p_dlm_controld ocf:pacemaker:controld \
  op start interval="0" timeout="90" \
  op stop interval="0" timeout="100" \
  op monitor interval="10"
primitive p_o2cb ocf:pacemaker:o2cb \
  op start interval="0" timeout="90" \
  op stop interval="0" timeout="100" \
  op monitor interval="10"
primitive p_fs_ocfs2 ocf:heartbeat:Filesystem \
  params device="<your device path>" \
    directory="<your mount point>" \
    fstype="ocfs2" \
  meta target-role=Stopped \
  op monitor interval="10"
group g_ocfs2 p_dlm_controld p_o2cb p_fs_ocfs2
clone cl_ocfs2 g_ocfs2 \
  meta interleave="true"
```

## Why keep the filesystem stopped?

Because you probably either don't have a configured OCFS2 filesystem
on your device yet, or your ran mkfs.ocfs2 when the Pacemaker stack
wasn't running. In either of those two cases, mount.ocfs2 will refuse
to mount the filesystem.

Thus, fire up your DLM and the o2cb process like the above
configuration does, and then:

- If you haven't got a filesystem yet, run `mkfs.ocfs2` on your device, or

- If you do already have one, run
  `tunefs.ocfs2 --update-cluster-stack <device>`.

Then when that's done, run `crm resource start p_fs_ocfs2` and your
filesystem should happily mount on all nodes.

* * *

This article originally appeared on the `hastexo.com` website (now defunct).
