Title: Running a solar-powered laptop
Date: 2022-05-14
Slug: solar-powered-laptop
Summary: I’m a happy Pinebook Pro user, and I frequently use it on solar power.

![Pinebook Pro laptop sitting on a table, outside, connected to a solar charging panel](/images/pinebookpro.jpg)

This piece of kit has been a conversation starter everywhere I take it
out, so I figured it could use a short writeup.

In 2020 I purchased a [Pinebook
Pro](https://www.pine64.org/pinebook-pro/) laptop. I had wanted a
low-power ARM laptop for a while, the PBP came in a tolerable size
(this is a 14" screen; about the top end of acceptable screen sizes
for me), and it was an absolute steal. Including shipping and import
duty — my device shipped from Hong Kong — I got mine for €277 all
told.

Now if you haven’t heard of the Pinebook Pro, or for that matter of
the PINE64 community, you should [check out their web
site](https://www.pine64.org/). They make a bunch of really neat
devices, though I can only speak to the Pinebook Pro as that’s the
only one of their devices I’ve ever owned.

Obviously, the device’s claim to fame is its low power profile. Thus
it should come at no surprise that its charging input voltage is a
USB-typical 5V, like you know from your phone.

Now the PBP comes with a separate barrel-plug charging port, but most
of the time I just charge it via it USB-C. This I do primarily for
convenience; it’s simply one fewer piece of kit to carry around. I can
charge thus charge the PBP with a standard wall-socket USB charger, a
USB power bank, or any other USB power source.

Which is where the solar panel comes into play. Mine is a [28W charger
from BigBlue](http://www.ibigblue.com/product/detail/?id=17). Now,
please don’t mistake me for an authority on solar panels; there may be
better or more efficient ones on the market — I just found this one
useful and compact enough for my liking. Nominally, this panel’s
maximum amperage is 4.8A, but I’ve never seen it actually generate
that. Under optimal conditions where I live (at 48°N latitude), that
is direct sunlight around solar noon on a cloudless day, I can get
just under 3A out of the panel in total. Out of this, the maximum
output of a single port is 2.1A, so that’s my maximum solar charge
current for the PBP.[^charge]

[^charge]: The device cannot charge over the barrel port and USB-C
    simultaneously.

Overall, for the PBP’s power consumption this is generally perfectly
fine. I can work under a sunny or partly cloudy sky for the whole day
if I want to.

I’ve also found the display contrast to be sufficient even in full
sunlight. I do use a light GNOME theme for my desktop settings, but I
don’t need to enable the high-contrast accessibility features. It’s
not advisable to work with the whole laptop exposed to full sunlight,
though, as the black device body does absorb a fair bit of heat. If
you’re sitting outside with a light breeze going, that mitigates this
problem.

Of course, sitting in the shade with just the panel exposed to the sun
is the most preferable setup overall.

In terms of software running on the device, I never particularly
warmed to the idea of running [Manjaro](https://manjaro.org/) (which
the PBP ships with by default), so I run
[armbian](https://www.armbian.com/pinebook-pro/) with Ubuntu. I’m not
a big fan of Cinnamon or XFCE either, but that’s no big issue: I just
started with the Ubuntu Focal XFCE image, and then installed the
`vanilla-gnome-desktop` metapackage and subsequently removed `xfce4*`.

Overall the Ubuntu `aarch64` port works very well on this device with
the armbian kernel (currently, that’s 5.9.14), with a couple of small
caveats:

* Suspend support is essentially limited to suspend-to-idle. I’d
  really love to have suspend-to-disk support on this device (ideally
  in combination with encrypted swap, which by itself works fine), but
  neither that nor suspend-to-ram are currently reliable. Even
  suspend-to-idle is sometimes unreliable and requires that I restart
  `gdm` after resuming.

* Some packages just behave oddly, or don’t function at all. For
  example, `ykcs11` just won’t want to accept my PIN when I try to
  hook my Yubikey up with `ssh-agent`.

* Most [PPAs](https://launchpad.net/ubuntu/+ppas) don’t build with
  `aarch64` support. Thus, if you like to run Ubuntu with a bunch of
  packages that are not in Ubuntu proper, you might have a hard time
  with the PBP.

* The PBP’s SoC maxes out at 4GiB RAM, which means you shouldn’t be
  using the PBP for video editing or gaming or any other RAM-intensive
  activities. Even the GIMP runs out of steam pretty quickly at about
  3 or 4 concurrently opened images.[^ram]

[^ram]: Note that I can get cloud computing capacity for cheap at work, so
    if I need more RAM for something I can get it in a pinch — I am
    aware that that option is not available to everyone.

So can I use this as my daily driver? Yes, with some minor drawbacks.
But those I can work around fairly well.
