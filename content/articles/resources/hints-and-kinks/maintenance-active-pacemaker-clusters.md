Title: Maintenance in active Pacemaker clusters
Date: 2012-09-24 19:49:31 +0100
Slug: maintenance-active-pacemaker-clusters
Tags: Pacemaker

In a Pacemaker cluster, as in a standalone system, operators must
complete maintenance tasks such as software upgrades and configuration
changes. Here's what you need to keep Pacemaker's built-in monitoring
features from creating unwanted side effects.

## Maintenance mode

This is quite possibly Pacemaker's single most useful feature for
cluster maintenance. In maintenance mode, Pacemaker essentially takes
a "hands-off" approach to your cluster. Enabling Pacemaker maintenance
mode is very easy using the Pacemaker `crm` shell:

```sh
crm configure property maintenance-mode=true
```

In maintenance mode, you can stop or restart cluster resources at
will. Pacemaker will not attempt to restart them. All resources
automatically become unmanaged, that is, Pacemaker will cease
monitoring them and hence be oblivious about their status. You can
even stop all Pacemaker services on a node, and all the daemons and
processes originally started as Pacemaker managed cluster resources
will continue to run.

You should know that when you start Pacemaker services on a node while
the cluster in maintenance mode, Pacemaker will initiate a single
one-shot monitor operation (a "probe") for every resource just so it
has an understanding of what resources are currently running on that
node. It will, however, take no further action other than determining
the resources' status.

You disable maintenance mode with the crm shell, as well:

```sh
crm configure property maintenance-mode=false
```

Maintenance mode is something you enable before running other
maintenance actions, not when you're already half-way through
them. And unless you're very well versed in the interdependencies of
resources running on the cluster you're working on, it's usually the
very safest option.

In short: when doing maintenance on your Pacemaker cluster, by
default, enable maintenance mode before you start, and disable it
after you're done.

## Disabling monitoring and error recovery on specific resources

For any configuration changes that take no more than a few minutes,
involving an admin that is potentially watching a console window the
whole time, maintenance mode is highly recommended. However, enabling
maintenance mode can be a bit hard to argue for large configuration
changes lasting, say, several hours. Think of a massive database
rebuild, for example. In such a case, you may want to put only your
database resource in something like maintenance mode, and have
Pacemaker continue to monitor other resources like normal.

You can do so by switching the resource to unmanaged mode and disable
its monitor operation:

```sh
crm configure edit p_database
```

Then change the `is-managed` meta  attribute and disable the `monitor`
operation:

```
meta is-managed=false
op monitor interval=<interval> enabled=false
```

Once you've done that, you'll effectively have enabled something akin
to maintenance mode for a single resource. You can reverse this as you
would expect:

```sh
crm configure edit p_database
```

Then change the `is-managed` meta attribute and re-enable the
`monitor` operation:

```
meta is-managed=true
op monitor interval=<interval> enabled=true
```
When using this approach, all other resources will be monitored and
automatically recovered as they normally would. Thus, you'll have to
be acutely aware of any side effects your maintenance activities have
on other resources. If you're unsure, you should use the global
maintenance mode instead.

* * *

This article originally appeared on the `hastexo.com` website (now defunct).
