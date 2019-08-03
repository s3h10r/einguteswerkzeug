#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TODO #13
"""
import glob
import logging
import os
import random
import string
import sys
from PIL import Image
from einguteswerkzeug.helpers import get_resource_file

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

RESOURCE_CONFIG_FILE="einguteswerkzeug.conf"

class EGWTemplate:
    """
    provides the interface for working with a template.

    properties with `_max`-suffix represent the maximum values for the template
    without need for upscaling it (and nope, we don't upscale).
    """

    BOX_FORMATS = { 'square' : 0, 'free' : 10}
    l_search_paths = [
        os.path.dirname(os.path.realpath(__file__)) + "/../templates/", ]

    def __init__(self, name = None, box = [], box_format = BOX_FORMATS['square']):
        self._IFACE_VERSION = "0.4.0"
        self._name = name
        self._fqfn = None
        self._box_format = box_format
        for s_path in self.l_search_paths:
            for fn in glob.iglob('%s/**/*' % (s_path), recursive = True):
                if os.path.basename(fn) == self._name: #gotcha
                    self._fqfn = fn
                    log.debug("template '{}' found in s_path '{}'.".format(self._name,s_path))
                    log.debug("fqfn : '{}'.".format(self._fqfn))
                    break
            if self._fqfn:
                break
        if not self._fqfn:
            raise Exception("couldn't find template {} in search_paths: {}".format(self._name, self.l_search_paths))
        self._box_max = box
        self._box = self._box_max
        self._tpl_image_max = Image.open(self._fqfn)
        self._tpl_image = Image.open(self._fqfn)

        if self._box_format != self.BOX_FORMATS['square']:
            raise Exception("Sorry, only format 'square' is supported yet. #6")
        # --- check if box-definition is a square & auto-correct if not
        w_max, h_max = self.box_size_max[0], self.box_size_max[1]
        if w_max != h_max:
            log.warning("boxdefinition for template '{}' is not a square. w,h {}".format(self.name,self.box_size_max))
            log.warning("difference is {}".format(abs(h_max-w_max)))
            # the longer side is made equal to the shorter side by removing pixels on both ends
            if w_max < h_max:
                diff = h_max - w_max
                self._box_max[1] += int(diff // 2)
                self._box_max[3] -= int(diff // 2) + int(diff % 2)
            else:
                diff = w_max - h_max
                self.box_max[0] += int(diff // 2)
                self.box_max[2] -= int(diff // 2) + int(diff % 2)
            self._box = self._box_max
            w_max, h_max = self.box_size_max
            log.warning("boxdefinition for template '{}' auto-adjusted to: {}".format(self.name,self.box_size_max))
            log.warning("boxdefinition is now: {}".format(box))
            assert(w_max == h_max)
            assert(self.box_size_max == self.box_size)
            # ---
            log.debug("Template-init for '{}' succeeded.".format(self._name))
            self._result_available = False # False until first .paste() call

    @property
    def iface_version(self):
        """
        returns interface version
        """
        return self._IFACE_VERSION


    @property
    def name(self):
        return self._name


    @property
    def fqfn(self):
        return self._fqfn


    @property
    def box_format(self):
        """
        returns format of the paste-area (box) human-readable
        """
        for k,v in self.BOX_FORMATS.items():
            if v == self._box_format:
                return k


    @property
    def info(self):
        """
        shows infos about the current state of the template
        """
        tpl_doc = string.Template("""
        iface_v     : $iface_version
        name        : $name
        box_format  : $box_format # (the format of the paste-area)
        fqfn        : $fqfn

        size_max      : $size_max
        size          : $size

        box_size_max  : $box_size_max
        box_size      : $box_size

        box_max       : $box_max
        box           : $box

        search_paths  : $s_paths
        """)
        return tpl_doc.substitute({
            'iface_version' : self.iface_version,
            'name' : self.name,
            'box_format' : self.box_format,
            'fqfn' : self.fqfn,
            'size_max' : self.size_max,
            'size' : self.size,
            'box_size_max' : self.box_size_max,
            'box_size' : self.box_size,
            'box_max' : self.box_max,
            'box' : self.box,
            's_paths' : self.search_paths,
            })


    @property
    def help(self):
        return self.info()


    @property
    def search_paths(self):
        return self.l_search_paths


    @property
    def size_max(self):
        """
        returns
            tuple(w,h) : max width, height of the template
        """
        return self._tpl_image_max.size


    @property
    def size(self):
        """
        returns
            tuple(w,h) : current width, height of the template
        """
        return self._tpl_image.size


    @property
    def box_size_max(self):
        """
        returns
            tuple(w,h) : width, height of the max paste-area for template
                         without upscaling the template
        """
        w = int(self.box_max[2] - self.box_max[0])
        h = int(self.box_max[3] - self.box_max[1])
        return (w,h)

    @property
    def box_size(self):
        """
        returns
            tuple(w,h) : width, height of the current paste-area for template
        """
        w = int(self.box[2] - self.box[0])
        h = int(self.box[3] - self.box[1])
        return (w,h)


    @property
    def box_max(self):
        """
        returns
                list(left, upper, right, lower) - positioning of the max-sized paste-area
        """
        return self._box_max


    @property
    def box(self):
        """
        returns
                list(left, upper, right, lower) - positioning of the current paste-area
        """
        return self._box


    def paste(image, alpha_blend = 1.0, max = False):
        """
        pastes Image instance into the .box of the template

        returns
            Image instance
        """
        raise Exception("TODO #13")


    def resize(self,**kwargs):
        """
        resizes template (and changes the .box, .size, ... properties accordingly)
        """
        raise Exception("TODO #13")


    def get_image(self):
        """
        btw. don't forget to call .paste() first

        returns
            Image instance with pasted image in template
        """
        if self._result_available:
            return self._tpl_image
        else:
            log.critical("please call .paste() etc. first - the template paste-area is still empty...")
            return None


def _load_templates(config = None):
    """
    loads templatedefinition & params from provided configfile
    returns list of Template-instances
    """
    templates = {} # template-instances
    configfile = get_resource_file(config)
    TEMPLATE_BOXES = None
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
    for k in TEMPLATE_BOXES:
        TEMPLATE_BOXES[k] = [int(round(f)) for f in TEMPLATE_BOXES[k]]
    for k,v in TEMPLATE_BOXES.items():
        templates[k] = EGWTemplate(name=k, box = list(v))
    log.info("{} templates loaded.".format(len(templates.keys())))
    return templates


def _select_template(name = None, templates = {}):
    if name.endswith('random') or name.endswith('rand'):
        log.info("choosing a random template...")
        tpl_keys = list(templates.keys())
        i = random.randint(0,len(tpl_keys) - 1)
        return templates[tpl_keys[i]]
    if name in templates:
        return templates[name]
    else:
        raise Exception("Sorry. Template not found. :-/")


if __name__ == '__main__':
    templates = _load_templates(config = RESOURCE_CONFIG_FILE)
    for name, tpl in templates.items():
        print(tpl.info)
        img = tpl.get_image()

    tpl = _select_template(name = 'egw-template_rodion-kutsaev-IJ25m7fXqtk-unsplash.jpg', templates = templates)
    print(tpl.info)

    tpl = _select_template(name = 'random', templates = templates)
    print(tpl.info)
