Title: Configuring Corosync
Slug: mysqlgalera-pacemaker-configuring-corosync
Series: MySQL/Galera in Pacemaker High Availability Clusters
Series_index: 2
Date: 2012-12-04 10:53:27 +0100
Tags: Galera, MySQL, Pacemaker

You now need configure Corosync. The following example configuration
file assumes that your cluster nodes have two network interfaces,
using the 192.168.122.0/24 and 192.168.133.0/24 networks. You will
need to adjust this to your own network configuration.

Set the contents of `/etc/corosync/corosync.conf` as follows:

```
compatibility: whitetank

totem {
        version: 2
        secauth: on
        threads: 0
        rrp_mode: active
        token: 10000
        interface {
                ringnumber: 0
                bindnetaddr: 192.168.122.0
                mcastaddr: 239.255.42.0
                mcastport: 5405
                ttl: 1
        }
        interface {
                ringnumber: 1
                bindnetaddr: 192.168.133.0
                mcastaddr: 239.255.42.1
                mcastport: 5405
                ttl: 1
        }
}

logging {
        fileline: off
        to_stderr: no
        to_logfile: no
        to_syslog: yes
        debug: off
        timestamp: on
        logger_subsys {
                subsys: AMF
                debug: off
        }
}
```

Also, create an authkey file for node authentication:

```sh
dd if=/dev/urandom of=/etc/corosync/authkey bs=128 count=1
chmod 0400 /etc/corosync/authkey
```

And create `/etc/corosync/service.d/pacemaker` with the following content:

```
service {
    name: pacemaker
    ver; 1
}
```

Finally, distribute the configuration across your cluster:

```sh
for n in bob charlie; do
  rsync -av /etc/corosync/* $n:/etc/corosync
done
```

And start Corosync on all cluster nodes:

```sh
service corosync start
```

Once Corosync has started on all nodes, you should be able to check its status with the `corosync-cfgtool` and `corosync-objctl` commands:

```sh
# corosync-cfgtool -s
Printing ring status.
Local node ID 1870309568
RING ID 0
    id  = 192.168.122.111
    status  = ring 0 active with no faults
RING ID 1
    id  = 192.168.133.111
    status  = ring 1 active with no faults
```

Both rings should be in the `active with no faults` state.

```sh
# corosync-objctl runtime.totem.pg.mrp.srp.members
runtime.totem.pg.mrp.srp.1870309568.ip=r(0) ip(192.168.122.111) r(1) ip(192.168.133.111) 
runtime.totem.pg.mrp.srp.1870309568.join_count=1
runtime.totem.pg.mrp.srp.1870309568.status=joined
runtime.totem.pg.mrp.srp.1887086784.ip=r(0) ip(192.168.122.112) r(1) ip(192.168.133.112) 
runtime.totem.pg.mrp.srp.1887086784.join_count=1
runtime.totem.pg.mrp.srp.1887086784.status=joined
runtime.totem.pg.mrp.srp.1903864000.ip=r(0) ip(192.168.122.113) r(1) ip(192.168.133.113) 
runtime.totem.pg.mrp.srp.1903864000.join_count=1
runtime.totem.pg.mrp.srp.1903864000.status=joined
```

All three nodes members should be in the membership with both of their
interfaces, and their status should be `joined`.
* * *

This article originally appeared on the `hastexo.com` website (now defunct).
