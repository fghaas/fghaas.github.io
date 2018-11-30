Title: A minimal Ubuntu OpenStack Juju configuration in just four nodes
Date: 2015-12-23
Slug: ubuntu-openstack-juju-4-nodes
Tags: OpenStack, Juju

Juju is Ubuntu's supported and preferred means of deployment
automation for an OpenStack cloud. While in Juju, a deployment unit (a
*Juju charm*) generally expects to fully own the filesystem it is
being deployed on, Juju allows you to co-deploy charms on the same
physical machines, by way of using LXC containers.

Now in general, Juju should allow you to deploy complex service
*bundles* in one swoop, however this works best when deploying to the
bare metal (i.e. without containers). Still, it is perfectly possible
to automate Juju deployment of an entire OpenStack cloud in just 4
physical nodes:

- A controller node (running your OpenStack APIs and your dashboard);
- a compute node (running VMs under libvirt/KVM management);
- a network gateway node (providing L3 network connectivity);
- a storage node (providing Cinder volumes via iSCSI and LVM).

The assumption for the setup below is that you already have a Juju
infrastructure in place. You may have set this up with MAAS, or you
may have just bootstrapped a deployment node and then created a Juju
`manual` environment and added your 4 nodes via SSH.

Note that the environment described here should not be used for
production purposes. However, the same approach is also applicable to
a 3-node controller HA cluster, 2-node Neutron gateway cluster with
support for HA routers, and as many converged Ceph/`nova-compute`
nodes as you want.

## Juju configuration

Consider the following Juju configuration YAML example, which you
might put into your home directory as `juju-config.yaml`.

```yaml
keystone:
  openstack-origin: 'cloud:trusty-liberty'
  admin-password: 'my very secret password'
nova-cloud-controller:
  openstack-origin: 'cloud:trusty-liberty'
  network-manager: Neutron
neutron-gateway:
  openstack-origin: 'cloud:trusty-liberty'
  ext-port: eth2
  bridge-mappings: 'external:br-ex'
  os-data-network: 192.168.133.0/24
  instance-mtu: 1400
neutron-api:
  openstack-origin: 'cloud:trusty-liberty'
  network-device-mtu: 1400
  # Always make sure you enable security groups
  neutron-security-groups: true
  overlay-network-type: vxlan
rabbitmq-server:
# Cinder is deployed in two parts: one for the API and scheduler
# (which can live in a container), one for the volume service (which
# cannot, at least not for the LVM/iSCSI backend)
cinder-api:
  openstack-origin: 'cloud:trusty-liberty'
  enabled-services: api,scheduler
cinder-volume:
  openstack-origin: 'cloud:trusty-liberty'
  enabled-services: volume
  # Adjust this to match the block device on your volume host
  block-device: vdb
glance:
  openstack-origin: 'cloud:trusty-liberty'
heat:
  openstack-origin: 'cloud:trusty-liberty'
mysql:
openstack-dashboard:
  openstack-origin: 'cloud:trusty-liberty'
  webroot: /
nova-compute:
  openstack-origin: 'cloud:trusty-liberty'
  manage-neutron-plugin-legacy-mode: false
  # Change to qemu if in a nested cloud environment
  virt-type: kvm
neutron-openvswitch:
  os-data-network: 192.168.133.0/24
```

## Deployment

Then, you can run the following shell script to deploy your control
services to LXC containers on machine 1, `nova-compute` (and its
subordinate charm, `neutron-openvswitch`) to machine 2,
`neutron-gateway` to machine 3, and `cinder-volume` to machine 4.

```sh
#!/bin/bash -ex

CONFIG=~/juju-config.yaml

juju deploy --config=$CONFIG mysql --to lxc:1
juju deploy --config=$CONFIG rabbitmq-server --to lxc:1

sleep 120s

juju deploy --config=$CONFIG keystone --to lxc:1
juju add-relation keystone:shared-db mysql:shared-db

juju deploy --config=$CONFIG glance --to lxc:1
juju add-relation glance:identity-service keystone:identity-service
juju add-relation glance:shared-db mysql:shared-db

juju deploy --config=$CONFIG neutron-api --to lxc:1
juju add-relation neutron-api:amqp rabbitmq-server:amqp
juju add-relation neutron-api:identity-service keystone:identity-service
juju add-relation neutron-api:shared-db mysql:shared-db

juju deploy --config=$CONFIG neutron-gateway --to 3
juju add-relation neutron-gateway:amqp rabbitmq-server:amqp
juju add-relation neutron-gateway:neutron-plugin-api neutron-api:neutron-plugin-api
juju add-relation neutron-gateway:shared-db mysql:shared-db

juju deploy --config=$CONFIG nova-cloud-controller --to lxc:1
juju add-relation nova-cloud-controller:amqp rabbitmq-server:amqp
juju add-relation nova-cloud-controller:identity-service keystone:identity-service
juju add-relation nova-cloud-controller:image-service glance:image-service
juju add-relation nova-cloud-controller:neutron-api neutron-api:neutron-api
juju add-relation nova-cloud-controller:shared-db mysql:shared-db

juju deploy --config=$CONFIG nova-compute --to 2
juju add-relation nova-compute:amqp rabbitmq-server:amqp
juju add-relation nova-compute:cloud-compute nova-cloud-controller:cloud-compute
juju add-relation nova-compute:image-service glance:image-service
juju add-relation nova-compute:shared-db mysql:shared-db

juju deploy --config=$CONFIG neutron-openvswitch
juju add-relation neutron-openvswitch:amqp rabbitmq-server:amqp
juju add-relation neutron-openvswitch:neutron-plugin-api neutron-api:neutron-plugin-api
juju add-relation neutron-openvswitch:neutron-plugin nova-compute:neutron-plugin 
juju deploy --config=$CONFIG cinder cinder-api --to lxc:1
juju add-relation cinder-api:amqp rabbitmq-server:amqp
juju add-relation cinder-api:cinder-volume-service nova-cloud-controller:cinder-volume-service
juju add-relation cinder-api:identity-service keystone:identity-service
juju add-relation cinder-api:image-service glance:image-service
juju add-relation cinder-api:shared-db mysql:shared-db

juju deploy --config=$CONFIG cinder cinder-volume --to 4
juju add-relation cinder-volume:amqp rabbitmq-server:amqp
juju add-relation cinder-volume:shared-db mysql:shared-db
juju add-relation cinder-volume:image-service glance:image-service

juju deploy --config=$CONFIG openstack-dashboard --to 1
juju add-relation openstack-dashboard:identity-service keystone:identity-service

juju deploy --config=$CONFIG heat --to lxc:1
juju add-relation heat:amqp rabbitmq-server:amqp
juju add-relation heat:identity-service keystone:identity-service
juju add-relation heat:shared-db mysql:shared-db
```

And you're done! The whole process should give you an OpenStack cloud
in about 20-30 minutes.

By the way, an exceedingly useful command to watch the installation progress of your Juju environment is:

    watch "juju stat --format=tabular"

* * *

This article originally appeared on the `hastexo.com` website (now defunct).
