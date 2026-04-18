Title: Containing OpenCode with Podman
Date: 2026-04-18
Slug: opencode-podman
Tags: Podman, OpenCode
Summary: It's not completely trivial to run OpenCode in rootless Podman. But it's not impossible, either.

[OpenCode](https://opencode.ai/) is an MIT-licensed agentic coding assistant.
It's not completely trivial to run it in [rootless Podman](https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md), but it can be done.
Here's how.

## The OpenCode container image

Although the OpenCode documentation makes it a bit hard to find, an official Docker image for OpenCode does exist, and is available from the [GitHub Container Registry](https://ghcr.io/anomalyco/opencode) (GHCR).

It runs in TUI mode, out of the box, with `podman run`, like so:

```shell
podman run -it ghcr.io/anomalyco/opencode
```

Images are released along with new OpenCode versions, so if you don't want the latest, you might instead want to run:
```shell
podman run -it ghcr.io/anomalyco/opencode:1.4.5
```

## Rootless Podman
I've written about how I manage services with `systemd` and `podman` in rootless mode before; see [this article]({filename}rootless-podman-docker-compose.md) for details.

The remainder of this article assumes the same setup.

## The objective
What I want to do is this:

1. Run OpenCode in a rootless Podman container that I can manage as a [user-mode systemd service](https://wiki.archlinux.org/title/Systemd/User).
2. _Selectively_ give OpenCode access to a directory containing Git repos.
3. Ensure that OpenCode has access to those files using my user identity, the way the OpenCode TUI would if I ran the `opencode` binary directly (without a container).
4. Define everything in a Docker Compose configuration.[^compose]

[^compose]: The reason I want to use the Docker Compose format is simplicity and personal preference.
Skipping this layer, and using [Podman Quadlets](https://docs.podman.io/en/latest/markdown/podman-quadlet.1.html) instead, would also be an option.

Obviously, the TUI itself won't be very helpful for that purpose.

However, OpenCode also comes with a very helpful [server mode](https://opencode.ai/docs/server/), including a web-based GUI, and this we can containerize rather well.

## Considerations
There's a few things one needs to know to make this work.

### Default config file paths
In a default configuration, OpenCode needs access to the following files and directories, in addition to the working directory with the code I want it to modify:

* `~/.config/opencode/opencode.json` or `~/.config/opencode/opencode.jsonc`: OpenCode's main configuration file.
* `~/.local/share/opencode`: Directory for logs, and OpenCode's SQLite database.
* `~/.local/state/opencode`: Directory for lock files and other state information.
* `~/.cache/opencode`: Cache directory.

Thus, containerized OpenCode requires that I mount these paths into my container.

### OpenCode in server mode

When running in server mode, OpenCode by default listens on `localhost` only.
Thus, if I want to run it in a container and port-forward its server, it's necessary to pre-create the `~/.config/opencode/opencode.json` file and populate it.
Like so:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "server": {
    "port": 4096,
    "hostname": "0.0.0.0",
    "cors": [
      "http://localhost:4096"
    ]
  }
}
```

### Podman with `PODMAN_USERNS=keep-id`
When you run Podman with `PODMAN_USERNS=keep-id`, as I normally do, Podman

* makes sure that the user ID and name in the container match the  UID and name of the host user that invokes the container,
* sets that user's home directory in the container to whatever `--workdir` option it was invoked with (or `/` if no such option was given),
* injects a line to the above effect into `/etc/passwd` in the container.


## Putting it all together
With all the above in mind, I can use this Compose configuration:

```yaml
services:
  opencode:
    image: ghcr.io/anomalyco/opencode:1.4.7
    container_name: opencode
    volumes:
      - ~/.local/share/opencode:/home/coder/.local/share/opencode
      - ~/.local/state/opencode:/home/coder/.local/state/opencode
      - ~/.config/opencode/opencode.json:/home/coder/.config/opencode/opencode.json
      - ~/.cache/opencode:/home/coder/.cache/opencode
      - ~/coding/git:/home/coder/git
    working_dir: "/home/coder"
    command: serve
    ports:
      - "127.0.0.1:4096:4096"
    environment:
      - 'SHELLCHECK_EXTERNAL_SOURCES=false'
    restart: unless-stopped
```

I can then invoke this like so:

```shell
PODMAN_USERNS=keep-id podman compose up
```

With this,

* My host UID is mapped to the same UID in the container, meaning all file access on the host and in the container use the same credentials.
* My home directory inside becomes `/home/coder` inside the container.
* My OpenCode configuration files and state directory are accessible to OpenCode in the container.
* My home directory's `coding/git` subdirectory (assuming that's where all my Git checkouts live) becomes `/home/coder/git` in the container.
If I wanted to be even more restrictive, I could mount just a single Git checkout directory into that container path.
* The OpenCode web server is available on my host as <http://localhost:4096>.

Setting the environment variable `SHELLCHECK_EXTERNAL_SOURCES=false` is a workaround for the [OpenCode issue 5363](https://github.com/anomalyco/opencode/issues/5363).
