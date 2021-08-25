#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
some helper funcs
"""
import json
import logging
import os
import site
import subprocess
import sys
import tempfile

import exifread
from PIL import Image

PACKAGE_NAME = "einguteswerkzeug"

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
if log.hasHandlers():
    log.andlers.clear()
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.propagate=False
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

def editor(text=None, default_editor="vi"):
    """
    Open an editor (environment variable EDITOR).
    Allows to edit (given) text like the functionality
    that happens when doing 'git commit' on the console. 

    args:
        text (string): the text to edit

    optional args:
        default_editor (string) : editor to use if environment varibale 
                                  EDITOR is not set

    returns:
        string: the edited text
    """
    fd, fname = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as f:
        f.write(text)
    cmd = os.environ.get('EDITOR', default_editor) + ' ' + fname
    subprocess.call(cmd, shell=True)
    with open(fname, 'r') as f:
        res = f.read()
    os.unlink(fname)
    return res

def confirm_prompt(question: str, yes_by_default = True) -> bool:
    """
    Shows a yes/no question.

    example:

        >>> reply = confirm_prompt("Are you sure?")
        >>> print(reply)

    args:
        yes_by_default (bool) : if True just hitting return equals yes.

    returns:
        bool : True if ansered with yes. False if answerded with no.
    """
    replies_prompt = "y/n"
    replies_values = ["y", "n"]
    yes = ("y")
    if yes_by_default: 
        replies.add("")
        replies_prompt = "Y/n"
        yes = ("", "y")
    reply = None
    while reply not in ("", "y", "n"):
        reply = input(f"{question} ({replies_prompt}): ").lower()
    return (reply in yes)
