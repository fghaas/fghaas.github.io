Title: Adding MySQL/Galera resources to Pacemaker
Slug: mysqlgalera-pacemaker-adding-mysqlgalera-resources-pacemaker
Series: MySQL/Galera in Pacemaker High Availability Clusters
Series_index: 6
Date: 2012-12-04 10:53:27 +0100
Tags: Galera, MySQL, Pacemaker

Once you have one instance of Galera running, and it is running on the
same node that holds the temporarily-configured cluster IP
(192.168.122.99 in our example), you can add your resources to the
Pacemaker cluster configuration.

Create a temporary file, such as `/tmp/galera.crm`, with the following
contents:

```
primitive p_ip_mysql_galera ocf:heartbeat:IPaddr2 \
  params nic="eth1" iflabel="galera" \
    ip="192.168.122.99" cidr_netmask="24"
primitive p_mysql ocf:heartbeat:mysql \
  params config="/etc/mysql/my.cnf" \
    pid="/var/run/mysqld/mysqld.pid" \
    socket="/var/run/mysqld/mysqld.sock" \
    binary="/usr/sbin/mysqld" \
  op monitor interval="30s" \
  op start interval="0" timeout="60s" \
  op stop interval="0" timeout="60s"
clone cl_mysql p_mysql \
  meta interleave="true"
colocation c_ip_galera_on_mysql \
  inf: p_ip_mysql_galera cl_mysql
property stonith-enabled="false"
```

Then, import this into your Pacemaker configuration:

```sh
crm configure load update /tmp/galera.crm
```

What this creates are a couple of Pacemaker resources:

- The cluster IP address, 192.168.122.99
  (`p_ip_mysql_galera`). Throughout the lifetime of the cluster, this
  will always be available on one of the nodes where any MySQL/Galera
  instance is running. This is the IP address new Galera nodes use
  when joining the cluster.

- The MySQL server itself (`cl_mysql`), which will be automatically
  recovered in-place if it ever fails.
* * *

This article originally appeared on the `hastexo.com` website (now defunct).
