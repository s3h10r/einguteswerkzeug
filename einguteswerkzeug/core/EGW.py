#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TODO #13 - transition of legacy code into class-based
"""

import glob
import logging
import os
import random
import string
import sys
from PIL import Image
from pluginbase import PluginBase
from einguteswerkzeug.helpers import get_resource_file, show_error
from einguteswerkzeug.plugins import EGWPluginFilter, EGWPluginGenerator
from einguteswerkzeug.core.template import EGWTemplate, load_templates, select_template

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

class EGW:
    __version__ = (0,3,90)

    l_searchpaths_filters = [os.path.dirname(os.path.realpath(__file__)) + "/../plugins/filters/", ]
    l_searchpaths_generators = [os.path.dirname(os.path.realpath(__file__)) + "/../plugins/generators/", ]
    _plugin_base = PluginBase(package='einguteswerkzeug.pluginframework')
    _plugin_source_filters = _plugin_base.make_plugin_source(searchpath=l_searchpaths_filters)
    _plugin_source_generators = _plugin_base.make_plugin_source(searchpath=l_searchpaths_generators)
    _PLUGINS_FILTERS = {}
    _PLUGINS_GENERATORS = {}
    _TEMPLATES = {}

    _RESOURCE_CONFIG_FILE="einguteswerkzeug.conf"
    # Font for the caption text
    _RESOURCE_FONT      = "fonts/default.ttf"
    _RESOURCE_FONT_SIZE = None

    def __init__(self, *args, **kwargs):
        self._IFACE_VERSION = "0.4.0"
        self._load_plugins()
        log.info("filters registered: {}".format(len(self.filters)))
        log.info("generators registered: {}".format(len(self.generators)))
        self._seed = None
        self._setup_args(**kwargs)
        if not self._seed:
            self._seed = random.randrange(sys.maxsize)
        random.seed(self._seed)
        self._process_args()
        # ... apply_filters, ...


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


    def _setup_args(self,**kwargs):
        # ---
        # Colors
        COLOR_FRAME   = (237, 243, 214)
        COLOR_BORDER  = (0, 0, 0)
        COLOR_TEXT_TITLE = (58, 68, 163)
        COLOR_TEXT_DESCR = COLOR_TEXT_TITLE
        COLOR_BG_INNER = (0,0,0)                # usefull if --nocrop
        # ---
        
        self._options = { 'rotate': None, 'crop' : True, 'noframe' : False} # defaults
        self._source = []
        self._size_box = (400,400) # inner size, only the picture without surrounding frame
        self._target = None
        self._align = "center"
        self._title = ""
        self._add_meta_to_title = False
        self._f_font = None
        self._template = None
        self._configfile = get_resource_file(self._RESOURCE_CONFIG_FILE)
        self._max_size = None # max size (width)
        self._add_exif_to_title = None
        self._alpha_blend = None
        self._bg_color_inner = COLOR_BG_INNER
        self._nopolaroid = False
        self._border_size = None           # only used  in combination with --no-polaroid
        self._border_color = (255,255,255) # only used  in combination with --no-polaroid
        self._apply_filters = None
        self._params_filter = []

        # process options
        if kwargs['<source-image>']:
            self._source = kwargs['<source-image>'].split(',') # some filters require a list of images ('composite', ...)
        if len(self._source) == 1:
            self._source = self._source[0]
        log.debug("source : %s" % self._source)
        self._generator = None
        if self._source and not isinstance(self._source, list):
            if self._source.lower() in('-', 'stdin'):
                raise Exception("hey, great idea! :) reading from STDIN isn't supported yet but it's on the TODO-list.")
        elif not self._source:
            self._generator = kwargs['--generator'] # surpriseme :)
            if not self._generator in self._PLUGINS_GENERATORS:
                show_error("Hu? Sorry generator '%s' unknown. Valid choices are: %s" % (generator, PLUGINS_GENERATORS.keys()))
        self._params_generator = []
        if kwargs['--params-generator']:
            self._params_generator = kwargs['--params-generator'].split('}')
            self._params_generator = [el + '}' for el in self._params_generator if el != '' ]
        log.debug("params_generator: %s" % self._params_generator)
        # overwriting the default-kwargs for generators with user-provided settings
        for i,pjson in enumerate(self._params_generator): # should only be 1 generator
            log.info("generator %s : loading & applying --params-generator %s '%s'" % (self._generator, i, pjson))
            params = json.loads(pjson)
            for k,v in params.items():
                if k in self._PLUGINS_GENERATORS[generator].kwargs:
                    self._PLUGINS_GENERATORS[generator].kwargs = {'k' : v}
                else:
                    raise Exception("generator '%s' provides no parameter '%s'. please check your --params-generator argument(s)." % (self._params_generator[i], k))
        if kwargs['--alpha-blend']:
            self._alpha_blend = float(args['--alpha-blend'])
        if kwargs['--border-size']:
            self._border_size = float(args['--border-size'])
        if kwargs['--border-color']:
            self._border_color = tuple([int(el) for el in kwargs['--border-color'].split(',')])
            assert(len(border_color)==3)
        if kwargs['--clockwise']:
            self._options['rotate'] = 'clockwise'
        elif kwargs['--anticlock']:
            self._options['rotate'] = 'anticlockwise'
        if kwargs['--crop']:
            self._options['crop'] = True
        elif kwargs['--nocrop']:
            self._options['crop'] = False
        if kwargs['--noframe']:
            self._options['noframe'] = True # using no polaroid nor any other template at all, outputs only the (maybe filtered) image
        if kwargs['--nopolaroid']:
            self._nopolaroid = True # using an other template thang polaroid
        if kwargs['--size-inner']:
            self._size_box = int(args['--size-inner'])
        if kwargs['--alignment']: # only used if --crop
            self._align = args['--alignment']
        if kwargs['--title']:
            self._title = args['--title']
        if kwargs['--title-meta']:
            self._add_meta_to_title = True # exif data | infos about choosen generator's-params
        if kwargs['--font']:
            self._f_font = args['--font']
        else:
            self._f_font = _RESOURCE_FONT
        if kwargs['--output']:
            self._target = args['--output']
        if kwargs['--template']:
            self._template = args['--template']
        if kwargs['--config']:
            self._configfile = args['--config']
        if args['--filter']:
            self._apply_filters = kwargs['--filter'].split(',')
            for filter in self._apply_filters:
                if filter not in self._PLUGINS_FILTERS:
                    show_error("Hu? Filter '%s' not available. Valid choices are: %s" % (filter, self._PLUGINS_FILTERS))
        if kwargs['--params-filter']:
            self._params_filter = args['--params-filter'].split('}')
            self._params_filter = [el + '}' for el in self._params_filter if el != '' ]
        log.debug("params_filter: %s" % self._params_filter)
        # overwriting the default-kwargs for filters with user-provided settings
        for i,pjson in enumerate(self._params_filter):
            log.info("filter %s : loading & applying --params-filter %s '%s'" % (self._apply_filters[i], i, pjson))
            params = json.loads(pjson)
            for k,v in params.items():
                if k in self._PLUGINS_FILTERS[apply_filters[i]].kwargs:
                    self._PLUGINS_FILTERS[apply_filters[i]].kwargs[k] = v
                else:
                    raise Exception("filter %s has no parameter '%s'. please check your --params-filter argument(s)." % (self._apply_filters[i], k))
        # ---
        if self._template:
            self._size_box = None # needs to be calculated
        if args['--max-size']:
            self._max_size = int(args['--max-size'])

        self._TEMPLATES = load_templates(configfile)

        if self._size_box and isinstance(self._size_box,int):
            self._size_box = (self._size_box,self._size_box) #square format

        if self._template:
            self._template = select_template(name=self._template, templates = self._TEMPLATES)
            self._size_box = self._template.size_box_max
            tpl_size = self._template.size_max
            # --- polaroid frame specific, needs refactoring, see issue #6
            self._LEGACY_IMAGE_TOP = self._template.box_max[1]
            self._LEGACY_IMAGE_BOTTOM = tpl_size[1] - (self._LEGACY_IMAGE_TOP + self._size_box[1])
            self._LEGACY_IMAGE_LEFT = self._template.box_max[0]
            self._LEGACY_IMAGE_RIGHT = tpl_size[0] - (self._LEGACY_IMAGE_LEFT + self._size_box[0])
            self._LEGACY_BORDER_SIZE  = 3
            self._RESOURCE_FONT_SIZE = int(self._LEGACY_IMAGE_BOTTOM - (self._LEGACY_IMAGE_BOTTOM * 0.2))
            # ---
        else:
            # --- polaroid frame specific, needs refactoring, see issue #6
            self._LEGACY_POLAROID_IMAGE_TOP    = int(self._size_box[0] / 16)     # added space on top
            self._LEGACY_POLAROID_IMAGE_BOTTOM = int(self._size_box[0] / 5.333)  # added space on bottom
            self._LEGACY_POLAROID_IMAGE_LEFT   = int(self._size_box[0] / 16)     # ...
            self._LEGACY_POLAROID_IMAGE_RIGHT  = int(self._size_box[0] / 16)     # ...
            self._LEGACY_POLAROID_BORDER_SIZE  = 3
            self._RESOURCE_FONT_SIZE = int(IMAGE_BOTTOM - (IMAGE_BOTTOM * 0.9))

            # ...

    def _process_args(self):
        """
        TODO migrateme (legacy) #13
        """
        # -- here we go...
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
            kwargs = PLUGINS_GENERATORS[generator].kwargs
            # TODO #11 if --size-inner or --max-size we can set generator kwargs['size'] to this already
            # for this the generator interface should provide always a tuple(size) ...
            if 'size' in kwargs:
                size_gen = kwargs['size']
                if isinstance(size_gen,tuple):
                    kwargs['size'] = size
                else:
                    log.warning("deprecated : generator {} doesn't provide 'size' parameter as tuple yet".format(generator))
            else:
                log.warning("deprecated : generator {} doesn't provide 'size' parameter".format(generator))
            generator = PLUGINS_GENERATORS[generator]
            source = generator.run()
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
                source_inst.append(Image.open(source))
            else:
                for src in source:
                    source_inst.append(Image.open(src))
            source = source_inst
        else:
            source = [source]
        source_unprep = source
        source = []
        if not isinstance(max_size,tuple):
            max_size=(max_size,max_size)
        for el in source_unprep:
            # do downsizing and cropping etc. befor applying filters
            log.info("size: {} max_size: {} image-input size: {}".format(size,max_size,el.size))
            if not isinstance(el,Image.Image):
                raise Exception("Ouch. Holy crap... wt..?!? ")
            if max_size and (max_size[0]*max_size[1] < el.size[0] * el.size[1]):
                log.warning("input-image can be downsized before applying filters etc..... TODO #11")
            if nopolaroid:
                bg_color_inner = border_color
            source.append(scale_and_prep_image(source = el, size = size, options = options, align = align, bg_color_inner= bg_color_inner))
        for el in source:
            log.info("size: {} max_size: {} image-input size after preproc: {}".format(size,max_size,source[-1].size))
        if len(source) == 1:
            source = source[0]
        if apply_filters:
            log.info("... start applying --filter(s): {}".format(apply_filters))
            if len(apply_filters) == 1:
                log.info("btw. did you know that you can chain filters via comma-seperator filter1,filter2,...? just sayin' that's fun. :)")
            custom_args_set = False
            if len(params_filter) > 0:
                custom_args_set = True
            img = _apply_filters(image=source, filters = apply_filters, custom_args_set = custom_args_set)
            source = img
            log.info("ok. filter(s) finished.")


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
