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
from pluginbase import PluginBase
from einguteswerkzeug.helpers import get_resource_file
from einguteswerkzeug.plugins import EGWPluginFilter, EGWPluginGenerator

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

RESOURCE_CONFIG_FILE="einguteswerkzeug.conf"

class EGW:
    __version__ = (0,3,90)
    l_searchpaths_filters = [os.path.dirname(os.path.realpath(__file__)) + "/../plugins/filters/", ]
    l_searchpaths_generators = [os.path.dirname(os.path.realpath(__file__)) + "/../plugins/generators/", ]

    _plugin_base = PluginBase(package='einguteswerkzeug.pluginframework')
    _plugin_source_filters = _plugin_base.make_plugin_source(searchpath=l_searchpaths_filters)
    _plugin_source_generators = _plugin_base.make_plugin_source(searchpath=l_searchpaths_generators)

    _PLUGINS_FILTERS = {}
    _PLUGINS_GENERATORS = {}

    def __init__(self,*args, **kwargs):
        self._IFACE_VERSION = "0.4.0"
        self._load_plugins()
        log.info("filters registered: {}".format(len(self.filters)))
        log.info("generators registered: {}".format(len(self.generators)))
        # ...

    def _load_plugins(self):
        """
        searches for plugins and registers / loads them class-wide
        """
        log.debug("loading filter-plugins from %s" % self._plugin_source_filters.searchpath)
        for plug in self._plugin_source_filters.list_plugins():
            plug_instance = self._plugin_source_filters.load_plugin(plug)
            try:
                if isinstance(plug_instance.filter, EGWPluginFilter):
                    log.debug("{} provides a EGWPluginFilter-instance. iface_v : {}".format(plug_instance.filter.name, plug_instance.filter.iface_version))
            except:
                continue
            if plug_instance.filter.name in self._PLUGINS_FILTERS:
                log.warning("loading filter-plugin '%s' skipped because of name-conflict :/" % plug_instance.filter.name)
                continue
            self._PLUGINS_FILTERS[plug_instance.filter.name] = plug_instance.filter
            log.info("filter '%s' successfully loaded" % plug_instance.filter.name)

        log.debug("loading generator-plugins from %s" % self._plugin_source_generators.searchpath)
        log.debug("generators.list_plugins %s" % self._plugin_source_generators.list_plugins())
        for plug in self._plugin_source_generators.list_plugins():
                plug_instance = self._plugin_source_generators.load_plugin(plug)
                try:
                    if isinstance(plug_instance.generator, EGWPluginGenerator):
                        log.debug("{} provides a EGWPluginGenerator-instance. iface_v: {}".format(plug_instance.generator.name, plug_instance.generator.iface_version))
                except:
                    continue
                if plug_instance.generator.name in self._PLUGINS_GENERATORS:
                    log.warning("loading generator-plugin '%s' skipped because of name-conflict :/" % plug_instance.generator.name)
                    continue
                self._PLUGINS_GENERATORS[plug_instance.generator.name] = plug_instance.generator
                log.info("generator '%s' successfully loaded" % plug_instance.generator.name)

    @property
    def filters(self):
        """
        returns
            list : names of filter-plugins available
        """
        return list(self._PLUGINS_FILTERS.keys())


    @property
    def generators(self):
        """
        returns
            list : names of generator-plugins available
        """
        return list(self._PLUGINS_GENERATORS.keys())

    @property
    def version(self):
        """
        returns
            string : version of einguteswerkzeug
        """
        return self.__version__

    @property
    def info(self):
        """
        shows infos about the current state of the template
        """
        tpl_doc = string.Template("""
        version     : $version
        filters     : $len_filters
        filters     : $filters
        generators  : $len_generators
        generators  : $generators
        """)
        return tpl_doc.substitute({
            'version' : self.version,
            'len_filters' : len(self.filters),
            'filters' : self.filters,
            'len_generators' : len(self.generators),
            'generators' : self.generators,
            })


    @property
    def help(self):
        return self.info()


if __name__ == '__main__':
    egw = EGW()
    print(egw.info)
