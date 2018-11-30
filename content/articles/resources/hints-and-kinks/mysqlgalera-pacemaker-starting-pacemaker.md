Title: Starting Pacemaker
Slug: mysqlgalera-pacemaker-starting-pacemaker
Series: MySQL/Galera in Pacemaker High Availability Clusters
Series_index: 3
Date: 2012-12-04 10:53:27 +0100
Tags: Galera, MySQL, Pacemaker

Once Corosync is running, you are able to start the Pacemaker cluster
resource manager on all cluster nodes:

```sh
service pacemaker start
```

Once cluster startup is completed, you should see output similar to
the following when invoking the `crm_mon` utility:

```
============
Last updated: Mon Dec  3 15:37:59 2012
Last change: Mon Dec  3 15:37:58 2012 via crmd on alice
Stack: openais
Current DC: alice - partition with quorum
Version: 1.1.7-ee0730e13d124c3d58f00016c3376a1de5323cff
3 Nodes configured, 3 expected votes
0 Resources configured.
============

Online: [ bob alice charlie ]
```
* * *

This article originally appeared on the `hastexo.com` website (now defunct).
