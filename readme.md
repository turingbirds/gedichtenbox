# De gedichtenbox

De gedichtenbox ("the poetry box" in Dutch) is a dispenser of free poetry to passer-bys. Over the years I've been fortunate to meet some awesome people who write unique pieces of improvised poetry, on a streetcorner or in a café, then and there. Typewriters are often involved. This project is intended as an homage to their art, and is also meant to provoke critical questions about the impact of technology (think of ChatGPT): can poetry, of all things, ever be "machinized"?

The operating principle is simple: press button, receive poetry. Poems are submitted by human (or machine?) authors and pre-loaded onto the machine. When a button is pressed, a random poem is printed on 80 mm wide thermal receipt paper. An intricate mechanism of motors, belts and rollers then delivers the poem to the top of the typewriter, which has been largely gutted (a heart-wrenching experience as it's such a beautiful work of engineering).

https://github.com/turingbirds/gedichtenbox/assets/1014092/50b8195d-de8d-44c0-9145-3f3c59cde40a


## Hardware notes

### System diagram

- Raspberry Pi 3B+
- 80 mm thermal receipt printer (with built-in partial cutter)
- Paper transport mechanism
- Servo paper cutter
- Front panel buttons
- 4 channel PWM driver (L293)
- 16 channel PWM generator chip (PCA9685)
- Uninterruptible power supply (UPS) module for the Raspberry Pi


https://github.com/turingbirds/gedichtenbox/assets/1014092/a68d2e8d-9c0c-4a15-b894-8fb986b5cebc


### Dimensions

33 cm (width) × 42 cm (depth) × 90 cm (height)

The pillar was made from 12 mm thick multiplex; all pieces were cut from a single 244×122 cm standard-size sheet.


## How to power on and power off

The Raspberry Pi runs the Linux operating system with mounted filesystems. To prevent filesystem corruption, the Pi is equipped with an uninterruptible power supply (UPS) module. This means it's possible to simply pull the plug and re-insert the plug at will. No special power on or power off procedures are needed. The system might continue to operate for a few minutes on battery power before automatically shutting down.

The printer is automatically started via a relay connected to the Raspberry Pi, that emulates a "power on" soft button press on the printer.


## How to load poems

The Raspberry Pi reads the poems from a USB drive. To make sure the poems can be found by the machine, please use the following structure.

Create a directory at the root of the USB drive called ``poems``. In there, create a directory for each language: ``Mestreechs``, ``Nederlands``, and ``English``. In each language directory, poems are saved as plain text files with the following structure:

```
<TITLE OF THE POEM>
<AUTHOR OF THE POEM>
<TEXT OF THE POEM>
<TEXT OF THE POEM>
...
<TEXT OF THE POEM>
```

Each plaintext file can have any name (``poem1.txt``, ``bukowski_poem.txt``, etc.) Try to avoid unusual Unicode characters. Make sure there are no empty (blank) lines at the end of the file.

Poems will be indexed when the Gedichtenbox is powered on. Please power down the Gedichtenbox before unplugging or replugging the USB drive. The USB socket can be found at the back of the pillar, behind the door, behind the paper feed button.

![Picture of roll in the holder](https://github.com/turingbirds/gedichtenbox/blob/main/fig/usb_stick.jpg?raw=true)


## How to change the poem layout and footer images

To change font and layout of each poem print, see ``scripts/print_poem.py``.

To change header and footer images, replace ``fig/header.png`` and ``fig/footer.png``. Make sure these images are 576 pixels wide.


## How to change the paper roll

Move the curtain aside on the back of the cabinet. There are two magnets holding it down on the bottom; you can pull these off and drape the curtain over the top of the typewriter to keep it out of the way.

![picture of curtain at back of cabinet](https://github.com/turingbirds/gedichtenbox/blob/main/fig/curtain.jpg?raw=true)

Use the key to open the door at the back of the cabinet. 

![picture of door and lock at back of cabinet](https://github.com/turingbirds/gedichtenbox/blob/main/fig/door_latch_rear.jpg?raw=true)

Remove the rubber band on one side of the metal axis holding the paper roll in place. Move the axis to the side unti it comes out and the old roll can be removed.

![Picture of roll in the holder](https://github.com/turingbirds/gedichtenbox/blob/main/fig/paper_roll_holder_rubber_band.jpg?raw=true)

Place the new roll in the holder. Make sure it's the right way around (the thermal paper can only be printed on its front side).

![Picture of roll in the holder](https://github.com/turingbirds/gedichtenbox/blob/main/fig/paper_roll_holder.jpg?raw=true)

By hand, feed the end of the paper into the printer. This can be a bit tricky; to make it easier, make a fold in the paper to get the right angle:

![Picture of making a fold in the paper](https://github.com/turingbirds/gedichtenbox/blob/main/fig/paper_prep.jpg?raw=true)

Additionally, to make it easier for the printer to grab onto the paper, you can make it more pointy by cutting off two corners with scissors:

![Picture of cutting off two corners of the paper](https://github.com/turingbirds/gedichtenbox/blob/main/fig/paper_prep2.jpg?raw=true)

Then, while holding the paper (straight!) into the printer, as indicated by the arrows:

![Picture of paper inserted into the printer](https://github.com/turingbirds/gedichtenbox/blob/main/fig/paper_inserted.jpg?raw=true)

Press the "feed paper" button until the paper roller in the printer latches on to it. Do not press feed longer than necessary, otherwise there will be a paper jam!

![Picture of the paper feed button](https://github.com/turingbirds/gedichtenbox/blob/main/fig/paper_feed_button.jpg?raw=true)


## How to clear a paper jam

From the top side, check that the rollers are clear and pull out any paper that might be stuck.

![Picture of the paper slot at the top](https://github.com/turingbirds/gedichtenbox/blob/main/fig/paper_slot.jpg?raw=true)

Try to use the paper feed button on the lower back to clear the paper jam.

If this doesn't work, you will have to open up the top lid of the pillar. Lift the typewriter by its frame in the front center (just underneath the space bar).

![Picture of the lid being lifted](https://github.com/turingbirds/gedichtenbox/blob/main/fig/lid_lift.jpg?raw=true)

![Picture of the lid being lifted](https://github.com/turingbirds/gedichtenbox/blob/main/fig/lid_lift2.jpg?raw=true)

![Picture of the lid being lifted](https://github.com/turingbirds/gedichtenbox/blob/main/fig/lid_lift3.jpg?raw=true)

If you lift the typewriter up as far as it will go, it will hold in that position.

**Be careful to lower the lid gently and not to get any fingers caught, the typewriter is very heavy!**

Remove any excess paper and check that the belts are aligned on the wheels. Check that the two metal rods on the bottom are coming out in such a position as to make contact with the top of the printer body when the lid is lowered.

![Picture of the paper transport mechanism](https://github.com/turingbirds/gedichtenbox/blob/main/fig/paper_transport.jpg?raw=true)

![Picture of the paper transport mechanism](https://github.com/turingbirds/gedichtenbox/blob/main/fig/paper_transport2.jpg?raw=true)


## How to move and install

The typewriter makes the pillar top heavy. It is essential to install additional weights at the bottom to make sure the machine can used safely in a public space, without risk of toppling over.

Before moving the machine, use the key to open the door on the back to remove any weights, if present.

![Picture of the paper feed button](https://github.com/turingbirds/gedichtenbox/blob/main/fig/pillar_weights.jpg?raw=true)


## How to set up the Raspberry Pi

Set the locale to en_US.UTF-8. Check this with ``python -c "import locale;print(locale.getdefaultlocale())"`` (also as superuser). See ``/etc/default/locale``.


### Thermal printer

Use python-escpos. Install from git as their PyPI entry is outdated: https://github.com/python-escpos/python-escpos Make sure to init and update the submodule.

Test using ``scripts/printer_demo.py``.

For more information, see: https://mike42.me/blog/what-is-escpos-and-how-do-i-use-it


### Auto-mount USB drives

Use pyudev (install using ``pip install pyudev``). See ``scripts/auto_mount_usb_drive.py``. Note that this script needs to run as superuser (sudo).


### Set up the Gedichtenbox script

```bash

cd
git clone https://github.com/turingbirds/gedichtenbox
crontab -e
```

```
@reboot cd /home/gedichtenbox/gedichtenbox/scripts ; sudo /usr/bin/python3 /home/gedichtenbox/gedichtenbox/scripts/auto_usb_mount.py
@reboot cd /home/gedichtenbox/gedichtenbox/scripts ; sleep 10 ; sudo /usr/bin/python3 /home/gedichtenbox/gedichtenbox/scripts/start_up_printer.py
@reboot cd /home/gedichtenbox/gedichtenbox/scripts ; sleep 20 ; /usr/bin/python3 /home/gedichtenbox/gedichtenbox/scripts/gedichtenbox.py
```


## Credits

This project was commissioned by [Cultura Mosae](https://culturamosae.nl) for Dag van de Poëzie, January 25th, 2024, in collaboration with [Centrummanagement Maastricht](https://cmmaastricht.nl/).

![Logo CMM](https://github.com/turingbirds/gedichtenbox/blob/main/fig/logo_cmm_small.png?raw=true)

![Logo Cultura Mosae](https://github.com/turingbirds/gedichtenbox/blob/main/fig/logo_cultura_mosae_small.png?raw=true)


## License

[Open source hardware](https://www.oshwa.org/) is hardware for which the design is made publicly available, so that anyone can study, modify, distribute, make, and sell the design or hardware based on that design, subject to the following license conditions.

Hardware licensed under the *CERN Open Hardware Licence Version 2 - Weakly Reciprocal,* a copy of which is included in this repository at [cern_ohl_w_v2.txt](https://github.com/turingbirds/ping-clock/blob/master/cern_ohl_w_v2.txt>).

Software licensed under the *Apache License 2.0,* a copy of which is included at [apache_license_2.0.txt](https://github.com/turingbirds/ping-clock/blob/master/apache_license_2.0.txt).
