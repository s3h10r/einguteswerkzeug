#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import sys
from PIL import Image, ImageDraw, ImageFont
from einguteswerkzeug.helpers import get_resource_file, show_error
from einguteswerkzeug.helpers.gfx import paste_image_into_box #legacy

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---


def make_polaroid(source, size, options, template = None, template_box = None, bg_color_inner=(255,255,255),color_border=(255,255,255), size_border = 3, LEGACY_CONST = {}):
    """
    Converts an image into polaroid-style. This is the (legacy) main-function
    of the old module. It is exposed and can still be imported and used by
    any Python-Script.

    returns
        PIL image instance
    """
    img = None
    if isinstance(source,Image.Image):
        img= source
    else:
        img = Image.open(source)
    if not options['crop']:
        img = _add_border(img, size_border, color_border)
    if not options['noframe']: # if pasting into a template (for example a polaroid frame) is wanted #2
        if template:
            img = paste_image_into_box(source_image=img, target_image = template, blend = None, box = template_box)
        else:
            img = _add_frame(img)
    return img

def _add_border(image, border_size = 3, color_border = (0,0,0)):
    w, h = image.size
    assert(w==h)
    img = Image.new("RGBA", (w + border_size, h + border_size), color_border)
    img.paste(image, (border_size,border_size))
    return img

def _add_frame(image):
    """
    adds the frame around the image
    """
    log.critical("_add_frame support dropped for now (#13). please consider using a Template")
    sys.exit(1)
