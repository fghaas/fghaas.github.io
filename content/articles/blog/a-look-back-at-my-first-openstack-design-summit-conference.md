Title: A look back at my first OpenStack Design Summit & Conference
Date: 2012-04-24 09:35
Slug: a-look-back-at-my-first-openstack-design-summit-conference
Author: florian
Tags: Conference, OpenStack

I've just returned from the [OpenStack Folsom Design Summit and Spring
2012
Conference](http://www.openstack.org/conference/san-francisco-2012/),
and am finally getting rid of my jet lag. Here's a summary of what's
been a mind-blowing conference experience for me.

<!--break--><!--break-->

This was my first OpenStack Design Summit and Conference. And as anyone
who's in open source is acutely aware, some communities can be reluctant
to accept newcomers. Some may even seem outright hostile to the timid.
Not the [OpenStack](http://www.openstack.org/community) community.

The minute I sat down in the opening session of the Design Summit on
Monday, I felt instantly welcome and at home. Even as a relative
OpenStack newbie (who was invited to the Design Summit to provide some
insights and guidance on high availability), I immediately got the
impression that I was in the right place at the right time. I've rarely
seen a developer community on such a positive vibe. Sure, we'll blast
each other on technical disagreements, but all in a good-natured, fun
way.

[My own Design Summit
session](http://folsomdesignsummit2012.sched.org/event/fa2a5803a4b4ba857db57c84a1e1d3bc)
clearly wasn't without such disagreements, and expectedly so. But I
think we came to some excellent conclusions:

-   Infrastructure high availability will be an overarching design goal
    in the upcoming OpenStack Folsom release.
-   We will shoot for providing HA solutions for all OpenStack
    infrastructure services. This includes MySQL, RabbitMQ, Glance,
    Keystone, Nova and Horizon (Swift already has HA built in). hastexo
    will play a very active role in this.
-   We will not reinvent the wheel, and instead rely on [the Pacemaker
    stack](http://clusterlabs.org/) wherever possible.
-   Most of the challenge is really in the documentation and in the
    development of reference solutions that deployment solutions
    ([Juju](https://jujucharms.com/), [Chef](https://www.chef.io/chef/),
    [Puppet](https://puppetlabs.com/)) can then build on. We will take a
    lot of responsibility in that effort, as well.
-   Some services still require some work to become fully HA capable.
    Cinder (the volume service that's being factored out of Nova for
    Folsom) is one example, Quantum is another. This work will be
    tackled.
-   We're currently planning to stop short of providing monitoring and
    HA for Nova instances (a.k.a. *guest HA*). This is on the list for
    the next release past Folsom.

With those issues discussed, voted on and on the record, I had the honor
of [presenting them to a larger audience at the main
conference](http://openstackconferencespring2012.sched.org/event/a6d940d2ebd11e37c6ac389f7d4d2125).
It seems to have hit home pretty well, based on feedback from attendees
given in-person and on Twitter. <span
style="text-decoration: line-through;">I'm hoping the conference
organizers will make a video recording available shortly. Meanwhile, my
presentation is already available
[here](https://prezi.com/gxaohiwl46z2/high-availability-in-openstack/).</span> [It's
now available here in the *Presentations*
section.](https://www.hastexo.com/resources/presentations/reliable-redundant-resilient-high-availability-openstack)

Overall, this has been a wonderful and very well organized conference,
and I'm very much looking forward to coming back next time around.

* * *

This article originally appeared on my blog on the `hastexo.com` website (now defunct).
