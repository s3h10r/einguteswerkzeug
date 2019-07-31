#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import datetime as dt
import json
import os
import random
import site
import sys
import logging
from docopt import docopt
import exifread
from PIL import Image, ImageDraw, ImageFont, ExifTags
from pluginbase import PluginBase

from einguteswerkzeug.helpers import get_resource_file, show_error
from einguteswerkzeug.helpers.gfx import get_exif
from einguteswerkzeug.helpers.gfx import add_border_around_image, crop_image_to_square, scale_image_to_square, scale_image, scale_square_image

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

# Image size constraints
IMAGE_SIZE   = (600,600)                # the thumbnail size (= the inner picture)
# --- polaroid frame specific, needs refactoring, see issue #6
IMAGE_TOP    = int(IMAGE_SIZE[0] / 16)     # added space on top
IMAGE_BOTTOM = int(IMAGE_SIZE[0] / 5.333)  # added space on bottom
IMAGE_LEFT   = int(IMAGE_SIZE[0] / 16)     # ...
IMAGE_RIGHT  = int(IMAGE_SIZE[0] / 16)     # ...
BORDER_SIZE  = 3
# ---
# Colors
COLOR_FRAME   = (237, 243, 214)
COLOR_BORDER  = (0, 0, 0)
COLOR_TEXT_TITLE = (58, 68, 163)
COLOR_TEXT_DESCR = COLOR_TEXT_TITLE
COLOR_BG_INNER = (0,0,0)                # usefull if --nocrop
# Font for the caption text
RESOURCE_FONT      = "fonts/default.ttf"
RESOURCE_FONT_SIZE = int(IMAGE_BOTTOM - (IMAGE_BOTTOM * 0.9))
RESOURCE_CONFIG_FILE="einguteswerkzeug.conf"

TEMPLATE_BOXES = {} # if --template is used we need a dict with templatename and box-definition for the image
TEMPLATE = None

plugin_base = PluginBase(package='einguteswerkzeug.pluginframework')
plugin_source_dummy = plugin_base.make_plugin_source(
    searchpath=[os.path.dirname(os.path.realpath(__file__)) + "/../plugins/dummy/", ])
plugin_source_filters = plugin_base.make_plugin_source(
    searchpath=[os.path.dirname(os.path.realpath(__file__)) + "/../plugins/filters/", ])
subdirs = [os.path.dirname(os.path.realpath(__file__)) + "/../plugins/generators/"]
subd = [x[0] for x in os.walk(os.path.dirname(os.path.realpath(__file__)) + "/../plugins/generators/")]
for d in subd:
    subdirs.append(d)
print(subdirs)
plugin_source_generators = plugin_base.make_plugin_source(searchpath=subdirs)

PLUGINS_DUMMY = {}
PLUGINS_FILTERS = {}
PLUGINS_GENERATORS = {}

__version__ = (0,3,28)

def get_version():
    return(__version__)

# ---

def _register_plugins():
    global PLUGINS_TESTS
    global PLUGINS_FILTERS
    global PLUGINS_GENERATORS
    #print(plugin_source_dummy.searchpath)
    for plug in plugin_source_dummy.list_plugins():
        log.info("loading dummy-plugin %s ... " % plug)
        plug_instance = plugin_source_dummy.load_plugin(plug)
        PLUGINS_DUMMY[plug_instance.name] = plug_instance
    log.info("loading filter-plugins from %s" % plugin_source_filters.searchpath)
    for plug in plugin_source_filters.list_plugins():
        plug_instance = plugin_source_filters.load_plugin(plug)
        try:
            plug_name = plug_instance.name
        except:
            log.warning("loading of %s failed. no .name set?" % plug)
            continue
        PLUGINS_FILTERS[plug_instance.name] = plug_instance
        log.info("filter '%s' successfully loaded" % plug_instance.name)

    log.debug("loading generator-plugins from %s" % plugin_source_generators.searchpath)
    log.debug("generators.list_plugins %s" % plugin_source_generators.list_plugins())
    for plug in plugin_source_generators.list_plugins():
            log.info("plug try : %s" % plug)
            plug_instance = plugin_source_generators.load_plugin(plug)
            # dirty way to check if file is a valid plugin: has it a name atrribute -> then it's valid for now...
            try:
                plug_name = plug_instance.name
            except:
                continue
            if plug_name in PLUGINS_GENERATORS:
                log.warning("loading generator-plugin '%s' skipped because of name-conflict" % plug_name)
                continue
            PLUGINS_GENERATORS[plug_instance.name] = plug_instance
            log.info("generator '%s' successfully loaded" % plug_instance.name)

def setup_globals(size, configfile=None, template = None, show = True):
    global IMAGE_SIZE
    global IMAGE_TOP
    global IMAGE_BOTTOM
    global IMAGE_LEFT
    global IMAGE_RIGHT
    global BORDER_SIZE
    global RESOURCE_FONT_SIZE
    global TEMPLATE_BOXES
    global TEMPLATE

    if size and isinstance(size,tuple):
        size = list(size) # we need to chhnge values in this func, so temporarily turning into list
    elif size and not isinstance(size,list):
        size = [size,size] #square format

    if configfile:
        if not (os.path.isfile(configfile)):
            log.warning("configfile {} not found... please always give absolute paths to config-file to avoid confusions :D".format(configfile))
            sys.exit(1)
        # --- load config file (if any)
        with open(configfile) as f:
            log.info("reading config...")
            code = compile(f.read(), configfile, 'exec')
            global_vars ={}
            local_vars = {}
            exec(code,global_vars, local_vars)
            TEMPLATE_BOXES=local_vars['TEMPLATE_BOXES']
    else:
        if template:
            log.critical("to use --template you need to define a config-file")
            sys.exit(1)

    if not template:
        IMAGE_SIZE   = size
        IMAGE_TOP    = int(IMAGE_SIZE[0] / 16)
        IMAGE_BOTTOM = int(IMAGE_SIZE[0] / 5.333)
        IMAGE_LEFT   = int(IMAGE_SIZE[0] / 16)
        IMAGE_RIGHT  = int(IMAGE_SIZE[0] / 16)
        BORDER_SIZE  = 3
        RESOURCE_FONT_SIZE = int(IMAGE_BOTTOM - (IMAGE_BOTTOM * 0.2))
    else:
        # calculate the values based on the properties of the template image
        # --- setup templates
        for k in TEMPLATE_BOXES:
            TEMPLATE_BOXES[k] = [int(round(f)) for f in TEMPLATE_BOXES[k]]
        # ---
        if template.endswith('random') or template.endswith('rand'):
            log.info("choosing a random template...")
            templates = list(TEMPLATE_BOXES.keys())
            rnd = random.randint(0,len(TEMPLATE_BOXES) - 1)
            template = os.path.dirname(template) + "/" + templates[rnd]
        TEMPLATE=template
        box = TEMPLATE_BOXES[os.path.basename(template)]
        w = box[2] - box[0]
        h = box[3] - box[1]
        if w != h:
            log.warning("boxdefinition for template {} is not a square. w,h {},{}".format(template,w,h))
            log.warning("difference is {}".format(abs(h-w)))
            log.warning("auto-fixing => making it square...")
            # the longer side is made equal to the shorter side by removing pixels on both ends
            if w < h:
                diff = h - w
                box[1] += int(diff // 2)
                box[3] -= int(diff // 2) + int(diff % 2)
            else:
                diff = w - h
                box[0] += int(diff // 2)
                box[2] -= int(diff // 2) + int(diff % 2)
            TEMPLATE_BOXES[os.path.basename(template)] = [box[0], box[1], box[2], box[3]]
            box = TEMPLATE_BOXES[os.path.basename(template)]
            w = box[2] - box[0]
            h = box[3] - box[1]
            log.warning("boxdefinition for template {} auto-adjusted to: w,h {},{}".format(os.path.basename(template),w,h))
            log.warning("boxdefinition is now: {}".format(box))
            assert(w == h)
        size = [w,h]
        assert((size[0] == w) and (size[0]== h)) # only squares supported for now because of legacy #6
        IMAGE_SIZE = tuple(size) # no further edits of this
        # overwrite the above calculated  _TOP,_BOTTOM, ... values
        # by the one our template "dictates"
        try:
            tpl = Image.open(template)
        except:
            tpl = Image.open(get_resource_file(template))
        tpl_x, tpl_y = tpl.size
        tpl.close()
        IMAGE_TOP = box[1]
        IMAGE_BOTTOM = tpl_y - (IMAGE_TOP + IMAGE_SIZE[1])
        IMAGE_LEFT = box[0]
        IMAGE_RIGHT = tpl_x - (IMAGE_LEFT + w)
        BORDER_SIZE  = 3
        RESOURCE_FONT_SIZE = int(IMAGE_BOTTOM - (IMAGE_BOTTOM * 0.2))
    # --- show
    if show:
        SETTINGS = {
        'IMAGE_SIZE' : IMAGE_SIZE,
        'IMAGE_TOP' : IMAGE_TOP,
        'IMAGE_BOTTOM' : IMAGE_BOTTOM,
        'IMAGE_LEFT' : IMAGE_LEFT,
        'IMAGE_RIGHT' : IMAGE_RIGHT,
        'BORDER_SIZE' : BORDER_SIZE,
        'RESOURCE_FONT_SIZE' : RESOURCE_FONT_SIZE,
        'TEMPLATE_KEY' : TEMPLATE,
        'TEMPLATE_VALUE': None,# we fill this if template ist != None
        'PLUGINS_DUMMY' : list(PLUGINS_DUMMY.keys()),
        'PLUGINS_FILTERS' : list(PLUGINS_FILTERS.keys()),
        'PLUGINS_GENERATORS' : list(PLUGINS_GENERATORS.keys()),
        }
        if template:
            SETTINGS['TEMPLATE_KEY'] = os.path.basename(TEMPLATE),
            SETTINGS['TEMPLATE_VALUE'] = TEMPLATE_BOXES[os.path.basename(TEMPLATE)],
        for k in list(PLUGINS_DUMMY.keys()):
            SETTINGS["plugins.example." + k + ".description"] = PLUGINS_DUMMY[k].description
            SETTINGS["plugins.example." + k + ".description"] = PLUGINS_DUMMY[k].version
            SETTINGS["plugins.example." + k + ".kwargs"] = PLUGINS_DUMMY[k].kwargs
            SETTINGS["plugins.example." + k + ".author"] = PLUGINS_DUMMY[k].author
        for k in list(PLUGINS_FILTERS.keys()):
            SETTINGS["plugins.filters." + k + ".description"] = PLUGINS_FILTERS[k].description
            SETTINGS["plugins.filters." + k + ".version"] = PLUGINS_FILTERS[k].version
            SETTINGS["plugins.filters." + k + ".kwargs"] = PLUGINS_FILTERS[k].kwargs
            SETTINGS["plugins.filters." + k + ".author"] = PLUGINS_FILTERS[k].author
        for k in list(PLUGINS_GENERATORS.keys()):
            SETTINGS["plugins.generators." + k + ".description"] = PLUGINS_GENERATORS[k].description
            SETTINGS["plugins.generators." + k + ".version"] = PLUGINS_GENERATORS[k].version
            SETTINGS["plugins.generators." + k + ".kwargs"] = PLUGINS_GENERATORS[k].kwargs
            SETTINGS["plugins.generators." + k + ".author"] = PLUGINS_GENERATORS[k].author
        print(json.dumps(SETTINGS,indent=4,sort_keys=True))

def make_polaroid(source, size, options, align, title, f_font = None, font_size = None, template = None, bg_color_inner=(255,255,255),filter_func=None):
    """
    Converts an image into polaroid-style. This is the (legacy) main-function of the module
    and it is exposed. It can be imported and used by any Python-Script.

    returns
        PIL image instance
    """
    caption = title
    img_in = None
    if isinstance(source,Image.Image):
        img_in = source
    else:
        img_in = Image.open(source)
    img_in.load()
    img = rotate_image(img_in, options['rotate'])
    [w, h] = img.size
    # Determine ratio of image length to width to
    # determine oriantation (portrait, landscape or square)
    image_ratio = float(float(h)/float(w))
    log.debug("image_ratio: %f size_w: %i size_h: %i" % (image_ratio, w, h))
    if round(image_ratio, 1) >= 1.3: # is_portrait
        log.info("source image ratio is %f (%s)" % (image_ratio, 'is_portrait'))
    elif round(image_ratio, 1) == 1.0: # is_square
        log.info("source image ratio is %f (%s)" % (image_ratio, 'is_square'))
    elif round(image_ratio, 1) <= 0.8: # is_landscape
        log.info("source image ratio is %f (%s)" % (image_ratio, 'is_landscape'))
    if options['crop']:
        img = crop_image_to_square(img, align)
    else:
        img = scale_image_to_square(img, bg_color=bg_color_inner)
        img = _add_border(img, BORDER_SIZE, COLOR_BORDER)
    img = scale_square_image(img, size)
    if filter_func:
        img = filter_func(img)
    if not options['noframe']: # if pasting into a template (for example a polaroid frame) is wanted #2
        if template:
            img = _paste_into_template(image=img, template=template)
            description = None
            img = add_text(img, caption, description, f_font = f_font, font_size = font_size)
        else:
            img = add_frame(img)
            description = None
            img = add_text(img, caption, description, f_font = f_font, font_size = font_size)
    return img

def apply_template(source = None, template = None, size = None, align = "center",  options = None, border_size_fact = None, border_color = (255,255,255) ):
    """
    **inprogress** - a more generic alternative to (legacy) make_polaroid

    resizes source-image to fit into template and
    pastes image into template (for now only square-area supported! #6)

    returns
        PIL image instance
    """
    if isinstance(source,Image.Image):
        img = source
    else:
        img = Image.open(source)
    [w, h] = img.size
    # Determine ratio of image length to width to
    # determine oriantation (portrait, landscape or square)
    image_ratio = float(float(h)/float(w))
    log.debug("image_ratio: %f size_w: %i size_h: %i" % (image_ratio, w, h))
    if round(image_ratio, 1) >= 1.3: # is_portrait
        log.info("source image ratio is %f (%s)" % (image_ratio, 'is_portrait'))
    elif round(image_ratio, 1) == 1.0: # is_square
        log.info("source image ratio is %f (%s)" % (image_ratio, 'is_square'))
    elif round(image_ratio, 1) <= 0.8: # is_landscape
        log.info("source image ratio is %f (%s)" % (image_ratio, 'is_landscape'))
    if options['crop']:
        img = crop_image_to_square(img, align)
    else:
        img = scale_image_to_square(img, bg_color=border_color)
    if not size: # set size to optimum depending on the template resolution
        size = _get_template_box_size(template)
    if border_size_fact and img.size[0] == img.size[1]:
        img = add_border_around_image(image = img, size = int(img.size[0] * border_size_fact), color = border_color)
    img = scale_square_image(img, size)
    log.warning("--template with --nopolaroid is experimental!")
    img = _paste_into_template(image=img, template=template)
    return img

def _get_template_box_size(template):
    """
    returns
        tuple(w,h) : width, height of the paste-area for template
    """
    box = TEMPLATE_BOXES[os.path.basename(template)]
    w = int(box[2] - box[0])
    h = int(box[3] - box[1])
    return (w,h)

def _paste_into_template(image = None, template = './templates/', box=None):
    """
    """
    if not box:
        box = TEMPLATE_BOXES[os.path.basename(template)]
        box_size = _get_template_box_size(template)
    else:
        w = int(box[2] - box[0])
        h = int(box[3] - box[1])
        box_size = (w,h)
    try:
        img_tpl = Image.open(template)
    except:
        img_tpl = Image.open(get_resource_file(template))
    # plausi check
    w = int(box[2] - box[0])
    h = int(box[3] - box[1])
    assert(box_size[0] == w and box_size[1] == h)
    # ---
    log.debug("box_size the picture will be pasted into is (w,h) {}".format(box_size))
    region2copy = image.crop((0,0,image.size[0],image.size[1]))
    if region2copy.size[0] > box_size[0]:
        # Downsample
        log.info("downsampling... (good)")
        region2copy = region2copy.resize(box_size,Image.ANTIALIAS)
    else:
        log.info("upscaling... (not so good ;)")
        region2copy = region2copy.resize(box_size, Image.BICUBIC)
    assert(region2copy.size == box_size)
    img_tpl.paste(region2copy,box)
    return img_tpl

def rotate_image(image, rotation):
    """
    rotates the image appropriately
    """
    if rotation == "clockwise":
        image = image.rotate(-90)
    elif rotation == "anticlockwise":
        image = image.rotate(90)
    return image

def _add_border(image, border_size = 3, color_border = COLOR_BORDER):
    w, h = image.size
    assert(w==h)
    img = Image.new("RGBA", (w + border_size, h + border_size), color_border)
    img.paste(image, (border_size,border_size))
    return img

def add_frame(image, border_size = 3, color_frame = COLOR_FRAME, color_border = COLOR_BORDER):
    """
    adds the frame around the image
    """
    frame = Image.new("RGB", (IMAGE_SIZE + IMAGE_LEFT + IMAGE_RIGHT, IMAGE_SIZE + IMAGE_TOP + IMAGE_BOTTOM), COLOR_BORDER)
    # Create outer and inner borders
    draw = ImageDraw.Draw(frame)
    draw.rectangle((BORDER_SIZE, BORDER_SIZE, frame.size[0] - BORDER_SIZE, frame.size[1] - BORDER_SIZE), fill = COLOR_FRAME)
    draw.rectangle((IMAGE_LEFT - BORDER_SIZE, IMAGE_TOP - BORDER_SIZE, IMAGE_LEFT + IMAGE_SIZE[0] + BORDER_SIZE, IMAGE_TOP + IMAGE_SIZE[1] + BORDER_SIZE), fill = COLOR_BORDER)
    # Add the source image
    frame.paste(image, (IMAGE_LEFT, IMAGE_TOP))
    return frame

def add_text(image, title = None, description = None, f_font = RESOURCE_FONT, font_size = RESOURCE_FONT_SIZE):
    """
    adds a title (string) to the image
    description is unused at the moment

    returns
        PIL Image instance
    """
    if (title is None) or (len(title)==0):
        return image
    size = font_size
    f_font = get_resource_file(f_font)
    try:
        font_title = ImageFont.truetype(f_font, font_size)
    except:
        show_error("Could not load resource '%s'." % f_font)
    width, height = font_title.getsize(title)
    while ((width > IMAGE_SIZE[1]) or (height > IMAGE_BOTTOM)) and (size > 0):
        size = size - 2
        try:
            font_title = ImageFont.truetype(f_font, font_size)
        except:
            show_error("Could not load resource '%s'." % f_font)
        font_title = ImageFont.truetype(get_resource_file(f_font), size)
        width, height = font_title.getsize(title)
        log.debug("searching suiting font_size... trying {}".format(size))
    if (size <= 0):
        showError("Text is too large")
    draw = ImageDraw.Draw(image)
    pos_x = (IMAGE_SIZE[0] + IMAGE_LEFT + IMAGE_RIGHT - width) / 2
    pos_y = IMAGE_SIZE[1] + IMAGE_TOP + ((IMAGE_BOTTOM - height)) / 2
    log.info("title fontsize {} pos_x, pos_y {},{}".format(size, pos_x, pos_y))
    draw.text(
        (pos_x, pos_y),
        title, font = font_title, fill = COLOR_TEXT_TITLE,
    )
    return image

def _apply_filters(image, filters = None, filters_args = None):
    """
    applies filter(s) to the image
    return PIL Image
    """
    img = image
    requires_lists = ('composite') # subset of filters which support processing of image-lists
    supports_lists = requires_lists # filters which support processing of image-lists
    is_list = isinstance(img, list)
    if is_list:
        log.info("got a list of images to apply filters for. only few filters are supporting this: %s" % supports_lists)
    kwargs = None
    for edit_filter in filters:
        filter_func = None
        if is_list and ( (edit_filter not in supports_lists)):
                log.warning("%s only supports one image as input (no lists) -> skipping %s" % edit_filter)
                continue
        elif is_list == False and edit_filter in requires_lists:
                log.warning("%s only supports multiple image as input but got only one. -> skipping %s" % (edit_filter, edit_filter))
                continue
        if edit_filter in ('ascii', 'ascii-color'):
            kwargs = PLUGINS_FILTERS[edit_filter].kwargs
            kwargs['image'] = img
            if edit_filter == 'ascii':
                kwargs['color'] = (0,0,0)
            else:
                kwargs['color'] = (0,0,240) #TODO choose random color
        elif edit_filter in ('composite'):
            kwargs = PLUGINS_FILTERS[edit_filter].kwargs
            kwargs['image'] = img
            kwargs['alpha'] = 0.5
        elif edit_filter in ('mosaic'):
            kwargs = PLUGINS_FILTERS[edit_filter].kwargs
            block_size = int(img.size[0] / random.randint(2,32))
            kwargs['image'] = img
            kwargs['block_size'] = block_size
        elif edit_filter in ('oil', 'oil2'):
            kwargs = PLUGINS_FILTERS[edit_filter].kwargs
            brush_size = random.randint(1,8)
            roughness = random.randint(1,255)
            kwargs['image'] = img
            kwargs['brush_size'] = brush_size
            kwargs['roughness'] = roughness
        elif edit_filter in ('pixelsort'):
            kwargs = PLUGINS_FILTERS[edit_filter].kwargs
            algos = [1,10,20]
            idx = random.randint(0,2)
            algo = algos[idx]
            kwargs['image'] = img
            kwargs['algo'] = algo
        else:
            # generic interface (kwargs always with 'image' and optionally with other arguments set to defaults)
            kwargs = PLUGINS_FILTERS[edit_filter].kwargs
            kwargs['image'] = img
        log.debug("%s kwargs = %s" % (edit_filter,kwargs))
        img = PLUGINS_FILTERS[edit_filter].run(**kwargs)
    return img

def main(args):
    rand_seed = random.randrange(sys.maxsize)
    random.seed(rand_seed)
    _register_plugins()
    options = { 'rotate': None, 'crop' : True, 'noframe' : False} # defaults
    source = []
    size = IMAGE_SIZE[0] # inner size, only the picture without surrounding frame
    target = None
    align = "center"
    title = ""
    f_font = None
    template = None
    configfile = get_resource_file(RESOURCE_CONFIG_FILE)
    max_size = None # max size (width) of the contactsheet
    add_exif_to_title = None
    bg_color_inner = COLOR_BG_INNER
    border_size = None           # only used  in combination with --no-polaroid
    border_color = (255,255,255) # only used  in combination with --no-polaroid
    # process options
    if args['<source-image>']:
        source = args['<source-image>'].split(',') # some filters require a list of images ('composite', ...)
    if len(source) == 1:
        source = source[0]
    log.debug("source : %s" % source)
    generator = None
    if source and not isinstance(source, list):
        if source.lower() in('-', 'stdin'):
            raise Exception("hey, great idea! :) reading from STDIN isn't supported yet but it's on the TODO-list.")
    elif not source:
        generator = args['--generator'] # surpriseme :)
        if not generator in PLUGINS_GENERATORS:
            show_error("Hu? Sorry generator '%s' unknown. Valid choices are: %s" % (generator, PLUGINS_GENERATORS.keys()))
    params_generator = []
    if args['--params-generator']:
        params_generator = args['--params-generator'].split('}')
        params_generator = [el + '}' for el in params_generator if el != '' ]
    log.debug("params_generator: %s" % params_generator)
    # overwriting the default-kwargs for filters with user-provided settings
    for i,pjson in enumerate(params_generator): # should only be 1 generator
        log.info("generator %s : loading & applying --params-generator %s '%s'" % (generator, i, pjson))
        params = json.loads(pjson)
        for k,v in params.items():
            if k in PLUGINS_GENERATORS[generator].kwargs:
                PLUGINS_GENERATORS[generator].kwargs[k] = v
            else:
                raise Exception("filter %s has no parameter '%s'. please check your --params-filter argument(s)." % (apply_filters[i], k))
    if args['--border-size']:
        border_size = float(args['--border-size'])
    if args['--border-color']:
        border_color = tuple([int(el) for el in args['--border-color'].split(',')])
        assert(len(border_color)==3)
    if args['--clockwise']:
        options['rotate'] = 'clockwise'
    elif args['--anticlock']:
        options['rotate'] = 'anticlockwise'
    if args['--crop']:
        options['crop'] = True
    elif args['--nocrop']:
        options['crop'] = False
    if args['--noframe']:
        options['noframe'] = True # using no polaroid nor any other template at all, outputs only the (maybe filtered) image
    nopolaroid = False
    if args['--nopolaroid']:
        nopolaroid = True # using an other template thang polaroid
    if args['--size-inner']:
        size = int(args['--size-inner'])
    if args['--alignment']: # only used if --crop
        align = args['--alignment']
    if args['--title']:
        title = args['--title']
    add_meta_to_title = False
    if args['--title-meta']:
        add_meta_to_title = True # exif data | infos about choosen generator's-params
    if args['--font']:
        f_font = args['--font']
    else:
        f_font = RESOURCE_FONT
    if args['--output']:
        target = args['--output']
    if args['--template']:
        template = args['--template']
    if args['--config']:
        configfile = args['--config']
    apply_filters = None
    if args['--filter']:
        apply_filters = args['--filter'].split(',')
        for filter in apply_filters:
            if filter not in PLUGINS_FILTERS:
                show_error("Hu? Filter '%s' not available. Valid choices are: %s" % (filter, PLUGINS_FILTERS))
    params_filter = []
    if args['--params-filter']:
        params_filter = args['--params-filter'].split('}')
        params_filter = [el + '}' for el in params_filter if el != '' ]
    log.debug("params_filter: %s" % params_filter)
    # overwriting the default-kwargs for filters with user-provided settings
    for i,pjson in enumerate(params_filter):
        log.info("filter %s : loading & applying --params-filter %s '%s'" % (apply_filters[i], i, pjson))
        params = json.loads(pjson)
        for k,v in params.items():
            if k in PLUGINS_FILTERS[apply_filters[i]].kwargs:
                PLUGINS_FILTERS[apply_filters[i]].kwargs[k] = v
            else:
                raise Exception("filter %s has no parameter '%s'. please check your --params-filter argument(s)." % (apply_filters[i], k))

    #plugins[filter[0]]

    # ---
    if template:
        size = None # needs to be calculated
    setup_globals(size, configfile, template)
    size = IMAGE_SIZE
    template = TEMPLATE
    if args['--max-size']:
        max_size = int(args['--max-size'])
    # here we go...
    if not isinstance(source, list):
        if add_meta_to_title:
            exif_data = get_exif(source)
            if ('EXIF DateTimeOriginal') in exif_data:
                v = exif_data['EXIF DateTimeOriginal']
                timestamp = dt.datetime.strptime(str(v), '%Y:%m:%d %H:%M:%S')
                meta = timestamp
            else:
                log.warning("--title-meta set but exif_data about DateTime unavailable for the input-image. :-/ : {}; ;".format(fn))
        name, ext = os.path.splitext(source)
        if not os.path.isfile(source):
            show_error("Source file '%s' does not exist." % source)
        if not target:
            target = name + ".polaroid.png"
        if not align in ("left", "right", "top", "bottom", "center"):
            show_error("Unknown alignment %s." % align)
    elif generator: # source can also be a generative art thingy
        if generator == 'psychedelic':
            kwargs = PLUGINS_GENERATORS[generator].kwargs
            generator = PLUGINS_GENERATORS[generator]
            source, meta = generator.run(**kwargs)
        else:
            kwargs = PLUGINS_GENERATORS[generator].kwargs
            generator = PLUGINS_GENERATORS[generator]
            source, meta = generator.run(**kwargs)
    if add_meta_to_title:
        if len(title) > 0:
            title += " "
        title += "%s" % (meta)
    # Prepare our resources
    f_font = get_resource_file(f_font)
    font_size = IMAGE_BOTTOM
    if not isinstance(source,Image.Image): # that's the case if we're not using a generator
        source_inst = []
        if not isinstance(source,list):
            source_inst = Image.open(source)
        else:
            for src in source:
                source_inst.append(Image.open(src))
        source = source_inst
    if apply_filters:
        log.warning("--filter is experimental. you can chain filters via comma-seperator filter1,filter2,...")
        img = _apply_filters(image=source, filters = apply_filters, filters_args = [])
        source = img
    if not nopolaroid:
        # finally create the polaroid.
        img = make_polaroid(
            source = source, size = size, options = options, align =align,
            title = title, f_font = f_font, font_size = font_size,
            template = template,
            bg_color_inner = bg_color_inner,
            )
    else:
        img = apply_template(source = source, template = template, size = size, align = align, options = options, border_size_fact=border_size, border_color = border_color)
        description = None
        img = add_text(img, title, description, f_font = f_font, font_size = font_size)
    log.debug("size: %i %i" % (img.size[0], img.size[1]))
    # ---  if --max-size is given: check if currently bigger and downscale if necessary...
    if max_size:
        xs, ys = img.size
        if (xs > max_size) or (ys > max_size):
            log.info('scaling result down to --max_size %i' % max_size)
            factor = 1
            if xs >= ys:
                factor = max_size / xs
            else:
                factor = max_size / ys
            x_new = int(img.width * factor)
            y_new = int(img.height * factor)
            img = img.resize((x_new,y_new),Image.ANTIALIAS)
    # yai, finally ... :)
    log.info("seed %f" % rand_seed)
    img.save(target)
    print(target)
