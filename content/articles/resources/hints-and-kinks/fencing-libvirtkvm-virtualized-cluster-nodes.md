Title: Fencing in Libvirt/KVM virtualized cluster nodes
Date: 2012-02-29 13:56:42 +0100
Slug: fencing-libvirtkvm-virtualized-cluster-nodes
Tags: Pacemaker

Often, people deploy the Pacemaker stack in virtual environments for
purposes of testing and evaluation. In such environments, it's easy to
test Pacemaker's fencing capabilities by tying in with the hypervisor.

This quick howto illustrates how to configure fencing for two virtual
cluster nodes hosted on a libvirt/KVM hypervisor host.

## libvirt configuration (hypervisor)

In order to do libvirt fencing, your hypervisor should have its
libvirtd daemon listen on a network socket. libvirtd is capable of
doing this, both on an encrypted TLS socket, and on a regular,
unencrypted TCP port. Needless to say, for production use you should
only use TLS, but for testing and evaluation – and for that purpose
only – TCP is fine.

In order for your hypervisor to listen on an unauthenticated,
insecure, unencrypted network socket (did we mention that's unsuitable
for production?), add the following lines to your libvirtd
configuration file:

```ini
listen_tls = 0
listen_tcp = 1
tcp_port = "16509"
auth_tcp = "none"
```

You can also set the `listen_addr` parameter, for example to have
libvirtd listen only on the network that your virtual machines run
in. If you don't set listen_addr, libvirtd will simply listen on the
wildcard address.

You'll also have to add the `-l` or `--listen` flag to your libvirtd
invocation. On Debian/Ubuntu platforms, you can do so by editing the
`/etc/default/libvirt-bin` configuration file.

Once you've done that, you can use `netstat -ltp` to check whether
libvirtd is in fact listening on its configured port, 16509/tcp. Also,
make sure that you don't have a firewall blocking that port.

## libvirt configuration (virtual machines)

Inside your virtual machines, you'll also have to install the libvirt
client binaries – the fencing mechanism uses the virsh utility under
the covers. Some platforms provide a `libvirt-client` package for that
purpose; for other's, you'll simply have to install the full `libvirt`
package.

Once that is set up, you should be able to run this command from
inside your virtual machines:

```sh
virsh --connect=qemu+tcp://<IP of your hypervisor>/system \
  list --all
```

... and that command should list all the domains running on that host,
including the one you're connecting from.

## Pacemaker configuration

In one of your virtual machines, you can now set up your fencing
configuration.

This example assumes that you have two nodes named alice and bob, that
their corresponding virtual machine domain names are also alice and
bob, and that they can reach their hypervisor by TCP at 192.168.0.1:

```
primitive p_fence_alice stonith:external/libvirt \
  params hostlist="alice" \
   hypervisor_uri="qemu+tcp://192.168.0.1/system" \
  op monitor interval="60"
primitive p_fence_bob stonith:external/libvirt \
  params hostlist="bob" \
    hypervisor_uri="qemu+tcp://192.168.0.1/system" \
  op monitor interval="60"
location l_fence_alice p_fence_alice -inf: alice
location l_fence_bob p_fence_bob -inf: bob
property stonith-enabled=true
```

Now you can test fencing to the best of your abilities.
* * *

This article originally appeared on the `hastexo.com` website (now defunct).
