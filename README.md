## Prerequisites

```bash
sudo apt-get install --no-install-recommends \
	xserver-xorg-video-fbdev \
	xserver-xorg-input-evdev \
	xserver-xorg-legacy \
	chromium-browser \
	rpi-chromium-mods \
	xinit \
	x11-xserver-utils \
	xserver-xorg \
	python3-requests
	python3-setuptools \
	python3-pip \
;

pip3 install -r requirements.txt
```

## Screen dimming
```
0  8  * * * root echo -n 0 > /sys/class/backlight/rpi_backlight/bl_power
0  23 * * * root echo -n 1 > /sys/class/backlight/rpi_backlight/bl_power
```

Disable screen at 11pm, enable at 8pm.  Would love to make this touch based.

## Image collection

```
54 *  * * * root python3 collector -i [ALBUM] photos
```

Grabs photos at 54 minutes after the hour from iCloud album [ALBUM].  Stores them in the `photos` directory. Multiple `-i` parameters can be passed to use multiple iCloud albums.

## Image rotation

Using either feh or sxiv in .Xsession to handle image slideshow on screen.  Only other additions to .Xsession are:

```bash
xset s off -dpms
xset s noblank
```

### Using feh

[feh](https://feh.finalrewind.org/) doesn't support animation, but randomization is a nice touch.  Also, properly vertical alignment on landscape photos.

```bash
sudo apt-get install feh ;

feh \
    --auto-rotate \
    --auto-zoom \
    --borderless \
    --fullscreen \
    --hide-pointer \
    --randomize \
    --recursive \
    --slideshow-delay 30 \
    photos/
;
```

### Using sxiv

[sxiv](http://muennich.github.io/sxiv) supports animation but not random ordering. Landscape images always appear pulled down to the bottom of the screen with a black bar only at the top of the screen.

```bash
sudo apt-get install sxiv ;

sxiv \
	-a \
	-b \
	-f \
	-p \
	-r \
	-S 30 \
	-s f \
	photos/ \
;
```
