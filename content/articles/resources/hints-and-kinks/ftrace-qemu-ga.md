Title: Using ftrace to trace function calls from qemu-guest-agent
Date: 2019-08-21
Slug: ftrace-qemu-ga
Tags: libvirt, Linux, ftrace, Qemu

When you are using functionality that is buried deep in the Linux
kernel, [`ftrace`](https://en.wikipedia.org/wiki/Ftrace) can be
extremely useful. Here are some suggestions on how to use it, using
the example of tracing function calls from `qemu-guest-agent`.

<!--break-->

## What’s this about?

Recently I used, for the first time,
**[libvirt](https://libvirt.org/)’s functionality to indicate to a
virtual guest that it is about to have a point-in-time copy of its
disks — a *snapshot* — taken.** In doing so, it can tell the virtual
machine (VM) to freeze I/O on all its mounted filesystems. 

The rationale behind this is, I hope, obvious: you want the VM to
momentarily stop I/O to its virtual disks, so that you can take a
snapshot when no I/O is in-flight, and the snapshot image can thus be
expected to be internally consistent. The snapshot itself will only
take a second or so, and the minor interruption is a small price to
pay for the added consistency guarantee you get.

You might be wondering how this works and it is, indeed, a bit
involved.

* First, you’ll need a **virtual serial console** that allows the
  hypervisor (in the host) to communicate with the guest. This will be
  defined [in your libvirt domain
  XML](https://wiki.libvirt.org/page/Qemu_guest_agent#Setting_QEMU_GA_up),
  and in [OpenStack Nova](https://docs.openstack.org/nova/latest/),
  this automatically pops up if you are booting your instance off an
  image [which has the `hw_qemu_guest_agent=yes` property
  set](https://docs.openstack.org/nova/rocky/admin/configuration/hypervisor-kvm.html#guest-agent-support).

* Then, you’ll need a **daemon** within the guest that listens for
  commands received over the serial port. This daemon is called
  `qemu-guest-agent`, or `qemu-ga` for short. All you’ll need for it
  to run is to install the package of that name, which you can do in
  various ways (`apt-get install qemu-guest-agent` being the simplest,
  on Ubuntu guests).

* One of the many commands that said daemon supports is
  [`guest-fsfreeze-freeze`](https://git.qemu.org/?p=qemu.git;a=blob;f=qga/commands-posix.c;h=dfc05f5b8ab958ef43aca36258e151ee2525ebf5;hb=33f18cf7dca7741d3647d514040904ce83edd73d#l2746). When
  it receives that command over the virtual serial link, the daemon
  will [loop over your mounted
  filesystems](https://git.qemu.org/?p=qemu.git;a=blob;f=qga/commands-posix.c;h=dfc05f5b8ab958ef43aca36258e151ee2525ebf5;hb=33f18cf7dca7741d3647d514040904ce83edd73d#l1295),
  and issue the [**`FIFREEZE`
  ioctl**](https://elixir.bootlin.com/linux/v5.2/source/fs/ioctl.c#L668)
  on all of them. This happens in reverse order, meaning your root
  (`/`) filesystem is frozen last.

* That ioctl then calls the [**`freeze_super()` kernel
  function**](https://elixir.bootlin.com/linux/v5.2/source/fs/super.c#L1694),
  which flushes each filesystem’s superblock, blocks (“freezes”) all
  new I/O to the filesystem, and syncs (flushes) all I/O that is
  currently in flight on that filesystem.
  
The combined net effect of all of the above is that you get a virtual
machine that is temporarily read-only, with pending I/O piling up,
until you are done taking your snapshot. When that happens, there are
a few more actions that happen:

* The hypervisor sends the `guest-fsfreeze-thaw` command over the
  virtual serial link.  Now, the daemon will [loop over all your
  mounted filesystems
  again](https://git.qemu.org/?p=qemu.git;a=blob;f=qga/commands-posix.c;h=dfc05f5b8ab958ef43aca36258e151ee2525ebf5;hb=33f18cf7dca7741d3647d514040904ce83edd73d#l1374),
  and issue the [**`FITHAW`
  ioctl**](https://elixir.bootlin.com/linux/v5.2/source/fs/ioctl.c#L672)
  on them. This time, it is taking the mounts in forward order,
  thawing the root filesystem first.

* That ioctl then calls the [**`thaw_super()` kernel
  function**](https://elixir.bootlin.com/linux/v5.2/source/fs/super.c#L1798),
  which unblocks (“thaws”) all new I/O to the filesystem, and allows
  the VM to continue normal operations.

Now there’s a bit of an issue with that. All of the aforementioned
kernel functions only write `printk`’s [on
error](https://elixir.bootlin.com/linux/v5.2/source/fs/super.c#L1737),
but they don’t tell you when they succeed. So you can try a snapshot,
then type `dmesg` in the guest, and you’ll have no way of telling
whether the whole freeze/thaw dance succeeded, or was never even
attempted.

But fear not, there’s a way that you can trace exactly what the kernel
is doing!

## tracefs, and configuring `ftrace`

If your guest runs any modern kernel, then chances are that it will,
by default, mount a virtual **tracefs filesystem** to the
`/sys/kernel/debug/tracing` mount point (although as of kernel 4.1,
this is nominally an alias, with `/sys/kernel/tracing` being the
canonical mount point). Regardless of its path, tracefs exposes [the
kernel’s `ftrace`
functionality](https://www.kernel.org/doc/Documentation/trace/ftrace.txt).

So the first thing you’ll tell ftrace, in your guest VM, is the
process for which you’ll want to do function tracing. In our case,
that’s your guest’s `qemu-ga`. So, you can do:

```bash
pidof qemu-ga > /sys/kernel/debug/tracing/set_ftrace_pid
```

Then, you’ll want to instruct `ftrace` to trace kernel function calls:

```bash
echo "function" > /sys/kernel/debug/tracing/current_tracer
```

And, you’ll want to make sure that we don’t trace only function calls
from `qemu-ga` itself, but also from its child processes:

```bash
echo "function-fork" > /sys/kernel/debug/tracing/trace_options
```


## Let’s see what’s happening!

Now you have a guest that’s properly instrumented for tracing kernel
function calls that originate with `qemu-ga`. So now, go ahead and
take a snapshot. On OpenStack Nova, you’d do that with:

```bash
openstack server image create --name <image-name> <instance-name>
```

Then, shell back into your guest, and interrogate your trace for
`ioctl` calls:

```bash
grep -E '(freeze|thaw)_super.*ioctl' /sys/kernel/debug/tracing/trace
```

And voilà:

```
         qemu-ga-14574 [001] ....   264.059109: freeze_super <-do_vfs_ioctl
         qemu-ga-14574 [001] ....   265.837955: thaw_super <-do_vfs_ioctl
         qemu-ga-14574 [001] ....   265.855048: thaw_super <-do_vfs_ioctl
         qemu-ga-14574 [001] ....   265.855084: thaw_super <-do_vfs_ioctl
```

So that’s the `FIFREEZE` ioctl that maps to `freeze_super()`, and the
`FITHAW` ioctl that maps to `thaw_super()`. And that’s how you know that
your guest is freezing and thawing I/O as you expect it to!

## Where to go from here

Feel free to dig further into your `trace` file (`cat` or `less` will
help), and play with other `ftrace` options. There’s a massive amount
of things you can do with it, as [the
documentation](https://www.kernel.org/doc/Documentation/trace/ftrace.txt)
explains. You’ll probably also find [this blog
post](https://jvns.ca/blog/2017/03/19/getting-started-with-ftrace/)
from [Julia Evans](https://twitter.com/b0rk) useful for exploring
`ftrace`.

Also, thank [Steven Rostedt](https://twitter.com/srostedt) when you
see him! He is the primary author of the ftrace framework.
