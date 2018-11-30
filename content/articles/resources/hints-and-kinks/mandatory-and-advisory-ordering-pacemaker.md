Title: Mandatory and advisory ordering in Pacemaker
Date: 2012-03-22 15:02:14 +0100
Slug: mandatory-and-advisory-ordering-pacemaker
Tags: Pacemaker

Ever wonder what's the difference between `order <name> inf:
<first-resource> <second-resource>` and a score of something other
than `inf`? We'll explain.

If you specify an order constraint score of `INFINITY` (`inf` or the
keyword `mandatory` in crm shell syntax), then the order constraint is
considered mandatory. If you specify `0`, or the keyword `advisory`
then it's advisory. What does that mean?

Firstly, anytime two resources are started in the same cluster
transition, order constraints do apply regardless of whether they're
mandatory or advisory. So for the two constraints shown here:

```
order o_foo_before_bar inf: foo bar
order o_foo_before_bar 0: foo bar
```

... if `foo` and `bar` are just starting, `foo` starts first, and
`bar` starts only when `foo`'s start operation is completed. So what's
the difference, really?

## Mandatory ordering

In a **mandatory** order constraint, the order is enforced under all
circumstances. Consider the following example (primitive definitions
omitted to keep this short):

```
order o_foo_before_bar inf: foo bar
```

Suppose `foo` fails. Now `foo` must be recovered, but before that,
`bar` must also stop. So the sequence of events is:

1. `foo` fails
2. Pacemaker attempts to stop `foo` again (to make sure it's cleaned
   up).
3. `bar` stops.
4. `foo` starts
5. `bar` starts.

If `foo` fails to start back up, then `bar` will remain stopped. Based
on the start-failure-is-fatal and migration-threshold settings both
resources can now potentially migrate to other nodes, but if `foo`
can't be started anywhere, `bar` also remains stopped.

## Advisory ordering

In an **advisory** order constraint, the order is enforced only if
both resources start in the same transition. Otherwise, it's
ignored. Consider the following example (primitive definitions again
omitted):

```
order o_foo_before_bar 0: foo bar
```

Again, suppose `foo` fails. `foo` must be recovered, but now `bar` can
keep running as it's not being started in the same transition. Thus:

1. `foo` fails
2. Pacemaker attempts to stop `foo` again (to make sure it's cleaned
   up).
3. `foo` starts

If `foo` fails to start back up, then `bar` can continue to
run. Still, based on the `start-failure-is-fatal` and
`migration-threshold` settings applying to `foo`, either it or both
resources (depending on colocation constraints) can potentially
migrate to other nodes.

## So when do I use which?

Advisory ordering is good for when your dependent resource can recover
from a brief interruption in the resource it depends on. For example,
you'll want to fire up your libvirt daemon before you start your
Pacemaker-managed virtual machines, but if libvirtd were ever to crash
you can restart it without needing to restart VMs.

Mandatory ordering is for stricter dependencies. Filesystems mounted
from an iSCSI device will probably want to be remounted if the iSCSI
initator has reported an error. Likewise, you'll probably also want to
restart the applications working with that filesystem.

* * *

This article originally appeared on the `hastexo.com` website (now defunct).
