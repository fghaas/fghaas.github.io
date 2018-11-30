Title: Wiping and resetting your SUSE OpenStack Cloud Crowbar configuration
Date: 2016-07-05
Slug: wipe-suse-openstack-cloud-config
Tags: OpenStack, SUSE

**Note: This article was originally written for SUSE OpenStack Cloud
6, and updated for SUSE OpenStack Cloud 7. It may not apply to later
SUSE OpenStack Cloud releases.**

If you're using [SUSE OpenStack
Cloud](https://www.suse.com/products/suse-openstack-cloud), you may
want to erase and reinstall your cloud deployment a few times during
the testing or proof-of-concept phase. You may also want to experiment
with a few permutations of Crowbar network configurations. SUSE's
(otherwise excellent) [Deployment
Guide](https://www.suse.com/documentation/suse-openstack-cloud-7/book_cloud_deploy/data/book_cloud_deploy.html)
suggests that the only way to change your Crowbar settings, after
`install-suse-cloud` has been run, [is to reinstall your entire admin
node](https://www.suse.com/documentation/suse-openstack-cloud-7/book_cloud_deploy/data/sec_depl_adm_inst_crowbar_network.html).
That isn't really true if you know what you're doing.

You may be thinking that you could just use
[`snapper`](http://snapper.io/) to
[revert to your last Btrfs snapshot](https://www.suse.com/documentation/sles-12/book_sle_admin/data/sec_snapper_auto.html)
created before you ran `install-suse-cloud`. After all, running `yast2
crowbar`, like any other YaST module, automatically creates a
before-and-after Btrfs snapshot of your root filesystem and all its
subvolumes. So, reboot machine, select pre-`install-suse-cloud`
snapshot, complete boot, run `snapper rollback`, done. Right?

Well, not quite. If you
[followed the Deployment Guide closely,](https://www.suse.com/documentation/suse-openstack-cloud-7/book_cloud_deploy/data/sec_depl_adm_inst_partition.html)
you will have removed your Btrfs subvolume for the `/srv` directory,
and replaced it with a separate, XFS-formatted partition. That means
it is excluded from all `snapper` Btrfs snapshots, and thus, no
rollback for you for that directory. Which, of course, Crowbar uses
rather extensively.

So, here is your checklist for resetting your admin node to a
pre-`install-suse-cloud` state:

- Reboot your admin node.

- In the SLES boot menu, select an appropriate snapshot taken
  immediately prior to running `install-suse-cloud`.

- Boot into your snapshot.

- Run `snapper rollback`.

- Reboot again.

- After rebooting, delete the following and directories:

    * `/srv/tftpboot/authorized_keys`
    * `/srv/tftpboot/validation.pem`
    * all subdirectories under `/srv/tftpboot/nodes/`

Then, you can reconfigure Crowbar (`yast2 crowbar`), run
`install-suse-cloud`, and reboot your OpenStack nodes. They should be
discovered anew, and you're then able to redeploy your OpenStack
barclamps to them.

* * *

This article originally appeared on the `hastexo.com` website (now defunct).
