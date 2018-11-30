Title: Setting Galera-specific MySQL options
Slug: mysqlgalera-pacemaker-setting-galera-specific-mysql-options
Series: MySQL/Galera in Pacemaker High Availability Clusters
Series_index: 4
Date: 2012-12-04 10:53:27 +0100
Tags: Galera, MySQL, Pacemaker

Now you can proceed with setting Galera specifics in your MySQL
configurations.

Create a configuration file, **identical on all cluster nodes,** named
`/etc/mysql/conf.d/galera.cnf` with the following content:

```ini
[mysqld]
bind_address=0.0.0.0
binlog_format=ROW
default_storage_engine=InnoDB
innodb_autoinc_lock_mode=2
innodb_locks_unsafe_for_binlog=1
```

Create another configuration file, **specific to each cluster node,**
named `/etc/mysql/conf.d/wsrep.cnf` with the following content:

```ini
[mysqld]
# node alice has address 192.168.122.111
wsrep_node_address=192.168.122.111
wsrep_provider=/usr/lib/libgalera_smm.so
wsrep_slave_threads=8
wsrep_sst_method=rsync
wsrep_cluster_address=gcomm://192.168.122.99
```

```ini
[mysqld]
# node bob has address 192.168.122.112
wsrep_node_address=192.168.122.112
wsrep_provider=/usr/lib/libgalera_smm.so
wsrep_slave_threads=8
wsrep_sst_method=rsync
wsrep_cluster_address=gcomm://192.168.122.99
```

```ini
[mysqld]
# node charlie has address 192.168.122.111
wsrep_node_address=192.168.122.113
wsrep_provider=/usr/lib/libgalera_smm.so
wsrep_slave_threads=8
wsrep_sst_method=rsync
wsrep_cluster_address=gcomm://192.168.122.99
```

You can now proceed with bootstrapping your cluster.
* * *

This article originally appeared on the `hastexo.com` website (now defunct).
