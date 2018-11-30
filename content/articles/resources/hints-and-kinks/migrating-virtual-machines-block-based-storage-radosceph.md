Title: Migrating virtual machines from block-based storage to RADOS/Ceph
Date: 2012-10-22 15:31:23 +0100
Slug: migrating-virtual-machines-block-based-storage-radosceph
Tags: Ceph, libvirt

Ceph allows you to replace existing SAN storage (or SAN drop-in
substitutes) with a flexible storage solution with real scale-out
capabilities. Here is how you migrate existing virtual machines
managed by libvirt from block-based storage to a Ceph based storage
solution.

## Prerequisites

What you'll need in order to successfully manage the migration from
block-based storage to a working Ceph cluster is this:

- A working Ceph cluster. You probably guessed this one. More
  specifically, you should have
  - access to the client.admin key of your RADOS
    installation. Usually, the key will be stored in /etc/ceph/keyring
    on nodes running RADOS.
  - a RADOS pool in which you can create RBD images. You can either
    use the standard rbd pool or create your own pool. We'll use the
    libvirt pool throughout the following example.
  - a set of credentials for a client to connect to the cluster and
    create and use RBD devices. If you use a libvirt version < 0.9.7,
    you will have to use the default client.admin credentials for this
    purpose. If you run libvirt 0.9.7 or later, you should use a
    separate set of credentials (i.e. create a user called
    e.g. client.rbd and use that one). That user should have at least
    the allow r permission on your mons, and allow rw on your osds
    (the latter you can restrict to the rbd pool used if you wish).
- qemu in version 0.14 or higher
- libvirt in version 0.8.7 or higher (0.9.7 or higher if you want to
  use a separate user for this)
- Ceph 0.48 ("argonaut") or higher

## Getting Started

When migrating a VM from block-based storage to a Ceph cluster, you
unfortunately can't avoid a period of downtime (after all, you won't
be able to reliably copy a filesystem from place A to B while it's
still changing on the go). So the first thing to do is shut down a
currently running virtual machine, like we will do with the
ubuntu-amd64-alice VM in this example:

```
virsh shutdown ubuntu-amd64-alice
```

Then you need to create an RBD image within that pool. Suppose you
would like to create one that is 100GB in size (recall, all RBD images
are thin-provisioned, so it won't actually use 100GB in the Ceph
cluster right from the start).

```
qemu-img create -f rbd rbd:libvirt/ubuntu-amd64-alice 100G
```

This means you are connecting to the Ceph mon servers (defined in the
default configuration file, /etc/ceph/ceph.conf) using the
client.admin identity, whose authentication key should be stored in
/etc/ceph/keyring. The nominal image size is 102400MB, it's part of
the libvirt pool and its name is a hardly creative ubuntu-amd64-alice.

You can run this command from any node inside or outside your Ceph
cluster, as long as the configuration file and authentication
credentials are stored in the appropriate location. The next step,
however, is one that you must complete on the node where you can
currently access your block-based storage. This could either be the
machine that you have your VM's device currently connected to via
iSCSI or - if you are using a SAN drop-in replacement based on DRBD -
the machine that currently has the VM's DRBD resource in Primary mode.

If you are unsure what your VM's block device is, take a look at the
VM's configuration with

```
virsh dumpxml ubuntu-amd64-alice
```

to find out the actual device name (look out for paragraphs including
a <disk> statement). In our case, the actual device is
/dev/drbd/by-res/vm-ubuntu-amd64-alice. Now let's go ahead and do the
actual conversion. Please note: For the following command to work, you
need a properly populated /etc/ceph directory because that is where
qemu-img gets its information from. This is the command that initiates
the conversion:

```
qemu-img convert -f raw -O rbd \
  /dev/drbd/by-res/vm-ubuntu-amd64-alice \
  rbd:libvirt/ubuntu-amd64-alice
```

Once the qemu-img command has completed, the actual conversion of your
data is already done. That was easy, wasn't it? The final step is to
change your libvirt VM configuration file to reflect the changes.

## Adapting the VM's libvirt configuration (libvirt < 0.9.7)

If we want our VM to run on top of a Ceph object store, we need to
tell libvirt how to start the VM appropriately. Luckily, current
versions of libvirt support Ceph-based RBD backing devices out of the
box. Please note: All following steps assume that you have your
/etc/ceph set up properly. This means that a working ceph.conf and a
keyring file containing the authentication key for client.admin is
present.

Open up your VM's configuration for editing with

```
virsh edit ubuntu-amd64-alice
```

and scroll down to the VM's disk definition. In our example, that part of the configuration looks like this:

```xml
<disk type='block' device='disk'>
  <driver name='qemu' type='raw' cache='none'/>
  <source dev='/dev/drbd/by-res/vm-ubuntu-amd64-alice'/>
  <target dev='vda' bus='virtio'/>
  <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
</disk>
```

Replace it with an entry using our RBD image:

```
<disk type='network' device='disk'>
  <driver name='qemu' type='raw'/>
  <source protocol='rbd' name='libvirt/ubuntu-amd64-alice'>
    <host name='192.168.133.111' port='6789'/>
    <host name='192.168.133.112' port='6789'/>
    <host name='192.168.133.113' port='6789'/>
  </source>
  <target dev='vda' bus='virtio'/>
  <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
</disk>
```

Be sure to replace the three IPs in the above example with the actual
IPs of your MON servers.

Finally, start your virtual machine:

```
virsh start ubuntu-amd64-alice
```

## Adapting the VM's libvirt configuration (libvirt >= 0.9.7)

Starting with libvirt 0.9.7, you can use a user other than
client.admin to access RBD images via libvirt. We recommend to do
this. Creating such a setup works very similar to the one without a
separate user; the main difference is that it requires you to define a
secret in libvirt for the VM. First of all, figure out what user you
will be using from within libvirt and where that user's authentication
key is stored. For this example, we will assume that the user is
called client.rbd and that this user's key is stored in
/etc/ceph/keyring.client.rbd. Now, create a new UUID by calling

```
uuidgen
```

on the command line. The UUID for our example will be
5cddc503-9c29-4aa8-943a-c097f87677cf.  Then, open
/etc/libvirt/secrets/ubuntu-amd64-alice.xml and define a secret block
in there:

```xml
<secret ephemeral="no" private="no">
<uuid>5cddc503-9c29-4aa8-943a-c097f87677cf</uuid>
<usage type="ceph">
  <name>client.rbd secret</name>
</usage>
</secret>
```

Be sure to replace the example's UUID with your own, self-generated
value. Make libvirt add this secret to its internal keyring:

```
virsh secret-define \
  /etc/libvirt/secrets/ubuntu-amd64-alice.xml
```
  
Now find out your user's secret key. Do

```
ceph auth get-or-create client.rbd
```

and take note of the key. In our example,
AQB0Q4ZQYDB2MBAAYzWmHvpg7t1MzV1E0jkBww== is the key that will allow us
access as client.rbd. Then define the actual password for our secret
definition:

```
virsh secret-set-value \
  5cddc503-9c29-4aa8-943a-c097f87677cf \
  AQB0Q4ZQYDB2MBAAYzWmHvpg7t1MzV1E0jkBww==
```
  
Again, be sure to use your self-generated UUID instead of the one in
this example. Also replace the example key with your real
key. Finally, go ahead and adapt your VM settings. Open your VM
configuration with

```
virsh edit ubuntu-amd64-alice
```

and scroll down to the VM's disk definition. In our example, that part of the configuration looks like this:

```xml
<disk type='block' device='disk'>
  <driver name='qemu' type='raw' cache='none'/>
  <source dev='/dev/drbd/by-res/vm-ubuntu-amd64-alice'/>
  <target dev='vda' bus='virtio'/>
  <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
</disk>
```

Replace it with an entry using our RBD image:

```xml
<disk type='network' device='disk'>
  <driver name='qemu' type='raw'/>
  <auth username='rbd'>
    <secret type='ceph' usage='client.rbd secret'/>
  </auth>
  <source protocol='rbd' name='libvirt/ubuntu-amd64-alice'>
    <host name='192.168.133.111' port='6789'/>
    <host name='192.168.133.112' port='6789'/>
    <host name='192.168.133.113' port='6789'/>
  </source>
  <target dev='vda' bus='virtio'/>
  <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
</disk>
```

Be sure to replace the three IPs in the above example with the actual
IPs of your MON servers.

Finally, start your virtual machine:

```
virsh start ubuntu-amd64-alice
```

That's it. Your VM should now boot up and use its RBD image from Ceph
instead of its original block-based storage backing device.

* * *

This article originally appeared on the `hastexo.com` website (now defunct).
