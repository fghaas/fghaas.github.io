Title: Bootstrapping the Galera cluster
Slug: mysqlgalera-pacemaker-bootstrapping-galera-cluster
Series: MySQL/Galera in Pacemaker High Availability Clusters
Series_index: 5
Date: 2012-12-04 10:53:27 +0100
Tags: Galera, MySQL, Pacemaker

In order to bootstrap your Galera cluster, manually bring up the
cluster IP address on the desired interface. In this example, we'll
use 192.168.122.99 and eth1:

```sh
ip address add 192.168.122.99/24 dev eth1 label eth1:galera
```

And initialize the Galera cluster:

```sh
mysqld --wsrep_cluster_address=gcomm:// &
```

Note the empty `gcomm://` address.

An avalanche of output is likely to follow. Near the end, you should
see entries similar to these:

```
[Note] WSREP: Synchronized with group, ready for connections
[Note] mysqld: ready for connections.
```

At this point, your MySQL/Galera cluster is properly initialized. It
only has one node, and it is not under cluster management yet, but
it's already a working Galera installation.

* * *

This article originally appeared on the `hastexo.com` website (now defunct).
