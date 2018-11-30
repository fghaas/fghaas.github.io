Title: Fencing in VMware virtualized Pacemaker nodes
Date: 2012-05-18 09:43:28 +0100
Slug: fencing-vmware-virtualized-pacemaker-nodes
Tags: Pacemaker

For users of VMware virtualization, it's becoming increasingly common
to deploy Pacemaker clusters within the virtual infrastructure. Doing
this requires that you set up fencing via ESX Server or, more
commonly, vCenter. Here's how to do that.

The `cluster-glue` package contains node Pacemaker's fencing (STONITH)
plugins, one of which is the `external/vcenter` plugin. It enables
Pacemaker to interface with an ESX Server host or vCenter server. When
a Pacemaker node needs to be fenced, the fencing node contacts the
vCenter host and instructs it to knock out the offending node.

For this to work, your configuration needs to satisfy a couple of prerequisites:

- Your setup needs a reasonably recent cluster-glue package (the one
  that ships in Debian squeeze-backports and Ubuntu precise is fine).

- You need to install the [vSphere Web Services
  SDK](http://www.vmware.com/support/developer/vc-sdk/) on your
  nodes. This itself has a number of Perl prerequisites. On
  Debian/Ubuntu systems, you should be able to install them with:

```
aptitude install libarchive-zip-perl libcrypt-ssleay-perl \
  libclass-methodmaker-perl libuuid-perl \
  libsoap-lite-perl libxml-libxml-perl
```

Now, create a set of vCenter credentials with the `credstore_admin.pl`
utility that comes bundled with the SDK:

```
/usr/lib/vmware-vcli/apps/general/credstore_admin.pl \
  -s <vCenter server IP or hostname> \
  -u <vCenter username> \
  -p <vCenter password>
```

This creates a credentials file in
`.vmware/credstore/vicredentials.xml` relative to your home
directory. Copy this file into a location where Pacemaker can find it,
say `/etc/vicredentials.xml`, and make sure it gets 0600
permissions. Also, remember to copy it to all your cluster nodes. Once
your credentials are properly set up, you can test the STONITH agent's
functionality by invoking it directly, like so:

```sh
  VI_SERVER=<vCenter server IP or hostname> \
  VI_CREDSTORE=/etc/vicredentials.xml \
  HOSTLIST="<pacemaker hostname>=<vCenter virtual machine name>" \
  RESETPOWERON=0 \
  /usr/lib/stonith/plugins/external/vcenter gethosts
```

<pacemaker hostname> is the name of one of your cluster nodes as per
uname -n, and <vCenter virtual machine name> is the corresponding
machine name in your vCenter inventory. If everything is working fine,
the gethosts command should return the Pacemaker hostname again.

Now, on to adding this to the Pacemaker configuration. The example
below is for two hosts named alice and bob, which in the inventory
happen to be listed by their FQDN in the example.com domain:

```
primitive p_fence_alice stonith:external/vcenter \
  params VI_SERVER="vcenter.example.com" \
    VI_CREDSTORE="/etc/vicredentials.xml" \
    HOSTLIST="alice=alice.example.com" \
    RESETPOWERON="0" \
    pcmk_host_check="static-list" \
    pcmk_host_list="alice" \
  op monitor interval="60"
primitive p_fence_bob stonith:external/vcenter \
  params VI_SERVER="vcenter.example.com" \
    VI_CREDSTORE="/etc/vicredentials.xml" \
    HOSTLIST="bob=bob.example.com" \
    RESETPOWERON="0" \
    pcmk_host_check="static-list" \
    pcmk_host_list="bob" \
  op monitor interval="60"
location l_fence_alice p_fence_alice -inf: alice
location l_fence_bob p_fence_bob -inf: bob
property stonith-enabled="true"
```

At this point you should be able to test fencing with `stonith_admin
-F` or `crm node fence`. Or simulate a node problem with `killall -9
corosync`.

Special thanks for this goes to Nhan Ngo Dinh both for writing the
plugin in the first place, and for providing an excellent and
straightforward README file for it.
* * *

This article originally appeared on the `hastexo.com` website (now defunct).
