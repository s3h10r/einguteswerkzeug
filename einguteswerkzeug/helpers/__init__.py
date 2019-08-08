#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging
import os
import site
import sys

import exifread
from PIL import Image

PACKAGE_NAME = "einguteswerkzeug"

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
# ---

def get_resource_file(basefile, PACKAGE_NAME = PACKAGE_NAME):
    """
    gets the fully qualified name of a resource file
    """
    fqn = os.path.join(os.path.dirname(os.path.realpath(__file__)), basefile)
    if not os.path.isfile(fqn):
        # when installed via pip the package_data (see MANIFEST.in, setup.py)
        # should be located somewhere in site-packages path of the (virtual-)env
        for dir in site.getsitepackages():
            fqn = dir + "/" + PACKAGE_NAME + "/" + basefile
            if os.path.isfile(fqn):
                return fqn
                break
    return fqn

def show_error(msg):
    """
    Show an error message and exit
    """
    log.critical("Error: %s" % msg)
    sys.exit(1)
