Title: Testing resource recovery
Slug: mysqlgalera-pacemaker-testing-resource-recovery
Series: MySQL/Galera in Pacemaker High Availability Clusters
Series_index: 7
Date: 2012-12-04 10:53:27 +0100
Tags: Galera, MySQL, Pacemaker


If MySQL happens to die in your cluster, Pacemaker will automatically
recover the service in place. To test this, select any node on your
cluster and send the `mysqld` process a `KILL` signal:

```sh
killall -KILL mysqld
```

Then, monitor your cluster status with `crm_mon -rf`. After a few
seconds, you should see one of your `p_mysql` clones entering the
`FAILED` state:

```
============
Last updated: Mon Dec  3 19:03:25 2012
Last change: Mon Dec  3 18:54:44 2012 via crmd on bob
Stack: openais
Current DC: charlie - partition with quorum
Version: 1.1.7-ee0730e13d124c3d58f00016c3376a1de5323cff
3 Nodes configured, 3 expected votes
4 Resources configured.
============

Online: [ bob alice charlie ]

Full list of resources:

 p_ip_mysql_galera  (ocf::heartbeat:IPaddr2):   Started alice
 Clone Set: cl_mysql [p_mysql]
     p_mysql:1  (ocf::heartbeat:mysql): Started bob FAILED
     Started: [ alice charlie ]

Migration summary:
* Node alice: 
* Node bob: 
* Node charlie: 

Failed actions:
    p_mysql:1_monitor_30000 (node=bob, call=30, rc=7, status=complete): not running
```

Then, after a few seconds, the resource will automatically recover:

```
============
Last updated: Mon Dec  3 19:03:35 2012
Last change: Mon Dec  3 18:54:44 2012 via crmd on bob
Stack: openais
Current DC: charlie - partition with quorum
Version: 1.1.7-ee0730e13d124c3d58f00016c3376a1de5323cff
3 Nodes configured, 3 expected votes
4 Resources configured.
============

Online: [ bob alice charlie ]

Full list of resources:

 p_ip_mysql_galera  (ocf::heartbeat:IPaddr2):   Started alice
 Clone Set: cl_mysql [p_mysql]
     Started: [ alice bob charlie ]

Migration summary:
* Node alice: 
* Node bob: 
   p_mysql:1: migration-threshold=1000000 fail-count=1
* Node charlie: 

Failed actions:
    p_mysql:1_monitor_30000 (node=bob, call=30, rc=7, status=complete): not running
```

To subsequently get rid of the entry in the `Failed actions` list, use
`crm resource cleanup cl_mysql`.
* * *

This article originally appeared on the `hastexo.com` website (now defunct).
