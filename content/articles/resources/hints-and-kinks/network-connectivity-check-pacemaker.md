Title: Network connectivity check in Pacemaker
Slug: network-connectivity-check-pacemaker
Date: 2012-02-27 17:45:19 +0100
Tags: Pacemaker

If you want a Pacemaker cluster to move resources on changes on the
network connectivity of an individual node, there are two major steps
involved:

- Let Pacemaker monitor connectivity;
- Configure constraints to react on connectivity changes.

## Prerequisites

Be sure to run at least Pacemaker 1.0.11 or 1.1.6 to include some
important fixes affecting the `ocf:pacemaker:ping` resource agent.

Preferably, choose more than one reliable ping targets in your network
(like a highly available gateway router, a core switch, or DNS
server).

## Pacemaker configuration

The following crm shell code snippet configures a cloned ping resource
including constraints to run Dummy resources on any node that has
connectivity at all. Please note, that the first constraint forbids to
run `p_dummy1` if all nodes lose connectivity. The second constraint
places `p_dummy2` on the node that has the best connectivity:

```
primitive p_ping ocf:pacemaker:ping \
   params host_list="dns.example.com router.example.com" \
   multiplier="1000" dampen="60s"\
   op monitor interval="10s"
clone cl_ping p_ping

primitive p_dummy1 ocf:pacemaker:Dummy
primitive p_dummy2 ocf:pacemaker:Dummy

location l_dummy1_needs_connectivity p_dummy1 \
  rule -inf: not_defined pingd or pingd lte 0
location l_dummy2_likes_best_connectivity p_dummy2 \
  rule pingd: defined pingd
```

* * *

This article originally appeared on the `hastexo.com` website (now defunct).
