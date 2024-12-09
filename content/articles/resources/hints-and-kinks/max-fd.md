Title: Exploding memory usage in Django/uWSGI containers
Date: 2024-12-07 09:00
Slug: max-fd
Tags: Kubernetes, Django, Containers, systemd
Summary: We recently came across an interesting problem at work while migrating from one flavor of Kubernetes to another. It's sufficiently obscure to merit a brief write-up for reference.

When running [Open edX](https://openedx.org/) on [Kubernetes](https://kubernetes.io) clusters, one of its [Pods](https://kubernetes.io/docs/concepts/workloads/pods/) is the `lms` Pod, which runs the core of the Open edX Learning Management System ([LMS](https://github.com/openedx/edx-platform/tree/master/lms)).

This is a relatively complex [Django](https://www.djangoproject.com/) application, which runs in the Pod's sole container.
Said Django application is being launched with [uWSGI](https://uwsgi-docs.readthedocs.io/).

At work, we had previously run this platform on Kubernetes clusters managed with [OpenStack Magnum](https://docs.openstack.org/magnum/), and were in the process of migrating to [Gardener](https://gardener.cloud/).
Apart from the fact that we were upgrading to a newer Kubernetes release, this also meant that the base operating system of our Kubernetes worker nodes changed from [Fedora CoreOS](https://fedoraproject.org/coreos/) to [Garden Linux](https://github.com/gardenlinux/gardenlinux) (which is effectively a Kubernetes-optimised Debian).
The virtualisation platform underpinning the Kubernetes cluster remained the same ([OpenStack](https://docs.openstack.org/)).

Mid-migration, we suddenly noticed that our cluster was [oom-killing](https://en.wikipedia.org/wiki/Out_of_memory#Recovery) our `lms` pods.
Now this shouldn't happen, for the following reasons:

* Normally, Kubernetes only kills a Pod for excessive memory usage when a [memory limit](https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/) is set on that Pod, which wasn't the case.
* Otherwise (that is, with no memory limit set), Pods get killed only by the "regular" kernel oom-killer, and that should only happen when the Pod is grossly misconfigured — that is, its actual memory usage far exceeds its configured [memory request](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits).

We quickly found out (via `kubectl top pod`) that we were dealing with the latter of these two: our `lms` Pod was consuming a whopping 8 GiB of memory when running on the Gardener-managed cluster — nearly 4 times the memory request of 2 GiB.

This had us scratching our heads, for on the Magnum-managed cluster it was previously running on, that same pod had typically consumed only 80-120 MiB of memory (with occasional spikes).
Thus, we were dealing with baseline memory usage that had suddenly increased by two orders of magnitude.

Now to explain this memory usage jump, you'll need this background information:

1. The `corerouter` plugin in uWSGI maintains an array of file descriptor references.
2. The size of this array, and with it its memory usage, is a multiple of the value set for uWSGI's `max-fd` configuration option.[^corerouter]
3. If `max-fd` has not been set in the uWSGI configuration, its default is the maximum number of open file handles allowed for the process per the system-wide configuration.
4. Said default can be defined by the `nofiles` [ulimit](https://www.man7.org/linux/man-pages/man5/limits.conf.5.html), or a [cgroups](https://wiki.archlinux.org/title/Cgroups) restriction.
   A cgroups restriction is also what systemd uses to implement [the `LimitNOFILE` option](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#Process%20Properties), which can be set on any systemd unit.[^man-outdated]
5. If neither the ulimit nor a cgroups restriction is in place, [the `fs.nr_open` sysctl](https://www.kernel.org/doc/Documentation/sysctl/fs.txt), if set, acts as a backstop. 

[^corerouter]: See [the source](https://github.com/unbit/uwsgi/blob/master/plugins/corerouter/corerouter.c#L705), which at the time of writing reads:
  ```
  ucr->cr_table = uwsgi_malloc(sizeof(struct corerouter_session *) * uwsgi.max_fd);
  ```

[^man-outdated]: As far as I can tell, at the time of writing the table captioned "Resource limit directives" in the `systemd.exec` man page is outdated and incorrect as far as `LimitNOFILE`'s default is concerned, and also the "Don't use" admonition seems misguided at this point.

Prior to release 256, systemd effectively [bumped the default](https://github.com/systemd/systemd/pull/29322) for `LimitNOFILE` from 1048576 (2²⁰) to `infinity`, which meant that rather than setting its own cgroups limit, it would rely on `fs.nr_open`.
And *that* value was recently upped in some distributions to 1073741824 (2³⁰) — an increase by a factor of 2¹⁰ or 1024 over the previously applicable value.

This change was also applied on Debian (which Garden Linux is based on), and it was even [discussed on the Debian mailing list](https://lists.debian.org/debian-devel/2024/06/msg00041.html) — where ironically, concerns about raising this limit were pre-emptively quashed with the assertion that file descriptors are such an "extremely cheap resource" that it does not hurt to allow absurdly high numbers of them.

In the uWSGI case, however, this had the somewhat devastating effect of increasing memory usage to insane levels.

To their credit, the Garden Linux developers identified this flaw (which, to my knowledge was baked into their version 1592.2), and [fixed it](https://github.com/gardenlinux/gardenlinux/pull/2442) in version 1592.3.
Still, to insulate ourselves from further such issues, we have opted to [reconfigure our systems](https://uwsgi-docs.readthedocs.io/en/latest/Configuration.html) to run uWSGI with an explicitly defined `max-fd` option, set to the prior system-wide default of 1048576 (although setting it to something as low as 1024 would *probably* work too). 

### Acknowledgements

[Lothar Bach](https://github.com/lotharbach), [Brennan Kinney](https://github.com/polarathene), [Piotr Kucułyma](https://github.com/pkdevpl), [Namrata Sitlani](https://github.com/NamrataSitlani), and [Maari Tamm](https://github.com/mrtmm) all contributed to the findings discussed in this article.[^order]

[^order]: I've listed these individuals in alphabetical order by surname.
