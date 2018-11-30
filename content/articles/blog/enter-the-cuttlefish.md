Title: Enter the cuttlefish!
Date: 2013-05-07 07:43
Slug: enter-the-cuttlefish
Author: florian
Tags: Ceph

Today, the developers released Ceph 0.61, codenamed cuttlefish. There
are some interesting features in this new release, take a look.

One thing that will undoubtedly make Ceph a lot more palatable to
RHEL/CentOS users is the **availability of Ceph in EPEL**. This was
[originally announced in late
March](http://www.inktank.com/ceph/ceph-is-in-epel-and-why-red-hat-users-should-care/),
but 0.61 is the first supported release that comes with Red Hat
compatible RPMs. Note that at the time of writing, EPEL is obviously
[still stuck on the 0.56 bobtail
release](http://dl.fedoraproject.org/pub/epel/testing/6/x86_64/), but it
is expected that cuttlefish support will follow shortly. In the interim,
cuttlefish packages are available outside EPEL, [on the ceph.com yum
repo](http://ceph.com/docs/master/install/rpm/).

This allows you to run a Ceph cluster on RHEL/CentOS. It does, however
come with a few limitations:

-   You can't use RBD from a kvm/libvirt box that is running RHEL. RHEL
    does not ship with librados support enabled in the qemu-kvm builds,
    and removing this limitation would mean for third parties to provide
    their own libvirt/kvm build. As of today, tough, no RBD-support
    libvirt/kvm lives in [CentOS
    Plus](http://wiki.centos.org/AdditionalResources/Repositories/CentOSPlus).
-   You can't use the kernel rbd or ceph modules from a client that is
    running RHEL. RBD and Ceph filesystem support is absent from RHEL
    kernels.

I'm curious to see if and when that will change, given Red Hat's [focus
on
GlusterFS](http://www.gluster.org/2013/05/glusterfs-is-ready-for-openstack/)
as their preferred distributed storage solution. It will be interesting
to see what happens there.

Another neat little new feature is the ability to **set quotas on
pools,** which is something that we've frequently had customers ask for
in our consulting practice.

Then there are **incremental snapshots for RBD,** another really handy
feature for RBD management in cloud solutions like
[OpenStack](https://www.hastexo.com/knowledge/openstack).

There's more, and you may head over to the press release and the Inktank
blog for more details. And then you might want to mark your calendars
for one of the following events:

-   At the [OpenStack DACH
    Day](https://www.hastexo.com/resources/news-releases/der-openstack-dach-tag-2013-das-erste-ganzt%C3%A4gige-event-der-openstack-communi)
    at [LinuxTag in Berlin on May
    24](http://www.linuxtag.org/2013/de/program/program/freitag-24-mai-2013/open-stack.html),
    Wolfgang Schulze from Inktank gives an overview about Ceph (in
    German, [register
    here](http://www.eventbrite.com/e/openstack-dach-day-2013-tickets-3206509757)).
-   At [OpenStack Israel](http://www.openstack-israel.org/) on May 27,
    I'll be speaking about Ceph integration with OpenStack (in English,
    [register here](http://www.meetup.com/IGTCloud/events/99146542/)).
-   And at [OpenStack CEE](http://openstackceeday.com/) on May 29 in
    Budapest, Martin speaks about *Scale-out Made Easy: Petabyte Storage
    with Ceph* (in English, [register
    here](http://www.eventbrite.com/e/openstack-cee-day-2013-budapest-registration-5634033546)).

All these events are expected to sell out beforehand, and they are only
a couple of weeks away. So make sure you grab your seat, and we'll see
you there!


* * *

This article originally appeared on my blog on the `hastexo.com` website (now defunct).
