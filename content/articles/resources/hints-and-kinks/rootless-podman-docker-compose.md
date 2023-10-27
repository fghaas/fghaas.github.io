Title: Rootless Podman, systemd, and Docker Compose files
Date: 2023-10-26 21:00
Slug: rootless-podman-docker-compose
Tags: Containers, Docker, Podman, systemd
Summary: How I run containers for my Home Assistant deployment

This is a summary of how I run a set of Docker (actually, [Podman](https://podman.io/)) containers for my [Home Assistant](https://www.home-assistant.io/) setup on a [Raspberry Pi](https://en.wikipedia.org/wiki/Raspberry_Pi). It works reasonably well for me, so I am sharing it here in the hope that it is useful to others.


## The stage

I run my Home Assistant environment on a [Raspberry Pi 4B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) running, currently, [Ubuntu 23.04 Lunar Lobster](https://releases.ubuntu.com/lunar/).
In total, that little machine runs five containers, out of which 3 are related to Home Assistant:

* One is for Home Assistant itself,
* one is for running the [Mosquitto](https://mosquitto.org/) MQTT broker,
* and one is for running [Grott](https://github.com/johanmeijer/grott).

For all these services, the respective developer communities do not only maintain official Docker images, but also supported or at least recommended [Docker Compose](https://docs.docker.com/compose/) configurations.

I wanted a way to make the most of those available configurations, so as not to reinvent too many wheels.


## How I manage containers

I prefer my containers to run [in the context of users other than `root`](https://www.redhat.com/sysadmin/rootless-podman-makes-sense).

### Per-container system users

This means that I create a dedicated user for each container.
What's important is that in order to be able to use systemd user services later, I enable [lingering](https://www.freedesktop.org/software/systemd/man/latest/loginctl.html#enable-linger%20USER%E2%80%A6) for each user account.

For example:

```console
$ sudo -i
# useradd homeassistant
# adduser homeassistant bluetooth
# loginctl enable-linger homeassistant
```

In order to *actually* enable lingering for the affected users, one must apparently reboot the machine after this change.

(I'll get back to why I add the `homeassistant` user to the `bluetooth` group in a moment.)

### Podman

I also don't very much like the daemon-driven approach from Docker proper, so I tend to prefer `podman` as my container manager on a small system like the Raspberry Pi.

Podman tends to not be *particularly* well covered in the documentation of the projects I work with, but that is not much of an issue:
I can combine Podman with a compatibility layer, `podman-compose`, so that although I am actually *using* Podman, I can configure my containers with an unchanged YAML configuration originally written for Docker Compose.

Here's how I can install the necessary packages on my Raspberry Pi:

```console
# apt install podman podman-compose
```

Next, I create the necessary Docker Compose configurations in the home directory of a user created to run that container.

For example, the `/home/homeassistant` directory, owned by the user `homeassistant`, contains this `docker-compose.yaml` file:

```yaml
# /home/homeassistant/docker-compose.yaml
---
version: '3'
services:
  homeassistant:
    container_name: homeassistant
    image: "ghcr.io/home-assistant/home-assistant:stable"
    volumes:
      - /etc/localtime:/etc/localtime:ro
      # Replace this volume mapping with wherever
      # you want to put your Home Assistant configuration
      - /home/homeassistant/.config/homeassistant:/config
      - /run/dbus:/run/dbus:ro
    ports:
      - 8123:8123
    restart: always
    environment : {}
```

You can of course create a more elaborate configuration as you please.

Once this is set, I can manually fire up my container as a non-`root` user, using Podman, like so:

```console
$ id
uid=1003(homeassistant) gid=1003(homeassistant) groups=1003(homeassistant),124(bluetooth)

$ podman-compose up
['podman', '--version', '']
using podman version: 4.3.1
** excluding:  set()
['podman', 'network', 'exists', 'homeassistant_default']
podman create --name=homeassistant --label io.podman.compose.config-hash=123 --label io.podman.compose.project=homeassistant --label io.podman.compose.version=0.0.1 --label com.docker.compose.project=homeassistant --label com.docker.compo
se.project.working_dir=/home/homeassistant --label com.docker.compose.project.config_files=docker-compose.yaml --label com.docker.compose.container-number=1 --label com.docker.compose.service=homeassistant -v /home/homeassistant/.config/h
omeassistant:/config -v /usr/share/zoneinfo/Etc/UTC:/etc/localtime:ro -v /run/dbus:/run/dbus:ro --net homeassistant_default --network-alias homeassistant -p 8123:8123 --restart always ghcr.io/home-assistant/home-assistant:stable
[...]
```

### Systemd

Once I am satisfied that my container comes up just fine, the next step is managing it with `systemd` in [user mode](https://wiki.archlinux.org/title/systemd/User).

To do that, I need to create a config directory for `systemd`:

```console
$ mkdir -p ~/.config/systemd/user
```

... and create a single file in there, which I name `podman-compose.service`:

```ini
[Unit]
Description=Podman via podman-compose
Wants=network-online.target
After=network-online.target
RequiresMountsFor=%t/containers

[Service]
Environment=PODMAN_SYSTEMD_UNIT=%n
Environment=PODMAN_USERNS=keep-id
Restart=always
TimeoutStartSec=60
TimeoutStopSec=60
ExecStart=/usr/bin/podman-compose up --remove-orphans
ExecStop=/usr/bin/podman-compose stop
Type=simple
WorkingDirectory=%h

[Install]
WantedBy=default.target
```

Note that many other tutorials about running `docker-compose` or `podman-compose` from systemd recommend you set `Type=oneshot` instead, and add the `-d` option to the `ExecStart` command.

I think using the `simple` type and *omitting* the `-d` option is the better idea, because in doing so,

* I see the latest log lines from the container in `systemctl --user status podman-compose`,
* I can access the full log with `journalctl --user -u podman-compose`,
* I get more reliable output overall from `systemctl --user status podman-compose`, because rather than only reflecting whether *starting* the container was successful, it tells me whether it is still *running* at the time I check.

For more details on what the various `%`-prefixed *specifiers* mean, see [the relevant section in the systemd documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html#Specifiers).

The `Environment=PODMAN_USERNS=keep-id` entry is somewhat crucial in a Home Assistant configuration.
This, in combination with adding the `homeassistant` user to the `bluetooth` group and bind-mounting the `/run/dbus` directory, enables me to use the Raspberry Pi's Bluetooth controller from the rootless container.[^fattire]
That comes in handy for Home Assistant integrations for sensor devices using [BLE](https://en.wikipedia.org/wiki/Bluetooth_Low_Energy).

[^fattire]: Thanks to GitHub user ["Fattire"](https://github.com/fat-tire) for [an immensely useful GitHub comment](https://github.com/onedr0p/containers/issues/68#issuecomment-1250035050) on this subject!


Then, running

```console
$ systemctl --user daemon-reload
$ systemctl --user start podman-compose
$ systemctl --user enable podman-compose
```

starts my container, and also brings it up (under the non-`root` user account) every time the system boots.

## In summary

What's nice about this whole approach is that for all of my container-based services **the configuration is exactly identical,** except for one thing that differs from service to service: the `docker-compose.yaml` file.
