Title: Fixing powerline flicker on your webcam feed with a udev rule
Date: 2021-01-17
Slug: webcam-rolling-shutter-udev
Tags: udev

If you are

* spending a non-trivial amount of time in video calls every week
  (something that, at the time of writing, is true for **a lot** of
  people due to the COVID-19 pandemic), and also

* having to use mains-powered artificial lighting in your office (true
  at the time of writing for significant portions of the Northern
  Hemisphere, as it’s winter there),
  
then you may be dealing with an unpleasant effect where your web cam
feed produces a permanent [horizontal
flicker](https://dsp.stackexchange.com/questions/19853/horizontal-banding-flickering-due-to-electronic-rolling-shutters)
that is due to the electronic rolling shutter interacting with the
(otherwise imperceptible) 50 or 60Hz AC powerline frequency.

The good news is that most webcams come with a facility to eliminate
that effect, and on a Linux desktop it’s not difficult to permanently
do so.

## `v4l2-ctl`

The utility you want to use for this purpose is `v4l2-ctl`, which on
Ubuntu ships with [the `v4l-utils`
package](https://packages.ubuntu.com/v4l-utils). `v4l2-ctl` allows you
to read and set a bunch of parameters for your webcam. Here’s the set
of parameters available for my [Razer
Kiyo](https://www.razer.com/gb-en/streaming-cameras/razer-kiyo/RZ19-02320100-R3U1),
a piece of kit that I highly recommend:

```
$ v4l2-ctl --list-ctrls --device=/dev/video0
                     brightness 0x00980900 (int)    : min=0 max=255 step=1 default=128 value=128
                       contrast 0x00980901 (int)    : min=0 max=255 step=1 default=128 value=128
                     saturation 0x00980902 (int)    : min=0 max=255 step=1 default=128 value=128
 white_balance_temperature_auto 0x0098090c (bool)   : default=1 value=1
                           gain 0x00980913 (int)    : min=0 max=255 step=1 default=0 value=0
           power_line_frequency 0x00980918 (menu)   : min=0 max=2 default=2 value=2
      white_balance_temperature 0x0098091a (int)    : min=2000 max=7500 step=10 default=4000 value=4000 flags=inactive
                      sharpness 0x0098091b (int)    : min=0 max=255 step=1 default=128 value=128
         backlight_compensation 0x0098091c (int)    : min=0 max=1 step=1 default=0 value=0
                  exposure_auto 0x009a0901 (menu)   : min=0 max=3 default=3 value=1
              exposure_absolute 0x009a0902 (int)    : min=3 max=2047 step=1 default=127 value=127
         exposure_auto_priority 0x009a0903 (bool)   : default=0 value=1
                   pan_absolute 0x009a0908 (int)    : min=-36000 max=36000 step=3600 default=0 value=0
                  tilt_absolute 0x009a0909 (int)    : min=-36000 max=36000 step=3600 default=0 value=0
                 focus_absolute 0x009a090a (int)    : min=0 max=255 step=1 default=0 value=0 flags=inactive
                     focus_auto 0x009a090c (bool)   : default=1 value=1
                  zoom_absolute 0x009a090d (int)    : min=100 max=140 step=10 default=100 value=100
```

The value you’re looking for is `power_line_frequency`. Its default is
`2` (compensating for a 60Hz powerline frequency), which means the
camera should work out of the box and without any powerline flicker in
the Americas and parts of Asia. I am in Europe though, where the mains
frequency is 50Hz, so I need to set this to `1`:

```bash
v4l2-ctl --device /dev/video0 --set-ctrl=power_line_frequency=1
```

However, it’s rather tedious to run that command every time I want to use the
webcam.

## udev

Thankfully, this process can be automated with a simple udev rule:

```bash
ACTION=="add", SUBSYSTEM=="video4linux", DRIVERS=="uvcvideo", RUN+="/usr/bin/v4l2-ctl --set-ctrl=power_line_frequency=1"
```

This way, any camera handled by the `uvcvideo` driver (meaning,
practically any contemporary webcam) will have its power line
frequency setting configured to the 50Hz value, eliminating the
banding effect from the rolling shutter.

Chuck that line into a file in `/etc/udev/rules.d`, run `sudo udevadm
trigger`, and you should be good to go.


## Acknowledgments and further reading

I got the udev rule suggestion from user
[telcoM](https://unix.stackexchange.com/users/258991/telcom)’s answer
on [this StackExchange
post](https://unix.stackexchange.com/questions/581867/how-can-i-change-my-webcams-power-line-frequency-setting). The
discussion thread on that post has a few additional suggestions,
including some not using udev.
