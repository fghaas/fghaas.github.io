Title: Running (Almost) Anything in LXC: Sound
Date: 2021-01-16
Slug: lxc-sound
Series: Running (Almost) Anything in LXC
Series_index: 2
Tags: LXC


Some of the [X applications I run in LXC]({filename}lxc-x11.md) make
sounds. Now, I find alert sounds horribly distracting so I turn them
off, but for some containerized applications I want to actually play
sound.

Examples include the [Spotify Linux
client](https://www.spotify.com/download/linux/) (which I run in its
own LXC container because it’s not open source), and occasionally
things like the latest available [Shotcut](https://shotcut.org/)
version for video editing.

You’ll notice that, on face value, that’s a pretty similar problem
compared to getting containerized applications to talk to my X
server. It’s just that rather than applications only being clients to
my X server, I also want them to be clients to my PulseAudio daemon.

## LXC (Non-)Configuration

In the article on running [X applications in
LXC]({filename}lxc-x11.md), I give the example of sharing a host
directory, which contains X.org server sockets.

In principle, I *could* do the same thing with the Unix socket that
PulseAudio runs. However, there’s a small problem with that: the
directory I would have to bind-mount into my container is
`/run/1000/pulse`, and you see the difference to bind-mounting
`/tmp/.X11-unix`: `/tmp` already exists in my container on system
startup — but while `/run` also does, `/run/1000` does not. I have
experimented with making this work, and I’ll spare you the details but
it’s not as simple as it initially looks. I eventually gave up on that
approach, because there is a much simpler way to do this — and it
doesn’t even require any specific LXC container configuration.

The trick is to use the PulseAudio `native-protocol-tcp` module. When
I load it into my running PulseAudio configuration, like so:

```bash
pactl load-module module-native-protocol-tcp
```

... then a PulseAudio sound server starts listening on a TCP socket on
port 4713.

I can of course also add this line (minus its `pactl` prefix) to my
PulseAudio configuration file, `~/config/pulse/default.pa`.

And then, all I need to do is attach to my container, export the
`PULSE_SERVER` environment variable set to `10.0.3.1` (my IPv4 address
of the host on the `lxcbr0` bridge), and launch an application.

I can do this all in one go, like so (using the Spotify client as an example):

```bash
pactl load-module module-native-protocol-tcp && \
  lxc-start -n focal-spotify && \
  sleep 1 && \
  lxc-attach -n focal-spotify -- \
  sudo -Hu florian env PULSE_SERVER="10.0.3.1" spotify && \
  lxc-stop -n focal-spotify
```

... and as long as the application links to any PulseAudio client
libraries, it will correctly parse the set `PULSE_SERVER` environment
variable as an instruction to connect to the given IP address on its
default port, and send its audio stream there.

I am then still able to control my volume, control my mix, and mute
the output from my host.

Of course, you probably want to chuck that long command into a
`.desktop` file, or wrap it in a script or function.

By the way, no I don’t really know why I need that 1-second `sleep`
between starting the container and attaching to it, but it works for
me and breaks without it. I presume there is *some* initialization
going on in the container that needs just a few tenths of a second to
complete. And I can deal with waiting for my music for one more
second.

## Things to consider

Your Ubuntu desktop will most likely run with
[`ufw`](https://wiki.ubuntu.com/UncomplicatedFirewall) enabled. If
your containerized applications are unable to connect to the
PulseAudio server because your firewall blocks them, you won’t get
sound. Here’s what I do:

First, I create `/etc/ufw/applications.d/pulseaudio`, with this
content:

```ini
[pulseaudio]
title=PulseAudio Native Protocol TCP
description=PulseAudio Sound Server 
ports=4713/tcp
```

Then, I allow traffic incoming via the LXC bridge to connect to that
server:
   
```bash
sudo ufw allow in on lxcbr0 to any app pulseaudio
```

Also do consider, of course, that once your system is set up in this
way, not only will your LXC applications be able to play sound through
your speakers, but they will also be able to pick up input from your
microphone. So use this wisely, particularly if the application you
are running does record and process sound.

Sometimes you totally **want** your application to record sound,
though, and indeed see the video stream from your webcam, too. Zoom
calls come to mind as one such example. More on this in the next
installment of this series, where I’ll talk about letting your
containerized app use host video input.
