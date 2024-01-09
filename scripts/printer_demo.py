# -*- coding: utf-8 -*-

"""
Printer demo

This script is part of the Gedichtenbox: https://github.com/turingbirds/gedichtenbox
"""

from escpos.printer import Usb


demo_text = "The quick brown fox\n"

p = Usb(0x0416, 0x5011, profile="RP-F10-80mm", in_ep=0x81, out_ep=0x02) #0416:5011

p.set(font="a", align="left")
p.text(demo_text)
p.set(font="a", align="left", bold=False, double_width=True, double_height=False)
p.text(demo_text)
p.set(font="a", align="left", bold=False, double_width=False, double_height=True)
p.text(demo_text)
p.set(font="a", align="left", bold=False, double_width=True, double_height=True)
p.text(demo_text)
p.set(font="a", align="left", bold=True, double_width=False, double_height=False)
p.text(demo_text)
p.set(font="b", align="left", bold=False, double_width=False, double_height=False)
p.text(demo_text)

p.image("output_image.png")
p.cut()
