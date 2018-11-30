Title: Containers: Just Because Everyone Else is Doing Them Wrong, Doesn't Mean You Have To
Date: 2016-02-21
Slug: containers-just-because-everyone-else
Author: florian
Tags: LXC, Containers, Ubuntu, Ansible
Summary: The recent CVE-2015-7547 vulnerability in glibc exposed a common antipattern in container management. Here's what you can do to avoid it, and instead adopt a container management pattern that will preserve your sanity and enable you to react to critical issues in minutes.


This is a writeup of [a presentation](http://sched.co/3xVu) I did at
LinuxCon Europe in Dublin last year. Since Linux Foundation Events
*still* don't come with video recording for all talks (all they do
record and publish are keynotes), I can't point you to a YouTube link,
though you're certainly welcome to
[peruse my slides]({filename}/articles/resources/presentations/manageable-application-containers.md)
from that talk.


## The problem

Suppose you're an operator who, in a massively scaled-out and highly
automated deployment, is responsible for keeping a few hundred or a
few thousand containers up and running. Your developers put those
together and then basically throw them over the wall for you to
manage. It's your job just to keep them alive, available, and secure;
what's *in* them is your developers' domain. Sure, you have Git repos
you build your containers from, and a Docker registry, so you can
always check what's in which container. You don't get to call the
shots, though.

Suppose further that all most of your containers run some form of web
service. And let's assume, just for the sake of this discussion, that
they're all running Apache, because that's your reference
platform. Your developers may be writing applications in Python or
Ruby or (shudder) PHP, but what all your apps have in common is that
you've settled on Apache as your reference platform. Your developers
can assume that with Apache, you, the ops person, know the boldface
cold, and you can give them an extremely stable, well-tuned platform
to build on.

And then Apache is affected by some disturbing security vulnerability
that you must now fix in record time. Say, something affecting your
core SSL library or maybe even your C library. Sound familiar? Thought
so.


### The fix in a non-containerized world

OK, so you must now fix OpenSSL or libc on all your systems in record
time before the anticipated exploit barrage rolls in. In a world
without containers, you'd rely on your trusted software source
(normally, your distro vendor) to provide you with a fixed package or
packages for the affected libraries. You would then roll those out via
your preferred software management utility, or system automation
facility, or unattended upgrade scheme.

In short, you'd have a tense time until updated packages are
available, but once they are, things get fixed in a matter of minutes.


### But what now?

With the deployment of containers comes, frequently, the notion that
packaging, package management, or dependency tracking is somehow a
terrible idea. Instead, you put everything you need into one container
image, deploy one container per service, and not worry about what a
*different* service running on the same physical hardware might need.

At first glance, that simplifies things. Your developer needs MySQL
configured a certain way, and some other app needs it differently?
Fine, they can put everything in their own separate containers,
binaries, libraries and all, problem solved. Storage is dirt cheap,
containers are efficient and produce little overhead. If they ever
need to change anything, say go from one MySQL point release to
another, then they just rebuild the container, you replace the old
build with the new one, fine.

But now it's not your developer who wants to change things, it's *you*
who needs to deploy a critical fix.[^twitter]

[^twitter]:
	Edit, 2016-02-22: Added Twitter quote from Josh Long.

> so.. using GlibC?
>
> How’s re-imaging all of your
> [@Docker](https://twitter.com/docker) images going?
>
> &mdash; Josh Long (龙之春)
> ([@starbuxman](https://twitter.com/starbuxman)) [February 19,
> 2016](https://twitter.com/starbuxman/status/700591322177019904)

So you set out to rebuild a few hundred containers, or maybe a couple
of thousand, to get the issue fixed. In a perfect environment, you
have access to every build chain, know about every version of every
container in your area of responsibility, can pinpoint exactly which
are affected by the vulnerability, have an automated toolchain to
build and deploy them, have perfect documentation so you don't need to
check back with any of your developers, so it doesn't matter whether
any one is out sick, on vacation, or has left the company since they
deployed one of their, now potentially affected, services.

And of course, everyone works in such a perfect environment. Right?

So now, even *after* a fix to your issue is already available, you
*still* need to scramble to get it deployed, and deploying is *a lot*
more complicated than in a world without containers.


## Is this an inherent problem with containers?

Of course not. The problem isn't with the fact that you're using
containers, or with the specific container technology. **The problem
is that everyone is telling you to use containers a certain way, and
from an operational perspective that way is wrong.** And it's not even
"wrong but still better than all other options", it's just wrong. I
guess you could call it the Docker Fallacy.

That's the bad news. The good news is that there is a way that is
better, saner, and cleaner, and will make your life as an operator
*much* easier, while not being too hard on your developer friends.

## So what's a better way?

You can use containers in a simpler, less flashy, less exciting
&mdash; in short, *better* way.

### Define a core platform, or platforms

Any organization worth its salt will select a handful of distributions
to build products and services on. Maybe it's even just one, but let's
assume you have several, say the latest Ubuntu LTS,[^ubuntu] the
latest CentOS, and the latest Debian. For each of these, you can
define an absolute bare-minimal list of packages. I can almost
guarantee you that none of your developers will care about a single
item on that list. A C library, a shell, an init system, coreutils,
NTP... chances are that you'll run up a list of well over 100 core
system components that *you* will be expected to keep secure; your
developers will take them all for granted.

What *you* can take for granted, thanks to the tireless work of
packagers and distro vendors over years and years, is that you will
get timely security updates for all of those.

[^ubuntu]:
	At the time of writing, the latest Ubuntu LTS is 14.04 "Trusty
	Tahr", which is based on a Linux 3.13 kernel. This Ubuntu stock
	kernel ships with a pre-release version of OverlayFS which
	predates the 3.14 mainline merge. I would not recommend using that
	kernel; instead you'll want to run your hosts with a more recent
	kernel from the
	[LTS Enablement Stack](https://wiki.ubuntu.com/Kernel/LTSEnablementStack). Again
	at the time of writing, this is a Linux 4.2 kernel that ships with
	the `linux-generic-lts-wily` package.


### Deploy your core platforms as often as you need

Deploy these reference systems across your physical hardware. Deploy
as many as you need for all the containers you're expected to run on
each platform. Do so in an automated fashion, so that you never have
to log into any of these systems by hand.


### Use OverlayFS for your containers

[OverlayFS](https://en.wikipedia.org/wiki/OverlayFS) is a union mount
filesystem that ships as part of the mainline kernel. With OverlayFS
you can do a few clever things:

* Use a read-only base filesystem with a writable overlay to create a
  read/write union mount.
* Write to the union mount and only touch the overlay, leaving the
  base filesystem pristine.
* Hide selected content in the base filesystem from the union mount,
  through the use of
  [opaque directories](https://www.kernel.org/doc/Documentation/filesystems/overlayfs.txt).
* Use one base filesystem with multiple overlays to create any number
  of separate read/write union mounts.
* Immediately make updates to the base filesystem known to *all* union
  mounts, by simply remounting them.

This makes OverlayFS extremely powerful when used together with
LXC. You define a bunch of overlay directories &mdash; one for each of
your containers &mdash;, and they can all share one base filesystem:
your host root filesystem.[^automount]

[^automount]:
	LXC containers do present per-container specific content for some
	directories by default, notably `/proc`, `/dev`, and `/sys`. Other
	host-filesystem content can be hidden by creating opaque
	directories in the container overlay; this is what you would
	commonly do for directories like `/root`, `/home`, `/tmp` and
	others.

Then, the union mount becomes your LXC container's root. It
automatically has read access to everything that is available on the
host, unless specifically hidden, and whatever it writes goes to the
overlay. When you discard a container, you delete the overlay.

Here is a minimal example configuration for a container like this:

```ini
# For additional config options, please look at lxc.container.conf(5)
# Common configuration
lxc.include = /usr/share/lxc/config/ubuntu.common.conf
# Container specific configuration
lxc.arch = amd64
# Network configuration
lxc.network.type = veth
lxc.network.link = lxcbr0
lxc.network.flags = up
lxc.network.hwaddr = 00:16:3e:76:59:10
# Automatic mounts
lxc.mount.auto = proc sys cgroup

lxc.rootfs = overlayfs:/var/lib/lxc/host/rootfs:/var/lib/lxc/mytestcontainer/delta0
lxc.utsname = mytestcontainer
```

Note that the LXC userland presently enforces an OverlayFS base
directory to be in a subtree of `/var/lib/lxc`. You can satisfy this
requirement by bind-mounting `/` to `/var/lib/lxc/host/rootfs`, as
shown in the example above.

What this creates, among other things, is crystal-clear separation of
concerns: whatever is in the overlay is for your developers to
decide. They can pull in packages from PyPI, Ruby Gems, NPMs,
whatever. What's in the host root is your responsibility.


### Automate, automate, automate

It's obvious and self-evident, but it doesn't hurt to reiterate: you
want to automate *all* of this. You're certainly free to select your
own tools to do it, but Ansible specifically has very good LXC
container support so it makes this a breeze.

Here's a simple Ansible playbook example that creates 100 containers,
all based off your host root.[^ansible]

[^ansible]:
	Please note that it's not *quite* as simple as shown in the
    Ansible example. You will want to provide some additional tweaks,
    such as added mounts or opaque directories. I've tried to keep the
    example brief to illustrate the concept.

```yaml
- hosts: localhost
  tasks:
    - name: Create a local bind mount for the host root filesystem
      mount:
        name: /var/lib/lxc/host/rootfs
        src: /
        opts: bind
        fstype: none
        state: mounted
    - name: Create a template container using the host root
      lxc_container:
        name: host
        state: stopped
        directory: /var/lib/lxc/host/rootfs
        config: /var/lib/lxc/host/config
        container_config:
          - "lxc.mount.auto = proc sys cgroup"
          - "lxc.include = /usr/share/lxc/config/ubuntu.common.conf"
    - name: Create 100 OverlayFS based containers
      lxc_container:
        name: host
        backing_store: overlayfs
        clone_snapshot: true
        clone_name: "mytestcontainer{{ item }}"
        state: started
      with_sequence: count=100
```

Now of course, this will also mean that you'll need to get your
developers to define their container config in Ansible. However, that
is fundamentally a *good* thing, because it means that developers and
operations people will be reading and writing the same language. Also,
if your developers can write a Dockerfile, they won't have a hard time
with Ansible YAML either.


## How does this help?

With this approach, think of what you now have to do to make hundreds
of containers running on the same box get a new libc.

1. Update your host libc.
2. Restart your containers.

That's it. That is literally all you have to do to update hundreds of
containers in one fell swoop. LXC will remount your OverlayFS on
container restart, and thus all changes to the host will be
immediately visible in the container's overlay filesystem.

On an Ubuntu platform, you could even go so far as automating this in
conjunction with unattended upgrades:

```perl
# /etc/apt/apt.conf.d/50unattended-upgrades
// Automatically upgrade packages from these (origin:archive) pairs
Unattended-Upgrade::Allowed-Origins {
	"${distro_id}:${distro_codename}-security";
};
```

```perl
# /etc/apt/apt.conf.d/05lxc
DPkg::Post-Invoke      { "/sbin/service lxc restart"; };
```

So there you have it. Upgrade loads of containers in minutes. No
rebuild, no redeploy, nothing. Packaging actually does work and has
merit, regardless of what the hipster crowd is trying to sell you.
* * *

This article originally appeared on my blog on the `hastexo.com` website (now defunct).
