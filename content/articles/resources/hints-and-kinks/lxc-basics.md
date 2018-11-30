Title: Running (Almost) Anything in LXC: The Basics 
Date: 2020-12-28
Slug: lxc-basics
Series: Running (Almost) Anything in LXC
Series_index: 0
Tags: LXC


LXC is part of my standard Linux desktop toolbox, and I use it
daily. I have done tutorials about this before, one of which you can
find [on YouTube](https://youtu.be/3nUbMREnnns) (courtesy of
[linux.conf.au](https://linux.conf.au/)) and
[GitHub](https://fghaas.github.io/lca2018-lxc/#/1), but it’s about
time I included this in a series of articles.

My motivations for running LXC containers are manifold, but here are
some of the most important ones:

* I want to keep my main system clean of anything that’s not free and
  open source software. There is, however, the odd bit of non-free
  software that I do need to or want to use — Zoom for work, for
  example, or the excellent Spotify Linux client for pleasure.

* Even if a piece of Software *is* open source, it sometimes does not
  play nicely with the version of my main system that I currently
  use. A recent example is the somewhat premature inclusion of
  pre-release versions of Calibre in Debian and Ubuntu, which means
  that Calibre is currently not playing too nicely on Ubuntu Focal
  (the current LTS at time of writing), but runs just dandy on Bionic,
  which I can handily run in an LXC container.

* Sometimes the opposite is true as well, that is, some application
  comes in a version that I want to use, except it’s only bundled with
  a future Ubuntu (or Debian) release that I am not yet prepared to
  use. Or else, it’s available only on Fedora or openSUSE, which are
  perfectly fine desktop distributions but just not my preferred ones
  to use on a daily basis. In that case, LXC containers are
  exceedingly useful as well, and are much less hassle than building
  the application in question from source.


Here are my general rules for running LXC containers:

1. I run my containers as non-root, under my own user account. (If you
   are unfamiliar with this, and would like to learn more about how it
   works and how you need to tweak your system to enable it, please
   see the excellent LXC [Getting
   Started](https://linuxcontainers.org/lxc/getting-started/#creating-unprivileged-containers-as-a-user)
   guide.)
2. I use UID and GID mapping rules so that all of the container’s user
   accounts, including the container’s root, are mapped to subgids and
   subuids of my account — all **except** my own user account and
   group, with uid and gid 1000.
3. I bind-mount the `/home` directory into the container. Combined
   with the uid and gid passthrough of my own account, this means that
   `florian` in the container can access `/home/florian` in any
   container, just like in the host.
4. I run all my containers in btrfs subvolumes.
5. I maintain a basic container configuration for each Ubuntu release
   I run, and then I duplicate that configuration for a bunch of
   containers using snapshot cloning (`lxc-copy -s`), which in
   combination with btrfs makes the clones quite space-efficient.

For example, this is the “container specific configuration” section in
`~/.share/lxc/focal/config`, the configuration for my current base
container running Ubuntu Focal:

```ini
# Container specific configuration
lxc.include = /etc/lxc/default.conf
lxc.idmap = u 0 100000 1000
lxc.idmap = g 0 100000 1000
lxc.idmap = u 1000 1000 1
lxc.idmap = g 1000 1000 1
lxc.idmap = u 1001 101001 64535
lxc.idmap = g 1001 101001 64535
lxc.mount.auto = proc sys cgroup
lxc.rootfs.path = btrfs:/home/florian/.local/share/lxc/focal/rootfs
lxc.uts.name = focal
lxc.mount.entry = /home home none bind,optional 0 0
```

Of this, perhaps the `lxc.idmap` settings merit a bit of extra
explanation:

* `lxc.idmap = u 0 100000 1000` means “map the uid 0 (`root`) in the
  container to uid 100000 in the host, and continue up until you’ve
  hit 1,000 mappings”. In other words, map uids 0 to 999 including, to
  100000 to 100999.
* `lxc.idmap = u 1000 1000 1` means “map the uid 1000 in the container
  to uid 1000 in the host,” (in my case, my user account named
  `florian`) “and follow this pattern for just one mapping”. In other
  words, make uid 1000 a pass-through.
* Finally, `lxc.idmap = u 1001 101001 64535` means “starting with uid
  1001 in the container, map it to uid 101001 in the host and proceed
  until you’ve hit 64,535 mappings”.
  
So in total, that’s LXC-ese for “map all possible uids from 0 to 65535
in the container to host subuids shifted by 100,000 *except* 1000,
which you shouldn’t map to any subuid. And the same is true for gids,
for the `g` idmaps. It’s a rather roundabout way of specifying this,
but it works.

Now by itself, this already gives me plenty of options for
command-line applications. But since it’s my main workstation that I
run this on, I usually want my applications to be wired up to my
desktop GUI. More on that in the next installment of the series.
