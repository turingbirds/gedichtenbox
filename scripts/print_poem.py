# -*- coding: utf-8 -*-

"""
Print a poem with its filename given as command-line parameter.

This script is part of the Gedichtenbox: https://github.com/turingbirds/gedichtenbox
"""

import time
import os
import sys
import argparse

from escpos.printer import Usb
from PIL import Image, ImageDraw, ImageFont


def chop_image_into_blocks(image_file, block_height):

    fnames = []
    with Image.open(image_file) as img:
        # Calculate the number of blocks
        img_width, img_height = img.size
        num_blocks = img_height // block_height + (img_height % block_height > 0)

        # Create a directory to store the blocks
        base_name = os.path.splitext(image_file)[0]
        os.makedirs(f"{base_name}_blocks", exist_ok=True)

        # Save each block
        for i in range(num_blocks):
            top = i * block_height
            bottom = min((i + 1) * block_height, img_height)
            block = img.crop((0, top, img_width, bottom))
            fname = f"{base_name}_blocks/block_{i}.png"
            block.save(fname)
            fnames.append(fname)

    return fnames


def do_print(filename_png, chop=True):
	p = Usb(0x0416, 0x5011, profile="RP-F10-80mm", in_ep=0x81, out_ep=0x02) #0416:5011

	if not chop:
		p.image(filename_png)
	else:
		time_between_blocks = 1
		fnames = chop_image_into_blocks(filename_png, 100)
		for fname in fnames:
			p.image(fname)
			time.sleep(time_between_blocks)

	p.text("\n\n\n\n\n\n")
	p.text("\n\n\n\n\n\n")

	p.cut()

	p.text("\n\n\n\n")



def create_image_with_text(poem_lines, font_path, image_width, header_image_path=None, footer_image_path=None, poem_title="", poem_author="", font_size=32, title_font_size=36, author_font_size=32, margin_author=20):
    # Load font
    font = ImageFont.truetype("Tinos-Regular.ttf", font_size)
    font_title = ImageFont.truetype("Tinos-Bold.ttf", title_font_size)
    font_author = ImageFont.truetype("Tinos-Italic.ttf", author_font_size)

    # Calculate image height
    line_height = font.getsize('A')[1] + 5  # Adjust spacing as needed

    header_height = 0
    if header_image_path:
        header_image = Image.open(header_image_path)
        header_height = header_image.height

    title_height = 0
    if poem_title:
        title_height = font_title.getsize('A')[1] + 15  # Adjust spacing as needed

    text_height = line_height * len(poem_lines)

    author_height = 0
    if poem_author:
        author_height = font_author.getsize('A')[1] + 15  # Adjust spacing as needed

    footer_height = 0
    if footer_image_path:
        footer_image = Image.open(footer_image_path)
        footer_height = footer_image.height

    image_height = header_height + title_height + text_height + margin_author + author_height + footer_height

    # Create image
    image = Image.new('RGB', (image_width, image_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw
    if header_image_path:
        image.paste(header_image, (0, 0))

    if poem_title:
        draw.text((10, header_height), poem_title, font=font_title, fill=(0, 0, 0))

    y_position = header_height + title_height
    for line in poem_lines:
        draw.text((10, y_position), line.strip(), font=font, fill=(0, 0, 0))
        y_position += line_height

    if poem_author:
        y_position += margin_author
        draw.text((10, y_position), poem_author, font=font_author, fill=(0, 0, 0))
        y_position += author_height

    if footer_image_path:
        image.paste(footer_image, (0, y_position))

    # Save or display the image
    image.save('output_image.png')
    #image.show()

parser = argparse.ArgumentParser()
parser.add_argument('--filename', help='the poem file to process')
args = parser.parse_args()
text_file_path = args.filename
print(f"The provided file name is: {text_file_path}")

if not text_file_path:
    print("File not found!")
    sys.exit(1)

# read text file
with open(text_file_path, 'r') as file:
    lines = file.readlines()

poem_title = lines[0]
poem_author = lines[1]
poem_lines = lines[2:]

# the header and  footer image should be 576 px wide
create_image_with_text(poem_lines, '', 576, '../fig/header.png', '../fig/footer.png', poem_title=poem_title, poem_author=poem_author)

do_print("output_image.png")
