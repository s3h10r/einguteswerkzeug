#!/usr/bin/env python3
"""
https://stackoverflow.com/questions/10615901/trim-whitespace-using-pil

* gets the border colour from the top left pixel, using getpixel, so you don't need to pass the colour.
* Subtracts a scalar from the differenced image, this is a quick way of saturating all values under 100, 100, 100
  (in my example) to zero. So is a neat way to remove any 'wobble' resulting from compression.
"""
import logging
import os
import sys
from PIL import Image, ImageChops

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

fn = sys.argv[1]
img = Image.open(fn)
img = trim(img)
target = "trimmed-" + os.path.basename(fn)
img.save(target)
print(target)
#img.show()
