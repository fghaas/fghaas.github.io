---
title: Podman Compose and Rootless Mode, an Update
date: 2026-10-05 23:00
slug: podman-compose-rootless-userns-mode
tags: Containers, Podman, Docker, systemd
summary: An update to my standard approach to running rootless Podman containers
---

I have [previously]({filename}opencode-podman.md) discussed my approach to running OpenCode in rootless Podman containers, based on an [earlier article]({filename}rootless-podman-docker-compose.md) on the general subject.

Having recently upgraded my system to Ubuntu Resolute (which ships with Podman 5.7), I came across this curveball:

1. In release 5.6, Podman started disallowing the use of `--pod` and `--userns` in the same container, which [tripped up](https://discussion.fedoraproject.org/t/error-userns-and-pod-cannot-be-set-together/164595/4) plenty of users.
2. At some point (I don't know when, exactly), `podman-compose` apparently started chucking all services defined in one compose file, into one Pod.
3. At that point, then, it became impossible to use the `userns_mode: keep-id` option in a compose definition.

What you must now do, if you want to keep passing through your user id into a rootless container, is add this snippet to your `podman-compose.yaml` file:

```yaml
x-podman:
  in_pod: false
```

So, far, so good, but this only saves you if you previously put `userns_mode: keep-id` *in your compose file.*

But as you'll recall from my [previous article]({filename}rootless-podman-docker-compose.md), there used to be another way of achieving userid passthrough, which was to set the `PODMAN_USERNS` environment variable.
I used to do this from a systemd user service definition, like so:

```ini
[Unit]
Description=Podman via podman-compose
Wants=network-online.target
After=network-online.target
RequiresMountsFor=%t/containers

[Service]
Environment=PODMAN_SYSTEMD_UNIT=%n
Environment=PODMAN_USERNS=keep-id
# [etc...]
```
And it looks like podman-compose's behaviour has changed to effectively *ignore* that environment variable (even though [the documentation](https://docs.podman.io/en/latest/markdown/podman-pod.unit.5.html#userns-mode) says it's still being honoured).

So, it looks like overall I need to follow this checklist:

1. In my Compose files, add `userns_mode: keep-id` to services where needed.
2. Add the `x-podman` section with `in_pod: false`.
3. Drop the `Environment=PODMAN_USERNS` line from my systemd definitions, having become a no-op.

