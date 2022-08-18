Title: Jammy, don’t snap at me!
Date: 2022-08-19 21:00:00
Slug: jammy-dont-snap
Tags: Ubuntu, Firefox
Summary: The current Ubuntu LTS release, 22.04 “Jammy Jellyfish”, tries to force a snap-installed Mozilla Firefox on you. I’m not a fan of that approach.

The current Ubuntu LTS release, 22.04 “Jammy Jellyfish”, does not
install a Debian package for Mozilla Firefox anymore. Instead, Ubuntu
now delivers Firefox as a [snap](https://snapcraft.io/). I’m not
particularly enthralled by that idea.

Every once in a while I look at the current state of snaps. And every
time I look them, I find that they don’t solve any problems I am
having at the time, but do add some. The same, incidentally, happens
to be true for Wayland, which is why I still use X.org. (I want to
emphasize that the foregoing is true for *me* — your own experience
may well differ, and that’s perfectly okay.) So I have kept my systems
free of `snapd`, and I intend to keep them that way for the
foreseeable future.

However, if you upgrade an existing Ubuntu Focal or Impish system to
Jammy in-place, with the customary `apt dist-upgrade` command, Ubuntu
*replaces* the pre-existing Debian (`.deb`) package with a snap. That
is to say, `firefox` in Ubuntu Jammy is a [transitional
package](https://packages.ubuntu.com/jammy/firefox) that would install
`snapd` as a dependency, and then run `snap install
firefox`. Mid-upgrade, it does pause and prompt you about this fact —
but there’s no yes or no that would give you the option to bail, only
an “OK” button.

What you thus want to do if you’re wired like me, *prior* to
commencing your upgrade, is tell Ubuntu that you want to keep
installing Firefox from a package. And while you’re at it, you might
also politely inform your package manager that you have no desire to
use snaps, at all.

To do so, first become `root`, and make the necessary changes to
change the `focal` or `impish` references in your
`/etc/apt/sources.list` and `/etc/apt/sources.list.d` files to `jammy`
as you normally would.

Then, make sure that you don’t have the `snapd` package installed:

```console
# dpkg -l snapd
Desired=Unknown/Install/Remove/Purge/Hold
| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
|/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
||/ Name           Version      Architecture Description
+++-==============-============-============-=================================
un  snapd          <none>       <none>       (no description available)
```

Next, mark the `snapd` package with `hold`, so that the current state
of the package (`un`) is made permanent:

```bash
apt-mark hold snapd
```

Now, add the `mozillateam` PPA:

```bash
add-apt-repository ppa:mozillateam/ppa
```

Next, create a file named `/etc/apt/preferences.d/mozilla-firefox`,
containing the following three lines:

```yaml
Package: *
Pin: release o=LP-PPA-mozillateam
Pin-Priority: 1001
```

At this stage, your system should be set up to (a) not install the
snap daemon, and (b) conduct the upgrade of the `firefox`
package using the regular Debian package as it appears in the PPA, not
the distro package that is a wrapper around `snap install`.

Now, proceed with:

```bash
apt dist-upgrade
```

Happy jamming!