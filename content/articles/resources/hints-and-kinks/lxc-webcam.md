Title: Running (Almost) Anything in LXC: Applications Using Your Webcam
Date: 2021-01-17
Slug: lxc-webcam
Series: Running (Almost) Anything in LXC
Series_index: 3
Tags: LXC

One of the non-open-source applications I sometimes have to run for
work purposes, and which out of principle I run in LXC containers, is
Zoom. Now Zoom is of course an X application, so my previously shared
[considerations]({filename}lxc-x11.md) for those apply. It also needs
to process input from my microphone, and feed sound into my
headphones, so [that’ll have to work, too]({filename}lxc-sound.md).

But a thus-configured LXC container is still missing one other bit:
it’ll have to process the video feed from my webcam. Here’s how to do
that.

## LXC Configuration

In the article on running [X applications in
LXC]({filename}lxc-x11.md), I give the example of sharing a host
*directory,* (the one that contains the X.org server sockets). For
sharing a webcam, I need to do the same for a few *files*.

Now, video capture devices like webcams are represented in Linux by
_character devices_ named `/dev/video0`, `/dev/video1` and so
forth. Udev manages these and (on Ubuntu platforms) creates them as
owned by the user `root` and the group `video` — but it helpfully also
creates POSIX ACL entries for the user currently logged in on the X
console.

All I thus need to do is *mount* these files into the container (yes,
LXC lets you “mount” individual files), like so:

```ini
lxc.mount.entry = /dev/video0 dev/video0 none bind,optional,create=file
lxc.mount.entry = /dev/video1 dev/video0 none bind,optional,create=file
lxc.mount.entry = /dev/video2 dev/video2 none bind,optional,create=file
lxc.mount.entry = /dev/video3 dev/video2 none bind,optional,create=file
```

Here, the `optional` bit of course means that the container will start
even in case a particular file does not exist in the host at the time
the container receives its `lxc-start` command.

That, in principle, is all there is to it.

## Things to consider


Be aware that [since early
2018](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=088ead25524583e2200aa99111bea2f66a86545a)
(in other words, in kernel 4.16 and later) the Linux kernel’s
`uvcvideo` subsystem will create **two** `/dev/video` devices for your
webcam. One of them is the actual video capture device; the second one
is a metadata device node. You can easily tell which is which, with
`v4l2-ctl`: only a video capture device will have a non-empty list of
supported formats.

This is a video capture device:
```
$ v4l2-ctl --list-formats --device /dev/video0
ioctl: VIDIOC_ENUM_FMT
	Type: Video Capture

	[0]: 'MJPG' (Motion-JPEG, compressed)
	[1]: 'YUYV' (YUYV 4:2:2)
	[2]: 'H264' (H.264, compressed)
```

And this is the metadata device; note that it lists no video codecs:

```
$ v4l2-ctl --list-formats --device /dev/video1
ioctl: VIDIOC_ENUM_FMT
	Type: Video Capture
```

Normally, device nodes `/dev/video0` and `/dev/video1` will be
occupied by a built-in webcam, your USB webcam will use `/dev/video2`
and `/dev/video3`, and if you have *another* video capture device then
that will be `/dev/video4` and `/dev/video5`.

Thus, perhaps you want your container to see *only* your USB webcam,
*and* you don’t care about the metadata device. In that case, instead
of the four `lxc.mount.entry` lines I gave above, you might use just
one:

```ini
lxc.mount.entry = /dev/video2 dev/video2 none bind,optional,create=file
```

Also, the bind mounts occur at the time you *start* the container. Thus,
if you plug in a USB webcam while the container is already running, it
won’t magically become available to the container. There are two ways
to address this:

1. You start (or restart) your container whenever you need to use a web
   cam (or other video device) that you have just plugged in, *or*

2. you remove the `optional` keyword from your `lxc.mount.entry`
   line(s), so that the container will refuse to start unless the
   correct webcam is plugged in.

Note further that for the same reason, if you disconnect your USB
webcam *while your container is running,* you can’t just plug it
back in and expect it to work. In that case, udev in the host will
have deleted the device node, so the bind mount in your container is
now stale, and your containerized applications won’t be able to use
your capture device anymore. Under those circumstances, you’ll simply
have to restart your container.
