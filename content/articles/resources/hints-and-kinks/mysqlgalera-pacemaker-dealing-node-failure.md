Title: Dealing with node failure
Slug: mysqlgalera-pacemaker-dealing-node-failure
Series: MySQL/Galera in Pacemaker High Availability Clusters
Series_index: 8
Date: 2012-12-04 10:53:27 +0100
Tags: Galera, MySQL, Pacemaker


If an entire node happens to get killed, and that node currently does
not hold the Galera IP (192.168.122.99 in our example), then the other
nodes simply continue to function normally, and you can connect to and
use them without interruption. In the example below, `alice` has left
the cluster:

```
============
Last updated: Mon Dec  3 22:24:55 2012
Last change: Mon Dec  3 22:23:19 2012 via crmd on charlie
Stack: openais
Current DC: charlie - partition with quorum
Version: 1.1.7-ee0730e13d124c3d58f00016c3376a1de5323cff
3 Nodes configured, 3 expected votes
4 Resources configured.
============

Online: [ bob charlie ]
OFFLINE: [ alice ]

Full list of resources:

p_ip_mysql_galera       (ocf::heartbeat:IPaddr2):       Started bob
 Clone Set: cl_mysql [p_mysql]
     Started: [ bob charlie ]
     Stopped: [ p_mysql:0 ]
```

If the node dies that does currently hold the Galera IP
(192.168.122.99 in our example), then the cluster IP shifts to a
different node, and when the failed node returns, it can re-fetch the
cluster state from the node that took over the IP address. In the
example below, in a healthy cluster the IP happens to be running on
`bob`:

```
============
Last updated: Mon Dec  3 22:32:35 2012
Last change: Mon Dec  3 22:23:19 2012 via crmd on charlie
Stack: openais
Current DC: charlie - partition with quorum
Version: 1.1.7-ee0730e13d124c3d58f00016c3376a1de5323cff
3 Nodes configured, 3 expected votes
4 Resources configured.
============

Online: [ bob alice charlie ]

Full list of resources:

p_ip_mysql_galera       (ocf::heartbeat:IPaddr2):       Started bob
 Clone Set: cl_mysql [p_mysql]
     Started: [ alice bob charlie ]
```

Subsequently, `bob` is affected by a failure, and the IP address
shifts to `alice`:

```
============
Last updated: Mon Dec  3 22:33:33 2012
Last change: Mon Dec  3 22:23:19 2012 via crmd on charlie
Stack: openais
Current DC: charlie - partition with quorum
Version: 1.1.7-ee0730e13d124c3d58f00016c3376a1de5323cff
3 Nodes configured, 3 expected votes
4 Resources configured.
============

Online: [ alice charlie ]
OFFLINE: [ bob ]

Full list of resources:

p_ip_mysql_galera       (ocf::heartbeat:IPaddr2):       Started alice
 Clone Set: cl_mysql [p_mysql]
     Started: [ alice charlie ]
     Stopped: [ p_mysql:1 ]
```

When `bob` returns, it simply connects to `alice` (which now hosts the
cluster IP), fetches the database state from there, and continues to
run:

```
============
Last updated: Mon Dec  3 22:35:46 2012
Last change: Mon Dec  3 22:23:19 2012 via crmd on charlie
Stack: openais
Current DC: charlie - partition with quorum
Version: 1.1.7-ee0730e13d124c3d58f00016c3376a1de5323cff
3 Nodes configured, 3 expected votes
4 Resources configured.
============

Online: [ bob alice charlie ]

Full list of resources:

p_ip_mysql_galera       (ocf::heartbeat:IPaddr2):       Started alice
 Clone Set: cl_mysql [p_mysql]
     Started: [ alice bob charlie ]
```
* * *

This article originally appeared on the `hastexo.com` website (now defunct).
