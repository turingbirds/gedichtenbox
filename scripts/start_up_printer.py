# -*- coding: utf-8 -*-

"""
Automatically start the printer by toggling the relay connected to the power on button.

This script is part of the Gedichtenbox: https://github.com/turingbirds/gedichtenbox
"""

import RPi.GPIO as GPIO
import time

from escpos.printer import Usb


try:
	p = Usb(0x0416, 0x5011, profile="RP-F10-80mm", in_ep=0x81, out_ep=0x02) #0416:5011
	p.text("\n")
	printer_found = True
except:
	printer_found = False

print("Printer found: " + str(printer_found))

#
# 	configure GPIO output to toggle the printer "on" switch
#

if not printer_found:
	GPIO.setmode(GPIO.BCM)
	pin_number = 12
	GPIO.setup(pin_number, GPIO.OUT)
	GPIO.output(pin_number, GPIO.HIGH)
	time.sleep(3)
	GPIO.output(pin_number, GPIO.LOW)
