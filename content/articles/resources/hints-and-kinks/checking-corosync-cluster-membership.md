Title: Checking Corosync cluster membership
Date: 2012-03-04 23:42:35 +0100
Slug: checking-corosync-cluster-membership
Tags: Corosync

It's simple and easy to get Pacemaker's view of the status of members
in a cluster – just invoke `crm_mon`. But what if you want to check on
the cluster membership when Pacemaker is not running, or you want to
make sure whether Corosync's view of the cluster is identical to
Pacemaker's? Here's how.

## Checking ring status with `corosync-cfgtool`

The `corosync-cfgtool` utility displays the cluster connectivity status
when invoked with the `-s` flag:

```
# corosync-cfgtool -s
Printing ring status.
Local node ID 303938909
RING ID 0
	id	= 10.0.1.1
	status	= ring 0 active with no faults
RING ID 1
	id	= 192.168.42.1
	status	= ring 1 active with no faults
```

The above is the status of two healthy rings; a failed ring (one
affected by a network interruption, for example) would show a `FAULTY`
status.

There's a catch. In a two-node cluster, if both nodes were to start
while all cluster communication links are down, then Corosync would
form *two* memberships with healthy, one-member rings. Both of the
nodes would show a ring status similar to the above, but your cluster
still wouldn't be communicating. So, you can't rely on
`corosync-cfgtool -s` alone. You must also check Corosync's member
list.

## Querying the member list with `corosync-cmapctl`

We can examine Corosync's cluster member list with the `corosync-cmapctl` command:

```
# corosync-cmapctl | grep member
runtime.totem.pg.mrp.srp.members.303938909.ip=r(0) ip(10.0.1.1) r(1) ip(192.168.42.1) 
runtime.totem.pg.mrp.srp.members.303938909.join_count=1
runtime.totem.pg.mrp.srp.members.303938909.status=joined
runtime.totem.pg.mrp.srp.members.320716125.ip=r(0) ip(10.0.1.2) r(1) ip(192.168.42.2) 
runtime.totem.pg.mrp.srp.members.320716125.join_count=1
runtime.totem.pg.mrp.srp.members.320716125.status=joined
```

In this example, we have two nodes (with node IDs `303938909` and
`320716125`). They are both configured to use two communication rings,
`r(0)` and `r(1)`, and both of them have successfully joined the
cluster.

**Note:** In earlier Corosync releases (pre-2.0), the
`corosync-cmapctl` tool was called `corosync-objctl`. Its command
syntax for querying the member list was identical.


* * *

This article originally appeared on the `hastexo.com` website (now defunct).
