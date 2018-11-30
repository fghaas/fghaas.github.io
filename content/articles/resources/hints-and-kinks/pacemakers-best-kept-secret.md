Title: Pacemaker's best-kept secret: crm_report
Slug: pacemakers-best-kept-secret
Tags: Pacemaker
Date: 2016-01-30
Modified: 2016-02-03
Summary: Pacemaker has an excellent, but little-known, error reporting facility: crm_report.

Whenever things in Pacemaker go wrong (say, for example, resource
failover doesn't work as expected, or your cluster didn't properly
recover after a node shutdown), you'll want to find out just exactly
*why* that happened. Of course, the actual reason for the malfunction
may be buried somewhere deep in your cluster configuration or setup,
and so you might need to look at quite a few different sources to pin
it down.

Sometimes, too, you want to enlist the help of a colleague, [or maybe
**our** help even](/contact), to get to the bottom of the issue. And
sometimes it's not practical to let someone access to system to just
trigger the problem and watch what breaks.

Thankfully, Pacemaker ships with a utility that helps you collect
everything you or someone else might need to look at, in a simple,
compact format. Unfortunately few people, including even long-time
Pacemaker users, know that it exists: it's called `crm_report`.

## Running `crm_report`

`crm_report`'s command syntax is rather quite simple. You just tell it
how far in the past you want the report to start, and which directory
you want to collect data in:

```sh
crm_report -f "2016-01-25 00:00:00" /tmp/crm_report
```

The directory you specify must not exist. If it does, `crm_report`
will refuse to run, rather than clobber or mess up your existing
report data.

By analyzing your logs all the way back to a start date you specify,
**`crm_report` makes it unnecessary for you to actually try to
reproduce the problem.** All you need is a rough idea when the issue
occurred, and then you give `crm_report` a timestamp a little earlier
than that as its start date.

You can also specify the *end* of the period you're interested
in. Suppose you're exactly aware of a 10-minute time window in which
the problem occurred. In that case, you could run:

```sh
crm_report -f "2016-01-25 01:15:00" -t "2016-01-25 01:25:00" /tmp/crm_report
```

Either way, `crm_report` will collect relevant log data for the
specified time window on the host it is run on, and then connect to
the other cluster nodes (via `ssh`) and do the same there. The latter
behavior can be disabled by adding the `-S` or `--single-node` option,
but there usually isn't a good reason to do that. In the end,
everything will be rolled into one tarball at
`/tmp/crm_report.tar.bz2`

You can then pull the report tarball off the node (with `scp`,
`rsync`, whatever you prefer), and then share it with whom you need
to. **Note that the tarball can contain sensitive information such as
passwords, so be careful whom you share it with.**


## What's in a `crm_report` tarball?

There's a bunch of truly helpful information in a `crm_report`
generated tarball. Depending on how your cluster is configured and
what problems were detected, it will contain, among other things:

- Your current Pacemaker Cluster Information Base (CIB),

- Your Corosync configuration,

- Corosync Blackbox output (if `qb-blackbox` is installed on your
  cluster nodes; you can read more about blackbox support
  [here](http://blog.clusterlabs.org/blog/2013/pacemaker-logging/)),

- `drbd.conf` and all your DRBD resource configuration files (if your
  cluster runs DRBD),

- `sysinfo.txt`, a text file including your kernel, distro, Pacemaker
  version, and version information for all your installed packages,

- your Syslog, filtered for the time period you specified in your
  `crm_report` command invocation,

- diffs for critical system information, if `crm_report` detected
  discrepancies between nodes.

In other words, it contains pretty much everything that needs to be
shared in a critical troubleshooting situation.

## Why isn't this more widely known?

To be perfectly honest, we have no idea. `crm_report` has been in
Pacemaker for years, and even prior to its existence, there was a
predecessor named `hb_report`. It's an extraordinarily useful utility,
yet when we ask customers to send a `crm_report` tarball during a
Pacemaker troubleshooting engagement, the usual response is, &ldquo;a
what?&rdquo;

We hope this post makes `crm_report` known to a wider audience, so it
gets the love it deserves. <i class="fa fa-smile-o"></i>
* * *

This article originally appeared on the `hastexo.com` website (now defunct).
