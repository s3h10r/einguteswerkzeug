from collections import OrderedDict
import datetime as dt
import logging
from operator import itemgetter
import os

import exifread
from PIL import Image, ImageChops

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---


def get_exif(source):
    """
    """
    if isinstance(source, Image.Image):
        if hasattr(source, filename):
            source = source.filename
        else:
            raise Exception("Sorry, source is an Image-instance and i could not determine the filename. Please geve me a FQFN instead.")
    elif not isinstance(source, str):
        raise Exception("Ouch. Sorry, source must be a valid filename.")
    with open(source, 'rb') as f:
        exif_data = exifread.process_file(f, details=True)
    for tag in exif_data:
        log.debug("exif_data has key: %s" % (tag))
        if tag in ('Image DateTime', 'EXIF DateTimeOriginal'):
            log.debug("EXIF data of %s for key %s is %s" % (source, tag, exif_data[tag]))
    return exif_data

def get_images_in_dir(directory=None, suffix=('jpg','jpeg','png','gif', 'bmp', 'tif','tiff'),traversal=True):
    res = []
    if traversal:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(suffix):
                    fqfn = os.path.join(root, file)
                    res.append(fqfn)
                    log.debug("file match: {}".format(fqfn))
    else:
        for file in os.listdir(directory):
            if file.endswith(suffix):
                fqfn = os.path.join(directory, file)
                res.append(fqfn)
    return res

def sort_images_by_name(images):
    pass

def sort_images_by_time(images, exclude_on_no_data = True, reverse= True, return_meta = False):
    return sort_images_by_original_ctime(images, exclude_on_no_data = exclude_on_no_data, reverse = reverse, return_meta = return_meta)

def sort_images_by_original_ctime(images, exclude_on_no_data = True, reverse = True, return_meta = True):
    """
    """
    DATA_UNAVAIL = []
    meta = { }

    for fn in images:
        exif_data = get_exif(fn)
        if ('EXIF DateTimeOriginal') in exif_data:
            log.debug("exif_data about DateTime: {}; {}; {}".format(fn, exif_data['Image DateTime'], exif_data['EXIF DateTimeOriginal']))
            v = exif_data['EXIF DateTimeOriginal']
            timestamp = dt.datetime.strptime(str(v), '%Y:%m:%d %H:%M:%S')
            meta[fn] = timestamp
        else:
            log.debug("exif_data about DateTime unavailable: {}; ;".format(fn))
            DATA_UNAVAIL.append(fn)
    log.info("exif_data about DateTime unavailable for {} images.".format(len(DATA_UNAVAIL)))
    # create sorted list
    for k,v in meta.items():
        if (k == None) or (v == None):
            log.critical("Oooouch. This should not happen... :-/ %s,%s" % (k,v))
    meta_sorted = OrderedDict(sorted(meta.items(), key = itemgetter(1), reverse = reverse))
    sorted_list = meta_sorted.keys()
    sorted_list = list(sorted_list)
    if not exclude_on_no_data:
        sorted_list.append(DATA_UNAVAIL)
        for fn in DATA_UNAVAIL:
            meta_sorted[fn] = None
        log.warning("exlude_on_no_data={} => added {} images without exif-data.".format(exclude_on_no_data, len(DATA_UNAVAIL)))
    else:
        log.warning("exlude_on_no_data={} => skipped {} images without exif-data.".format(exclude_on_no_data, len(DATA_UNAVAIL)))
    if return_meta:
        return sorted_list, meta_sorted, DATA_UNAVAIL
    return sorted_list

def filter_images_by_time(images, exclude_on_no_data = True):
    pass

def filter_images_by_size(images, min_size, max_size = None):
    """
    usefull to find only high-resolution photos and kicking out
    thumbnails and junk on the fly
    """
    pass

def crop_image_to_square(image, align='center'):
    """
    crops the image into square-format

    returns cropped Image
    """
    # Do the cropping needed
    if image.size[0] > image.size[1]:
        if align in ("left", "top"):
            box = (0, 0, image.size[1], image.size[1])
        elif align in ("right", "bottom"):
            delta = image.size[0] - image.size[1]
            box = (delta, 0, image.size[0], image.size[1])
        elif align == "center":
            delta = (image.size[0] - image.size[1]) / 2
            box = (delta, 0, image.size[0] - delta, image.size[1])
        image = image.crop(box)
        image.load()
    elif image.size[1] > image.size[0]:
        if align in ("left", "top"):
            box = (0, 0, image.size[0], image.size[0])
        elif align in ("right", "bottom"):
            delta = image.size[1] - image.size[0]
            box = (0, delta, image.size[0], image.size[1])
        elif align == "center":
            delta = (image.size[1] - image.size[0]) / 2
            box = (0, delta, image.size[0], image.size[1] - delta)
        image = image.crop(box)
        image.load()
    # make sure we have a perfect square
    log.debug("cropped to size: %i %i" % (image.size[0], image.size[1]))
    if image.size[0] != image.size[1]:
        if image.size[0] > image.size[1]:
            box = (0, 0, image.size[1], image.size[1])
        else:
            box = (0, 0, image.size[0], image.size[0])
        image = image.crop(box)
        assert(image.size[0] == image.size[1])
        image.load()
        log.debug("re-cropped to size: %i %i" % (image.size[0], image.size[1]))
    return image

def scale_image_to_square(image, bg_color = (255,255,255)):
    img_w, img_h = image.size
    image_ratio = float(float(img_h)/float(img_w))
    add_border = 0
    if image_ratio < 1:
        add_border = image.size[0] * (( 1 + image_ratio ) / 64)
    else:
        add_border = image.size[1] * ((image_ratio - 1) / 64)
    add_border = int(add_border)
    background = None
    if image.size[0] > image.size[1]:
        background = Image.new('RGBA', (image.size[0] + add_border, image.size[0] + add_border), bg_color)
    elif image.size[1] > image.size[0]:
        background = Image.new('RGBA', (image.size[1] + add_border, image.size[1] + add_border), bg_color)
    else:
        return image # already square
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(image, offset)
    background.load()
    return background

def scale_square_image(image, size):
    """
    scales the (square) image to size (up-/downsampling)

    returns scaled image
    """
    if image.size[0] != image.size[1]:
        raise Exception("ouch - no square image.")
    if image.size[0] > size:
        # Downsample
        image = image.resize((size, size), Image.ANTIALIAS)
    else:
        image = image.resize((size, size), Image.BICUBIC)
    log.debug("scaled to size: %i %i" % (image.size[0], image.size[1]))
    return image

def scale_image(image, new_width=600):
    """
    scales the image to new_width while maintaining aspect ratio
    """
    new_w = new_width
    (old_w, old_h) = image.size
    aspect_ratio = float(old_h)/float(old_w)
    new_h = int(aspect_ratio * new_w)
    new_dim = (new_w, new_h)
    image = image.resize(new_dim)
    return image

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
