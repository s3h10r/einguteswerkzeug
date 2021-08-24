#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import cmd
import logging
import string
from pluginbase import PluginBase
from einguteswerkzeug.plugins import EGWPluginFilter, EGWPluginGenerator
from einguteswerkzeug.core.template import EGWTemplate, load_templates, select_template
from einguteswerkzeug.core import EGW

import cli_ui
from colorama import init, Fore, Back, Style
from termcolor import colored

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.CRITICAL)
if log.hasHandlers():
    log.handlers.clear()
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.propagate=False
# ---

__version__ = (0,0,1)


class EGWShell(cmd.Cmd):
    """
    An interactive line-oriented command interpreter for
    einguteswergzeug (egw).
    """
    __version__ = __version__
    intro = 'Welcome to the egw-shell shell. Type help or ? to list commands.\n'
    prompt = '(egw) '
    egw = None # egw instance

    def __init__(self, *args, **kwargs):
        print(kwargs)
        self.egw = EGW(**kwargs)
        super().__init__()

    def do_EOF(self, line):
        return True

    def postloop(self):
        print

    def do_listGenerators(self,arg):
        """
        list available generators
        """
        #print(Fore.CYAN) #MAGENTA YELLOW LIGHTBLUE_EX LIGHTGREEN_EX CYAN LIGHTCYAN_EX
        for i, g in enumerate(self.egw.generators.values()):
            print(Fore.LIGHTBLUE_EX + "{} {} - {}".format(i, g.name, g.description) + Style.RESET_ALL)

    def do_listFilters(self,arg):
        """
        list available filters
        """
        print(Fore.CYAN)
        for i, f in enumerate(self.egw.filters.values()):
            print("{} {} - {}".format(i, f.name, f.description))
        print(Style.RESET_ALL)

    def do_detailGenerator(self, generator):
        """detailGenerator [generator]
        shows details about generator. if no arg: active generator is used.
        """
        if not generator:
            g = self.egw.generator
        else:
            g = self.egw.generators[generator]


        header  = "{}".format(g.name)
        tpl = string.Template("""
        help
        ----
        $help
        """)

        content = tpl.substitute({
            'help' : g.help,
        })

        print(Fore.LIGHTBLUE_EX + header)
        print("="*len(header))
        print(Fore.LIGHTBLUE_EX + content + Style.RESET_ALL)

    def do_setGenerator(self, generator):
        """setGenerator [generator]
        sets active generator. if no arg: shows details about active generator"
        """
        print(Fore.BLUE)
        if generator:
            self.egw.generator = generator
        self.do_detailGenerator(generator)

    def do_generator(self, generator):
        """generator [generator]
        sets active generator. if no arg: shows details about active generator"
        """
        self.do_setGenerator(generator)

def main(kwargs):
    init()
    egwsh = EGWShell(**kwargs)
    egwsh.cmdloop()
