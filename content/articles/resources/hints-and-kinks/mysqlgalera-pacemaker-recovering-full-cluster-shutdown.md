Title: Recovering from full cluster shutdown
Slug: mysqlgalera-pacemaker-recovering-full-cluster-shutdown
Series: MySQL/Galera in Pacemaker High Availability Clusters
Series_index: 9
Date: 2012-12-04 10:53:27 +0100
Tags: Galera, MySQL, Pacemaker

If at any time *all* of the nodes in your cluster have been taken
down, it is necessary to re-initialize the Galera replication
state. In effect, this is identical to bootstrapping the cluster.

Start by manually bringing up the cluster IP on one of your nodes:

```sh
ip address add 192.168.122.99/24 dev eth1 label eth1:galera
```

Re-initialize the Galera cluster:

```sh
mysqld --wsrep_cluster_address=gcomm:// &
```

Note the empty `gcomm://` address.

Finally, clear your resource state with `crm resource cleanup
cl_mysql`. Pacemaker will leave the running IP address and MySQL
instance untouched, and bring up the additional MySQL instances.
* * *

This article originally appeared on the `hastexo.com` website (now defunct).
