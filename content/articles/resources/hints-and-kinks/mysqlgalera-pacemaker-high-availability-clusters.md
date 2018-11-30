Title: MySQL/Galera in Pacemaker High Availability Clusters
Slug: mysqlgalera-pacemaker-high-availability-clusters
Series: MySQL/Galera in Pacemaker High Availability Clusters
Series_index: 1
Date: 2012-12-04 10:53:27 +0100
Tags: Galera, MySQL, Pacemaker

In this walkthrough, you will create a Pacemaker managed MySQL/Galera
cluster. It assumes that you are running on a Debian 6.0 (squeeze)
box, but the concepts should be equally applicable to other platforms
with minimal modifications.

It also assumes that your Galera cluster will consist of three nodes,
named alice, bob and charlie. Furthermore, all cluster nodes can
resolve each other's hostnames.

**Please note: All commands in this walkthrough require that you are
logged into your system as root.**

First, make sure you have the required packages installed. One of the
easiest ways to get your hands on MySQL/Galera binaries is to install
Percona XtraDB Cluster, which our friends at Percona make available in
their public software repository.

Create `/etc/apt/sources.list.d/percona.list` with the following
content:

```
deb http://repo.percona.com/apt squeeze main
```

Fetch the Percona repository signing key:

```sh
apt-key adv --keyserver hkp://keys.gnupg.net --recv-keys 1C4CBDCDCD2EFD2A
```

You also require Pacemaker packages from the Debian backports
repository. Do do so, create `/etc/apt/sources.list.d/backports.list`
with the following content:

```
deb http://backports.debian.org/debian-backports squeeze-backports main
```

Now, update your package lists:

```sh
apt-get update
```

Once that is completed, you are able to install the
`percona-xtradb-cluster-server-5.5` package:

```
apt-get -y install percona-xtradb-cluster-server-5.5
```

Note that `percona-xtradb-cluster-server-5.5` conflicts with the
standard Debian `mysql-server` packages, so if you have any of those
installed, they will be removed in the process of installing XtraDB
Cluster.

Stop the MySQL server services for the time being:

```sh
service mysql stop
```

Also required is the pacemaker package (and its dependencies) from
squeeze-backports:

```sh
apt-get -t squeeze-backports install pacemaker
```

And finally rsync is required for one of the supported Snapshot State
Transfer (SST) methods for Galera:

```sh
apt-get install rsync
```

Now, all required packages are installed and you're ready to configure
XtraDB Cluster.

* * *

This article originally appeared on the `hastexo.com` website (now defunct).
