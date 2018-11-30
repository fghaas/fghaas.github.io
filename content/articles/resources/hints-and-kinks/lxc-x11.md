Title: Running (Almost) Anything in LXC: X applications
Date: 2021-01-09
Slug: lxc-x11
Series: Running (Almost) Anything in LXC
Series_index: 1
Tags: LXC

I occasionally want to run X applications in an LXC
container. Sometimes that’s because they’re not open source and I need
to run them for work, like Zoom. Sometimes it’s an open source X
application that doesn’t work splendidly well on the Ubuntu release
that I am using.

It turns out that this isn’t particularly hard to do — **if you are
running X.org.** To the best of my knowledge, what I am describing
here cannot be expected to work, reliably, on Wayland. To me that’s no
big loss, because there are several other things that I like to use
(like [Autokey](https://github.com/autokey/autokey) and
[Plover](https://www.openstenoproject.org/plover/)) that won’t work on
Wayland, either. So I run GNOME on X by default, anyway.

## LXC Configuration

Compared to the [basic LXC configuration that I have described
before]({filename}lxc-basics.md), there’s only one line that you’ll
need to add:

```ini
lxc.mount.entry = /tmp/.X11-unix tmp/.X11-unix none bind,optional,create=dir,ro
```

Now let me explain what this does. `/tmp/.X11-unix` is where your X
display sockets will live, and I map it to the same path in the
container. 

If I look into this directory while I’m in an X session myself, I
see one single socket file in there, named `X0`, which is owned by my
user account that owns the session.

And since my standard configuration maps my personal user account (and
*only* my personal user account) from the host to the container, that
means that processes running as `florian` in the container will be
able to use this socket just like processes owned by `florian` in the
host can.

Now, what’s with the `create=dir` and `ro` options?

* `create=dir` tells LXC to create the mount point in the container if
  it does not exist.
* `ro` bars processes in the container from creating or deleting any
  files in the directory. You see, my X server always runs in my host
  OS, I only want applications running in the container to connect to
  it, as clients. So there’s no need for applications in the container
  to ever modify this directory. However, you’ll almost certainly be
  running something on your system that will sweep `/tmp` on system
  startup
  ([`systemd-tmpfiles`](https://www.freedesktop.org/software/systemd/man/systemd-tmpfiles-setup.service.html)
  will, for example), and if that happened, you’d lose the socket.

With all that set up, any application that runs in the container with
a default `$DISPLAY` variable (`:0`) in its environment, will connect
to the socket in `/tmp/.X11-unix/X0` which is a direct pass-through of
the X server socket in the host.


## Things to consider

* Since my [default configuration]({filename}lxc-basics.md) maps
  `/home` in the host to `/home` in the container, any application
  running in the container will happily apply the same configuration
  as in the host. So for example, if I start Firefox in the
  container, my Firefox profiles and configuration are all
  there. However, so are any application locks that my application
  creates.  
  Sticking with the Firefox example, I won’t be able to open a
  specific profile in the container that is simultaneously open in the
  host. I can, however, totally use two different profiles
  side-by-side, or the same profile sequentially in first the host,
  then the container or the other way round.

* On a highly customized desktop your application may look different
  in the container than it does in the host. For example, my desktop
  is configured to use
  [Cantarell](https://en.wikipedia.org/wiki/Cantarell_(typeface)) as
  its sans-serif and [Hack](https://sourcefoundry.org/hack/) as its
  monospace font. If I neglect to install the `fonts-cantarell` and
  `fonts-hack` Ubuntu packages in my container, containerized X
  applications will instead fall back to the system default fonts. The
  same consideration applies for GTK themes.

* I have yet to tell you about pushing sound from the container to the
  host, and about sharing the host’s webcam and microphone with the
  container. More on that in future installments in this series.
