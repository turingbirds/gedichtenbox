# -*- coding: utf-8 -*-

"""
Automatically mount USB drives when they are inserted.

Note that this script has to be run as superuser.

This script is part of the Gedichtenbox: https://github.com/turingbirds/gedichtenbox
"""

import time
import os
import pyudev
import subprocess


def write_string_to_file(fname: str, s: str):
	with open(fname, "w") as file:
		file.write(s)


def list_usb_devices():
	context = pyudev.Context()
	usb_drivers = []
	for device in context.list_devices(subsystem="block"):
		print("\tdevice sys_name: " + str(device.sys_name))
		print("\tdevice driver: " + str(device.driver))
		if "ID_USB_DRIVER" in device:
			usb_drivers.append(device)
	return usb_drivers


while True:
	usb_devices = list_usb_devices()
	print("Listed " + str(len(usb_devices)) + " devices")
	for device in usb_devices:
            device_path = device.device_node
            mount_point = f"/mnt/{device.get('ID_FS_LABEL', 'usb_drive')}"

            try:
                os.makedirs(mount_point, exist_ok=True)
                subprocess.run(['mount', device_path, mount_point], check=True)
                print(f"Mounted {device_path} at {mount_point}")
                write_string_to_file(fname="/tmp/usb_device_path", s=mount_point)
            except subprocess.CalledProcessError as e:
                print(f"Error mounting {device_path}: {e}")

	time.sleep(1)
