Title: Exploding memory usage in Django/uwsgi containers
Date: 2024-06-05 21:00
Slug: max-fd
Summary: A tale of innocent assumptions made by developers, and how those can bit you.

We recently came across an interesting problem at work while migrating from one flavor of Kubernetes to another.
It's sufficiently obscure to merit a brief write-up for reference.

We run [Open edX](https://openedx.org/) on [Kubernetes](//kubernetes.io) clusters.
One of the Pods that a thus-managed Open edX platform consists of is the `lms` Pod, which runs the core of the Open edX Learning Management System ([LMS](https://github.com/openedx/edx-platform/tree/master/lms)).

This is a relatively complex [Django](https://www.djangoproject.com/) application, which runs in the Pod's sole container.
Said Django application is being launched with [uWSGI](https://uwsgi-docs.readthedocs.io/).

Now, we had previously run this on Kubernetes clusters managed with [OpenStack Magnum](https://docs.openstack.org/magnum/), and were in the process of migrating to [Gardener](https://gardener.cloud/).
Apart from the fact that we were upgrading to a newer Kubernetes release, this also meant that the base operating system of our Kubernetes worker nodes changed from [Fedora CoreOS](https://fedoraproject.org/coreos/) to [Garden Linux](https://github.com/gardenlinux/gardenlinux) (which is effectively a somewhat Kubernetes-optimized Debian).
The virtualisation platform underpinning the Kubernetes cluster remained the same ([OpenStack](https://docs.openstack.org/)).

Mid-migration, we suddenly noticed that our cluster was oom-killing our `lms` pods.
Now this shouldn't happen, for the following reasons:

* Normally, Kubernetes only kills a Pod for excessive memory usage when a [memory limit](https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/) is set on that Pod, which wasn't the case.
* Otherwise (that is, with no memory limit set), Pods get killed only by the "regular" kernel oom-killer, and that should only happen when the Pod is grossly misconfigured (that is, its [memory request](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) does not at all reflect its actual memory usage).

We quickly found out (via `kubectl top pod`) that we were dealing with the latter of these two: our `lms` Pod was consuming a whopping 8 GiB of memory when running on the Gardener-managed cluster — nearly 4 times the memory request of 2 GiB.

This had us scratching our heads, for on the Magnum-managed cluster it was previously running on, that same pod had typically consumed only 80-120 MiB of memory (with occasional spikes).
Thus, we were dealing with baseline memory usage that had suddenly increased by two orders of magnitude.

Now to explain this memory usage jump, you'll need this background information:

1. The `corerouter` plugin in `uwsgi` maintains an array of file descriptor references.
2. The size of this array, and with it its memory usage, is a multiple of the value set for `uwsgi`'s `max-fd` configuration option.[^corerouter]
3. If `max-fd` has not been set in the `uwsgi` configuration, its default is the maximum number of open file handles allowed for the process per the system-wide configuration.
4. Said default can be defined by the `nofiles` ulimit, or a cgroups restriction.
   A cgroups restriction is also what systemd uses to implement the `LimitNOFILES` option, which can be set on any systemd unit.
5. If neither the ulimit or a cgroups restriction is in place, the `fs.nofiles` sysctl, if set, acts as a backstop. 

[^corerouter]: See [the source](https://github.com/unbit/uwsgi/blob/master/plugins/corerouter/corerouter.c#L705), which at the time of writing reads:
  ```
  ucr->cr_table = uwsgi_malloc(sizeof(struct corerouter_session *) * uwsgi.max_fd);
  ```

Crucially, systemd made an interesting decision earlier this year:
it bumped the default for `LimitNOFILES` from 1048576 (2²⁰) to 1073741824 (2³⁰) — an increase by a factor of 2¹⁰ or 1024. 

This change was also applied on Debian (which Garden Linux is based on), and it was even discussed on the Debian mailing list — where ironically, concerns about raising this limit were quashed with the assertion that file descriptors are such a cheap resource that it does not hurt to allow absurdly high numbers of them.

In the `uwsgi` case, however, this had the somewhat devastating effect of increasing memory usage to insane levels.

To their credit, the Garden Linux developers identified this flaw (which, to my knowledge was baked into their version 1592.2), and fixed it in version 1592.3.
Still, to insulate ourselves from further such issues, we have opted to reconfigure our systems to run `uwsgi` with an explicitly defined `max-fd` option, set to the prior system-wide default of 1048576 (although setting it to something as low as 1024 would *probably* work too). 
