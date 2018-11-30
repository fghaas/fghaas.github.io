Title: High Availability in OpenStack
Date: 2012-03-21 13:08
Slug: high-availability-in-openstack
Author: florian

A few thoughts on high availability features (or the current absence
thereof) in OpenStack.

I've just proposed a session for the [OpenStack Folsom design
summit](http://wiki.openstack.org/Summit/Folsom) which [Jay
Pipes](http://www.joinfu.com/) was nice enough to invite me to
(thanks!), and I thought I'd write up a few thoughts of mine ahead of
time to get the discussion started.

A little while back, Tristan van Bokkem [started a discussion on high
availability for
Nova](http://www.mail-archive.com/openstack@lists.launchpad.net/msg07495.html)
on the OpenStack mailing list. So in Nova specifically, there are a few
components where high availability is readily available; you just have
to use it.

-   MySQL. That's a no-brainer. [MySQL HA with
    Pacemaker](https://www.hastexo.com/resources/presentations/zen-pacemaker)
    has been done so many times that I won't rehash it here. What's nice
    in this regard is that
    [Galera](http://galeracluster.com/products/mysql_galera) (included
    in [Percona XtraDB
    Cluster](http://www.percona.com/software/percona-xtradb-cluster))
    now promises to do away with the limitations of both
    [DRBD](https://www.hastexo.com/drbd) and traditional [MySQL
    replication](http://dev.mysql.com/doc/refman/5.6/en/replication.html),
    and provide multiple-node, multiple-master *synchronous* replication
    for MySQL. As I'm sure you're aware, classic MySQL replication isn't
    synchronous, and DRBD can't do multi-node master-master, but the
    Galera based solution looks promising, [if not as mature as the
    other
    two](http://www.percona.com/blog/2012/01/09/announcement-of-percona-xtradb-cluster-alpha-release/).
    Of course, I don't understand why the Galera folks had to reinvent
    not only replication (which makes sense) but also cluster membership
    and management (which doesn't), but that's a different discussion to
    be had altogether.
-   RabbitMQ. Has somewhat similar HA considerations as MySQL. A
    Pacemaker/DRBD-based solution [exists, but is considered deprecated
    by the RabbitMQ
    maintainers](http://www.rabbitmq.com/pacemaker.html). Enter
    [mirrored queues,](http://www.rabbitmq.com/ha.html) where again the
    developers seemingly threw out the baby with the bath water and
    rather than just reimplementing replication (sensible), they came up
    with their own cluster manager (questionable). Their mirrored queues
    would probably have played very nicely with master/slave sets in
    Pacemaker.

As Tom Ellis [pointed out in another
email](http://www.mail-archive.com/openstack@lists.launchpad.net/msg07595.html)
the previously mentioned thread, there are more HA considerations for
services in Nova proper.

-   nova-volume still has a lot of work to do. It has an iSCSI
    [driver](http://nova.openstack.org/api/nova.volume.driver.html)
    which can of course be used as an iSCSI proxy pointed at a highly
    available, potentially DRBD-backed, software iSCSI target. Or at an
    iSCSI based hardware solution that has HA built-in, such as HP
    LeftHand. Alternatively, we could just operate on RBD volumes (part
    of
    [Ceph](https://www.hastexo.com/blogs/florian/2012/03/08/ceph-tickling-my-geek-genes))
    which will also take care of redundancy for us, and add seamless
    scaleout and remirroring. That being said, there is currently no
    real HA provision for the nova-volume service itself, and that's
    something that will be required.
-   Compute nodes can all run their own instance of nova-api.
-   Front-end API servers can all run nova-scheduler, with a load
    balancer in front of them.

The
[Pacemaker](https://www.hastexo.com/knowledge/high-availability/pacemaker)
stack has the potential of being a nice fit for most of the above. It
comes with [iSCSI target
support](http://linux-ha.org/doc/man-pages/re-ra-iSCSITarget.html) (RBD
doesn't need Pacemaker on the server end, as Ceph takes care of its own
HA). Pacemaker also ties in directly with upstart, so any upstart job
can be monitored as a Pacemaker service. And Pacemaker's [clone
facility](http://clusterlabs.org/doc/en-US/Pacemaker/1.1/html/Pacemaker_Explained/s-resource-clone.html "Don't balk at the XML! That's Pacemaker's reference documentation; any sane person would use the crm shell to manage Pacemaker resources in real life.")
makes it easy to run multiple instances of inherently stateless services
with minimal configuration. What's more, Pacemaker comes with full
integration for the [ldirectord](http://horms.net/projects/ldirectord/)
load-balancing service. Of course, Pacemaker adds a reliable
communications layer
([Corosync](https://www.hastexo.com/knowledge/high-availability/corosync))
and a multi-master, self-replicating configuration facility.

As for non-Nova Openstack services, Glance could use some Pacemaker
integration (not hard to do; it's just that someone has to do it).

Ceph, in my opinion, has the very interesting potential of being a
redundant, scalable storage one-stop shop for OpenStack. It serves the
purposes of both volume/block storage (with RBD) and object storage
(with RADOS/radosgw). And, as already pointed out, it comes with HA,
replication, and scalability built-in.

Comments and feedback on the above are much appreciated. For OpenStack
developers who visit this blog for the first time: you need to login to
post comments in our effort to combat comment spam – but you can simply
use your Launchpad OpenID to do so.



* * *

This article originally appeared on my blog on the `hastexo.com` website (now defunct).
