Title: Solve a DRBD split-brain in 4 steps
Slug: solve-drbd-split-brain-4-steps
Date: 2012-03-06 01:29:24 +0100
Tags: DRBD

Whenever a DRBD setup runs into a situation where the replication
network is disconnected and fencing policy is set to `dont-care`
(default), there is the potential risk of a split-brain. Even with
resource level fencing or STONITH setup, there are corner cases that
will end up in a split-brain.

When your DRBD resource is in a split-brain situation, don't panic!
Split-brain means that the contents of the backing devices of your
DRBD resource on both sides of your cluster started to diverge. At
some point in time, the DRBD resource on both nodes went into the
Primary role while the cluster nodes themselves were disconnected from
each other.

Different writes happened to both sides of your cluster
afterwards. After reconnecting, DRBD doesn't know which set of data is
"right" and which is "wrong".

## Indications of a Split-Brain

The symptoms of a split-brain are that the peers will not reconnect on
DRBD startup but stay in connection state StandAlone or
WFConnection. The latter will be shown if the remote peer detected the
split-brain earlier and was faster at shutdown its connection. In your
kernel logs you will see messages like:

```
kernel: block drbd0: Split-Brain detected, dropping connection!
```

## 4 Steps to solve the Split-Brain

### Step 1

Manually choose a node which data modifications will be discarded.

We call it the split brain victim. Choose wisely, all modifications
will be lost! When in doubt run a backup of the victim's data before
you continue.

When running a Pacemaker cluster, you can enable maintenance mode. If
the split brain victim is in Primary role, bring down all applications
using this resource. Now switch the victim to Secondary role:

```
victim# drbdadm secondary resource
```

### Step 2

Disconnect the resource if it's in connection state `WFConnection`:

```
victim# drbdadm disconnect resource
```

### Step 3

Force discard of all modifications on the split brain victim:

```
victim# drbdadm -- --discard-my-data connect resource
```

for DRBD 8.4.x:

```
victim# drbdadm connect --discard-my-data resource
```

### Step 4

Resync will start automatically if the survivor was in
`WFConnection` network state. If the split brain survivor is still in
`Standalone` connection state, reconnect it:

```
survivor# drbdadm connect resource
```

At the latest now the resynchronization from the survivor
(`SyncSource`) to the victim (`SyncTarget`) starts immediately. There
is no full sync initiated but all modifications on the victim will be
overwritten by the survivor's data and modifications on the survivor
will be applied to the victim.

## Background: What happens?

With the default after-split-brain policies of disconnect this will
happen always in dual primary setups. It can happen in single primary
setups if one peer changes at least once its role from Secondary to
Primary while disconnected from the previous (before network
interruption) Primary.

There are a variety of automatic policies to solve a split brain but
some of them will overwrite (potentially valid) data without further
inquiry. Even with theses policies in place a unresolvable split-brain
can occur.

The split-brain is detected once the peers reconnect and do their DRBD
protocol handshake which also includes exchanging of the Generation
Identifiers (GIs).
* * *

This article originally appeared on the `hastexo.com` website (now defunct).
