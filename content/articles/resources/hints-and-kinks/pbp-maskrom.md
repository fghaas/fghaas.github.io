Title: Reviving a near-bricked Pinebook Pro
Date: 2025-10-05
Modified: 2025-10-05
Slug: pbp-maskrom
Summary: I've recently had to bring back my Pinebook Pro from a zombie state.
Tags: Pinebook Pro

Recently, I put [my Pinebook Pro]({filename}solar-powered-laptop.md) in something of a zombie state.
This was by no means the hardware's fault, nor that of the [Armbian](https://www.armbian.com/pinebook-pro/) system I run on it.
Rather, I put a bad bootloader image into the SPI flash (`/dev/mtd0`), which upon reboot put the laptop in permanent Maskrom mode.

It took me a little while to figure this out, because from the outside Maskrom mode looks remarkably like the machine is dead:
when you hit the power button, nothing appears to happen.
The power LED doesn't come on (not even in red), the display stays dark.
And the PBP being a fanless device, there's obviously no fan spin-up either.

What I needed to do instead was find another machine, and connect it (via a USB A-to-C cable) to the PBP's USB-C port.
Then I powered on the PBP.
If the PBP is in fact *not* dead, but in Maskrom mode, the kernel log (on the good machine) will show a message like this:

```console
$ journalctl -b --grep 2207
Oct 05 09:30:43 foobar kernel: usb 1-6: New USB device found, idVendor=2207, idProduct=330c, bcdDevice= 1.00
```

I was also able to use `rkdeveloptool` (on the good machine) to talk to the device:

```console
$ rkdeveloptool ld
DevNo=1	Vid=0x2207,Pid=0x330c,LocationID=106	Maskrom
```

Once able to access the PBP in Maskrom mode, I was nearly back in business.
I now needed to follow the instructions for [writing to the SPI from another machine](https://wiki.pine64.org/wiki/Pinebook_Pro_SPI#After_entering_maskrom_mode) in the Pinebook Pro wiki.

Now, I've found that zeroing the SPI (which *should* mean that the PBP boot process just ignores the SPI, and attempts to find a boot loader on the eMMC, and then on the MicroSD card) didn't change anything for me --- the PBP just kept coming back into Maskrom mode after resetting or power-cycling.

Thus, I chucked [Tow-Boot](https://tow-boot.org/devices/pine64-pinebookPro.html) into the SPI.
At the time of writing, that was version 2023.07-007, downloaded from its [GitHub release page](https://github.com/Tow-Boot/Tow-Boot/releases/tag/release-2023.07-007).

I also had to obtain the `rk3399_loader_spinor` binary from the recommended source (at the time of writing, that's <https://dl.radxa.com/rockpi4/images/loader/spi/rk3399_loader_spinor_v1.15.114.bin> per the wiki).

Thus, the whole process amounted to:

1. Enumerating the device with `rkdeveloptool ld`
2. Applying the bootloader
3. Writing the `Tow-Boot.spi.bin` file
4. Checking
4. Rebooting the device

Here is the corresponding sequence of commands.

```console
$ rkdeveloptool ld
DevNo=1	Vid=0x2207,Pid=0x330c,LocationID=106	Maskrom
$ db rk3399_loader_spinor_v1.15.114.bin
Downloading bootloader succeeded.
$ rkdeveloptool wl 0 towboot/pine64-pinebookPro-2023.07-007/binaries/Tow-Boot.spi.bin
Write LBA from file (100%)
$ rkdeveloptool td
Test Device OK.
$ ./rkdeveloptool rd
Reset Device OK
```

After this, the power LED immediately came on and the PBP happily booted Tow-Boot, which then enabled me to select the boot device and boot from either the eMMC or MicroSD card.
