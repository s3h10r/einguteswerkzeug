#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import cmd
import logging
import json
import pydoc
import string
from pluginbase import PluginBase
from einguteswerkzeug.helpers import editor, confirm_prompt
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

__version__ = (0,1,0)


class EGWShell(cmd.Cmd):
    """
    An interactive line-oriented command interpreter for
    einguteswergzeug (egw).
    """
    __version__ = __version__
    intro = 'Welcome to egw-shell ({}). Type help or ? to list commands.\n'.format('.'.join(str(i) for i in __version__))
    prompt = '(egw) '
    egw = None # egw instance
    # ---colors ... MAGENTA YELLOW LIGHTBLUE_EX LIGHTGREEN_EX CYAN LIGHTCYAN_EX
    # TODOP3 move to config-file
    #color_prompt = Fore.LIGHTGREEN_EX
    color_prompt = Fore.GREEN
    color_gen  = Fore.LIGHTCYAN_EX
    color_gen2 = Fore.CYAN
    color_flt  = Fore.LIGHTYELLOW_EX
    color_flt2 = Fore.YELLOW
    # ---

    def __init__(self, *args, **kwargs):
        print(kwargs)
        self.egw = EGW(**kwargs)
        super().__init__()

    def do_EOF(self, line):
        return True

    def preloop(self):
        print(self.color_prompt)

    def postloop(self):
        print(Style.RESET_ALL)

    def postcmd(self, stop, line):
        print(self.color_prompt)

    def do_listGenerators(self):
        """
        list available generators
        """
        for i, g in enumerate(self.egw.generators.values()):
            print(self.color_gen + "{} {} - {}".format(i, g.name, g.description) + Style.RESET_ALL)

    def do_generators(self, arg):
        """
        list available generators
        """
        self.do_listGenerators()

    def do_listFilters(self,arg):
        """
        list available filters
        """
        print(self.color_flt)
        for i, f in enumerate(self.egw.filters.values()):
            print("{} {} - {}".format(i, f.name, f.description))
        print(Style.RESET_ALL)

    def do_filters(self, arg):
        """
        list available filters
        """
        self.do_listFilters(None)

    def do_detailGenerator(self, generator):
        """detailGenerator [generator]
        shows details about generator. if no arg: active generator is used.
        """
        if not generator:
            g = self.egw.generator
        else:
            g = self.egw.generators[generator]

        header  = "{}".format(g.name)
        header  += "\n" +"="*len(g.name)
        tpl = string.Template("""
help
----
$help

parameters ('--params-generator')
---------------------------------
$kwargs
        """)
        content = tpl.substitute({
            'kwargs' : json.dumps(g.kwargs,sort_keys=True, indent=4),
            'help'   : g.help,
        })
        page = "{}\n{}".format(header,content)
        print(self.color_gen)
        pydoc.pager(page)
        
    def do_setGenerator(self, generator):
        """setGenerator [generator]
        sets active generator. if no arg: shows details about active generator"
        """
        print(self.color_gen)
        if generator:
            self.egw.generator = generator
        self.do_detailGenerator(generator)

    def do_generator(self, generator):
        """generator [generator]
        sets active generator. if no arg: shows details about active generator"
        """
        self.do_setGenerator(generator)

    def do_paramsGenerator(self, arg):
        """paramsGenerator [parameters]
        edit parameters (kwargs) of active generator.
        equivalent to '--params-generator=' on console.

        optional args:
            parameters (string) : generator's parameters in json-format

        Example:
            paramsGenerathor {"seed":1372403442, "colors":["#ff0000", "#00ff00", "#0000ff"]}' 
        """
        params = self.egw.generator.kwargs
        if not arg:
            params = json.dumps(params)
        else:
            params = arg
        params = json.dumps(json.loads(params), indent=4, sort_keys=True) # prettify
        status_msg = colored("ok.", "green")
        finished = False
        while not finished:
            params = editor(params)
            try:
                self.egw.generator.kwargs = json.loads(params)
            except:
                print(colored("Ouch! Could not parse parameters...", "green"))
                finished = not confirm_prompt("Wanna re-edit?")
                print(finished)
            else:
                print(colored("ok.", "green"))
                finished = True

    def do_editGenerator(self, arg):
        """alias of paramsGenerator"""
        self.do_paramsGenerator(arg)

    # ...

    def do_run(self, arg):
        """
        run (egw-)job
        """
        print("TODO")

    def do_printCLI(self, arg):
        """
        generate suiting egw command (handy for copy'n'paste)
        """
        print("TODO")

def main(kwargs):
    init()
    egwsh = EGWShell(**kwargs)
    egwsh.cmdloop()
