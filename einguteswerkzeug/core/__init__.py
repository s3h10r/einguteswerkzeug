#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
enjoy the mess ;) #13
the transition of the legacy code into class-based looks... ummm...
"not very pretty"... but it works so it's good enough for now.
"""
import datetime as dt
import glob
import json
import logging
import os
import random
import string
import sys
from PIL import Image
from pluginbase import PluginBase
from einguteswerkzeug.helpers import get_resource_file, show_error
from einguteswerkzeug.helpers.gfx import scale_and_prep_image, scale_square_image, add_border_around_image
from einguteswerkzeug.plugins import EGWPluginFilter, EGWPluginGenerator
from einguteswerkzeug.core.template import EGWTemplate, load_templates, select_template
from einguteswerkzeug.core.polaroid import make_polaroid # legacy #13

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

__version__ = (0,3,93)

class EGW:
    __version__ = __version__

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
    _RESOURCE_FONT_SIZE = 64

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
            self._alpha_blend = float(kwargs['--alpha-blend'])
        if kwargs['--border-size']:
            self._border_size = float(kwargs['--border-size'])
        if kwargs['--border-color']:
            self._border_color = tuple([int(el) for el in kwargs['--border-color'].split(',')])
            assert(len(self._border_color)==3)
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
            self._size_box = int(kwargs['--size-inner'])
        if kwargs['--alignment']: # only used if --crop
            self._align = kwargs['--alignment']
        if kwargs['--title']:
            self._title = kwargs['--title']
        if kwargs['--title-meta']:
            self._add_meta_to_title = True # exif data | infos about choosen generator's-params
        if kwargs['--font']:
            self._f_font = kwargs['--font']
        else:
            self._f_font = self._RESOURCE_FONT
        if kwargs['--output']:
            self._target = kwargs['--output']
        if kwargs['--template']:
            self._template = kwargs['--template']
        if kwargs['--config']:
            self._configfile = kwargs['--config']
        if kwargs['--filter']:
            self._apply_filters = kwargs['--filter'].split(',')
            for filter in self._apply_filters:
                if filter not in self._PLUGINS_FILTERS:
                    show_error("Hu? Filter '%s' not available. Valid choices are: %s" % (filter, self._PLUGINS_FILTERS))
        if kwargs['--params-filter']:
            self._params_filter = kwargs['--params-filter'].split('}')
            self._params_filter = [el + '}' for el in self._params_filter if el != '' ]
        log.debug("params_filter: %s" % self._params_filter)
        # overwriting the default-kwargs for filters with user-provided settings
        for i,pjson in enumerate(self._params_filter):
            log.info("filter %s : loading & applying --params-filter %s '%s'" % (self._apply_filters[i], i, pjson))
            params = json.loads(pjson)
            for k,v in params.items():
                if k in self._PLUGINS_FILTERS[self._apply_filters[i]].kwargs:
                    self._PLUGINS_FILTERS[self._apply_filters[i]].kwargs[k] = v
                else:
                    raise Exception("filter %s has no parameter '%s'. please check your --params-filter argument(s)." % (self._apply_filters[i], k))
        # ---
        if self._template:
            self._size_box = None # needs to be calculated
        if kwargs['--max-size']:
            self._max_size = int(kwargs['--max-size'])

        self._TEMPLATES = load_templates(self._configfile)

        if self._size_box and isinstance(self._size_box,int):
            self._size_box = (self._size_box,self._size_box) #square format

        if self._template:
            self._template = select_template(name=os.path.basename(self._template), templates = self._TEMPLATES)
            self._size_box = self._template.box_size


    def _process_args(self):
        """
        """
        # -- here we go...
        if not isinstance(self._source, list):
            if self._add_meta_to_title:
                exif_data = get_exif(source)
                if ('EXIF DateTimeOriginal') in exif_data:
                    v = exif_data['EXIF DateTimeOriginal']
                    timestamp = dt.datetime.strptime(str(v), '%Y:%m:%d %H:%M:%S')
                    meta = timestamp
                else:
                    log.warning("--title-meta set but exif_data about DateTime unavailable for the input-image. :-/ : {}; ;".format(fn))
            name, ext = os.path.splitext(self._source)
            if not os.path.isfile(self._source):
                show_error("Source file '%s' does not exist." % source)
            if not self._target:
                self._target = name + ".polaroid.png"
            if not self._align in ("left", "right", "top", "bottom", "center"):
                show_error("Unknown alignment %s." % self._align)
        elif self._generator: # source can also be a generative art thingy
            kwargs = self._PLUGINS_GENERATORS[self._generator].kwargs
            # TODO #11 if --size-inner or --max-size we can set generator kwargs['size'] to this already
            # for this the generator interface should provide always a tuple(size) ...
            if 'size' in kwargs:
                kwargs['size'] = self._size_box
            else:
                log.warning("deprecated : generator {} doesn't provide 'size' parameter".format(generator))
            generator = self._PLUGINS_GENERATORS[self._generator]
            self._source = generator.run()
        if self._add_meta_to_title:
            if len(self._title) > 0:
                self._title += " "
            self._title += "%s" % (meta)
        # Prepare our resources
        self._f_font = get_resource_file(self._f_font)
        if not isinstance(self._source,Image.Image): # that's the case if we're not using a generator
            source_inst = []
            if not isinstance(self._source,list):
                source_inst.append(Image.open(self._source))
            else:
                for src in self._source:
                    source_inst.append(Image.open(src))
            self._source = source_inst
        else:
            self._source = [self._source]
        source_unprep = self._source
        self._source = []
        if not isinstance(self._max_size,tuple):
            self._max_size=(self._max_size,self._max_size)
        for el in source_unprep:
            # do downsizing and cropping etc. befor applying filters
            log.info("size: {} max_size: {} image-input size: {}".format(self._size_box,self._max_size,el.size))
            if not isinstance(el,Image.Image):
                raise Exception("Ouch. Holy crap... wt..?!? ")
            if self._max_size and (self._max_size[0]*self._max_size[1] < el.size[0] * el.size[1]):
                log.warning("input-image can be downsized before applying filters etc..... TODO #11")
            if self._nopolaroid:
                self._bg_color_inner = self._border_color
            self._source.append(scale_and_prep_image(source = el, size = self._size_box, options = self._options, align = self._align, bg_color_inner= self._bg_color_inner))
        for el in self._source:
            log.info("size: {} max_size: {} image-input size after preproc: {}".format(self._size_box,self._max_size,self._source[-1].size))
        if len(self._source) == 1:
            self._source = self._source[0]


    def _do_filters(self, image, filters = None, custom_args_set = False):
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
            if not custom_args_set: # randomize params to get some unpredictable variations per default
                log.info("no custom parameters for filters set (--params-filter). applying parameter-randomization.")
                filter_func = None
                if is_list and ( (edit_filter not in supports_lists)):
                        log.warning("%s only supports one image as input (no lists) -> skipping %s" % edit_filter)
                        continue
                elif is_list == False and edit_filter in requires_lists:
                        log.warning("%s only supports multiple image as input but got only one. -> skipping %s" % (edit_filter, edit_filter))
                        continue
                if edit_filter in ('ascii', 'ascii-color'):
                    kwargs = self._PLUGINS_FILTERS[edit_filter].kwargs
                    kwargs['image'] = img
                    if edit_filter == 'ascii':
                        kwargs['color'] = (0,0,0)
                    else:
                        kwargs['color'] = (0,0,240)
                elif edit_filter in ('composite'):
                    kwargs = self._PLUGINS_FILTERS[edit_filter].kwargs
                    kwargs['image'] = img
                    kwargs['alpha'] = 0.5
                elif edit_filter in ('mosaic'):
                    kwargs = self._PLUGINS_FILTERS[edit_filter].kwargs
                    block_size = int(img.size[0] / random.randint(2,32))
                    kwargs['image'] = img
                    kwargs['block_size'] = block_size
                elif edit_filter in ('oil', 'oil2'):
                    kwargs = self._PLUGINS_FILTERS[edit_filter].kwargs
                    brush_size = random.randint(1,8)
                    roughness = random.randint(1,255)
                    kwargs['image'] = img
                    kwargs['brush_size'] = brush_size
                    kwargs['roughness'] = roughness
                elif edit_filter in ('pixelsort'):
                    kwargs = self._PLUGINS_FILTERS[edit_filter].kwargs
                    algos = [1,10,20]
                    idx = random.randint(0,2)
                    algo = algos[idx]
                    kwargs['image'] = img
                else:
                    # generic interface (kwargs always with 'image' and optionally with other arguments set to defaults)
                    kwargs = self._PLUGINS_FILTERS[edit_filter].kwargs
                    kwargs['image'] = img
                log.info("%s kwargs = %s" % (edit_filter,kwargs))
            else:
                log.info("custom parameters for filters set via --params-filter. therefore no parameter-randomization applied.")
                # generic interface (kwargs always with 'image' and optionally with other arguments set to defaults)
                kwargs = self._PLUGINS_FILTERS[edit_filter].kwargs
                kwargs['image'] = img
                log.info("%s kwargs = %s" % (edit_filter,kwargs))
            self._PLUGINS_FILTERS[edit_filter].kwargs = kwargs
            img = self._PLUGINS_FILTERS[edit_filter].run()

        return img


    def run(self):
        """
        apply filters, paste into template, generate output, save output
        returns
            Imagin instance : the final image is saved and also returned
        """
        # --- apply_filters
        if self._apply_filters:
            log.info("... start applying --filter(s): {}".format(self._apply_filters))
            if len(self._apply_filters) == 1:
                log.info("btw. did you know that you can chain filters via comma-seperator filter1,filter2,...? just sayin' that's fun. :)")
            custom_args_set = False
            if len(self._params_filter) > 0:
                custom_args_set = True
            img = self._do_filters(image=self._source, filters = self._apply_filters, custom_args_set = custom_args_set)
            self._source = img
            log.info("ok. filter(s) finished.")
        # --- finish the picture: paste it into the template,
        #     add borders, text, whatsoever ...
        if self._nopolaroid:
            options['alpha_blend'] = self._alpha_blend
            if isinstance(self._source,Image.Image):
                img = self._source
            else:
                img = Image.open(self._source)
            [w, h] = img.size
            assert(w == self._size_box[0])
            assert(h == self._size_box[1])
            if self._border_size_fact and (w == h):
                img = add_border_around_image(image = img, size = int(img.size[0] * border_size_fact), color = self._border_color)
            img = scale_square_image(img, self._size_box)
            log.warning("--template with --nopolaroid is experimental! alpha_blend: {}".format(options['alpha_blend']))
            img = self._template.paste(image=img, alpha_blend = self._alpha_blend)
            self._img = img
        else:
            if self._template:
                self._img = make_polaroid(source = self._source, size = self._size_box, options = self._options, template = self._template.image, template_box = self._template.box)
                if (self._title and self._title != ""):
                    f_kwargs = {'title' : self._title, 'font' : self._f_font, 'color' : (0,0,220)}
                    self._img = self._template.add_text(**f_kwargs)
            else:
                self._img = make_polaroid(source = self._source, size = self._size_box, options = self._options, template = None, template_box = None)
        log.debug("size: {}".format(self._img.size))
        # ---  if --max-size is given: check if currently bigger and downscale if necessary...
        if self._max_size:
            xs, ys = self._img.size
            if (xs > self._max_size[0]) or (ys > self._max_size[1]):
                log.info('scaling result down to --max_size {}'.format(self._max_size))
                factor = 1
                if xs >= ys:
                    factor = self._max_size[0] / xs
                else:
                    factor = self._max_size[1] / ys
                x_new = int(self._img.width * factor)
                y_new = int(self._img.height * factor)
                self._img_final = self._img.resize((x_new,y_new),Image.ANTIALIAS)
            else:
                self._img_final = self._img
        else:
            self._img_final = self._img
        self._img_final.save(self._target)
        print("saving final image...")
        print(self._target)
        return self._img_final

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
        version       : $version
        filters       : $len_filters
        filters       : $filters
        generators    : $len_generators
        generators    : $generators
        len_templates : $len_templates
        template      : $template
        templates     : $templates
        """)
        tpl_name = None
        if self._template:
            tpl_name = self._template.name
        return tpl_doc.substitute({
            'version' : self.version,
            'len_filters' : len(self.filters),
            'filters' : self.filters,
            'len_generators' : len(self.generators),
            'generators' : self.generators,
            'len_templates' : len(self._TEMPLATES),
            'template' : tpl_name,
            'templates' : self._TEMPLATES,
            })


    @property
    def help(self):
        return self.info()


def main(kwargs):
    print(type(kwargs), kwargs)
    egw = EGW(**kwargs)
    print(egw.info)
    egw.run()

if __name__ == '__main__':
    egw = EGW()
    print(egw.info)
