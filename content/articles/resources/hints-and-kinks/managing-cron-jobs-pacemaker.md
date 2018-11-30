Title: Managing cron jobs with Pacemaker
Date: 2012-03-19 16:42:40 +0100
Slug: managing-cron-jobs-pacemaker
Tags: Pacemaker

It's not uncommon in Pacemaker clusters to run specific cron jobs only
on a node that currently runs a particular resource. The
`ocf:heartbeat:symlink` resource agent can be exceptionally helpful in
this situation. Here's how to use it.

Suppose you've got a cron job for Postfix whose definition normally
lives in `/etc/cron.d/postfix`. All your Postfix related data is in a
mountpoint `/srv/postfix` (that filesystem could live on iSCSI, or DRBD,
or it could be a GlusterFS mount – that's irrelevant for the purposes
of this discussion). And as such, you've moved your cron definition to
`/srv/postfix/cron`.

Now you want that cron job to execute only on the node that also is
currently the active Postfix host. That's not hard at all:

```
primitive p_postfix ocf:heartbeat:postfix \
  params config_dir="/etc/postfix" \
  op monitor interval="10"
primitive p_symlink ocf:heartbeat:symlink \
  params target="/srv/postfix/cron" \
    link="/etc/cron.d/postfix" \
    backup_suffix=".disabled" \
  op monitor interval="10"
primitive p_cron lsb:cron \
  op monitor interval=10
order o_symlink_before_cron inf: p_symlink p_cron
colocation c_cron_on_symlink inf: p_cron p_symlink
colocation c_symlink_on_postfix inf: p_symlink p_postfix
```

What this will do for you is this:

- Check whether a file named `postfix` already exists in `/etc/cron.d`

- If it does, rename it to `postfix.disabled` (remember, cron ignores
  job definitions with dots in the filename)

- (Re-)Create the postfix job definition as a symlink to
  `/srv/postfix/cron`

- Restart `cron` when it's done.

The `c_symlink_on_postfix` colocation ensures that all of this happens
on the node where the `p_postfix` resource is also active.
* * *

This article originally appeared on the `hastexo.com` website (now defunct).
