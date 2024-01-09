# -*- coding: utf-8 -*-

"""
Gedichtenbox main script

https://github.com/turingbirds/gedichtenbox
"""

import subprocess
import board
import busio
from adafruit_pca9685 import PCA9685
import RPi.GPIO as GPIO
import os
import time
import sys


min_time_between_prints = 3

languages = ["Mestreechs", "Nederlands", "English"]

# where to read the poems from: this file contains a string indicating the actual device path to read from
usb_device_path_fname = "/tmp/usb_device_path"



#
# 	configure LED PWM
#

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c, address=0x41)
pca.frequency = 1000
max_duty = 0xFFFF
cutter_servo_min_duty = 35000
cutter_servo_max_duty = 65000
init_duty = [0, max_duty // 3, 2 * max_duty // 3]
duty = init_duty.copy()
fast_duty_step = 300
slow_duty_step = 100
duty_step = [slow_duty_step, slow_duty_step, slow_duty_step]



#
# 	wait for start_up_printer.py to turn the printer on
#

time.sleep(5)



#
# 	configure button input
#

GPIO.setmode(GPIO.BCM)
pin_numbers = [25, 24, 23]
for pin_number in pin_numbers:
	GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)

time_of_last_print = 0


#
# 	index all the poems on the USB drive
#

poems = {} # mapping of language string -> list of absolute poem filenames
poem_idx = {language: 0 for language in languages}  # set initial poem index

successfully_read = False
while not successfully_read:
	try:
		f = open(usb_device_path_fname, "r")
		usb_device_path = f.readlines()[0].strip()
		f.close()
		successfully_read = True
	except:
		print("Could not open " + usb_device_path_fname + " for reading poems")
		#sys.exit(1)

	time.sleep(1)


for language in languages:

	print("Finding poems for language '" + language + "' from " + os.path.join(usb_device_path, "poems",  language))

	poems[language] = []

	for root, dirs, files in os.walk(os.path.join(usb_device_path, "poems", language)):
		poems[language] = [os.path.join(root, fname) for fname in files]

	print("-> Found " + str(len(poems[language])) + " poems")


#
# 	paper feed motor off
#

pca.channels[3].duty_cycle = 0


#
# 	main loop
#

process = None

timer = 0.

STATE_IDLE = 0
STATE_PRINTING = 6
STATE_CUT_WAIT_FOR_FEED = 1
STATE_CUT_1 = 2
STATE_CUT_2 = 3

state = STATE_IDLE

last_time = time.time()
pca.channels[15].duty_cycle = cutter_servo_max_duty

while True:

	#
	# 	update LED brightness
	#

	for ch in range(3):
		if (duty_step[ch] > 0 and duty[ch] + duty_step[ch] >= max_duty) or (duty_step[ch] < 0 and duty[ch] + duty_step[ch] < 0):
			duty_step[ch] = -duty_step[ch]
		else:
			duty[ch] += duty_step[ch]
		pca.channels[ch].duty_cycle = duty[ch]

	#
	# 	read input
	#

	input_state = [1 - int(GPIO.input(pin_number)) for pin_number in pin_numbers]
	language = None
	button_idx = -1
	for i in range(len(languages)):
		if input_state[i]:
			language = languages[i]
			button_idx = 2 - i
			break

	if state == STATE_IDLE and language and time.time() - time_of_last_print > min_time_between_prints:
		# print!
		state = STATE_PRINTING
		print("Printing: " + str(language))
		time_of_last_print = time.time()

		# turn on paper feed motors
		pca.channels[3].duty_cycle = max_duty

		# blink only the selected language button
		for i in range(len(languages)):
			duty_step[i] = 0
			duty[i] = 0

		duty_step[button_idx] = fast_duty_step

		# do the actual print
		poem_fname = poems[language][poem_idx[language]]
		try:
			process = subprocess.Popen(["sudo", "python3", "print_poem.py", "--filename", poem_fname])
		except:
			pass

		# set the index for the next poem
		poem_idx[language] = (poem_idx[language] + 1) % len(poems[language])

	if process and process.poll() is not None:
		# print finished
		process = None

		timer = 0
		state = STATE_CUT_WAIT_FOR_FEED

	timer += time.time() - last_time
	last_time = time.time()

	if state == STATE_CUT_WAIT_FOR_FEED and timer > 3:
		pca.channels[15].duty_cycle = cutter_servo_min_duty
		state = STATE_CUT_1
		timer = 0
	elif state == STATE_CUT_1 and timer > 1:
		pca.channels[15].duty_cycle = cutter_servo_max_duty
		state = STATE_CUT_2
		timer = 0
	elif state == STATE_CUT_2 and timer > 12:
		# turn off paper feed motors
		pca.channels[3].duty_cycle = 0
		state = STATE_IDLE
		timer = 0

		# re-init LED duty cycles
		for i in range(len(languages)):
			duty_step[i] = slow_duty_step
			duty[i] = init_duty[i]

		time_of_last_print = time.time()

	#time.sleep(.01)
