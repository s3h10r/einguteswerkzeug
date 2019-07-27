**0.9.38** (work in progress)

- introduces generators (`--generator` option) as an alternative to source-image
  (psychedelic, squares+circles, sprites, cowsay)
- implements a simple to use plugin-mechanism for custom filters & generators.
  => makes it a no-brainer to write a custom plugin (`see plugins/examples/examples.py`).
- adds minimalistic + fun filter-funcs (asciiart, pixelsorting, quads, heehee)
- includes "serious filters" from https://github.com/Tinker-S/SomeImageFilterWithPython
- enables filter-chaining support
- seperates polaroidme-plugin repository from the core-script
- supports random-template choice (`--template <fqdir>/random`, `--template <fqdir>/rand`)
- restructures all the messy parts at least a bit ([packages](https://docs.python.org/3.6/tutorial/modules.html#packages)
- TODO: contactsheet supports filtering by time-window
- TODO: improved template support
- bugfixes & new bugs

**0.9.32**
- option to use high-res scanned blank Polaroid frames as template
  (NEW args `--template` & `--config`). visual output quality
  gains expression by this. :)
- inits tools for template-preparation (trim_, setup_)
- option to use EXIF-data (DateTimeOriginal) as title or append it to the title
  (NEW arg `--title-meta`).
- new args `--size-inner` & `--max-size``
- several minor bugfixes
- contactsheet: sorting options based on EXIF-data

**0.9.2**
- converts into a "real" python-module which exports its core-functionality (`make_polaroid()`-function)
- adds contactsheet-script (thumbnails can be polaroids with filename as caption)
- convinient argparsing (via docopt)
- testbuild-script
- updates docs

**0.9.1**
- argument alignment omitted if `--nocrop option` is set
- updates packaging meta-data & docs
- adds more free fonts. changes default font to [Jakes Handwriting](https://www.dafont.com/jakeshandwriting.font)

**0.9.0**
- packaging (pypi)

**0.8.4**
- updates usage-string
- adds correct file encoding (`pydoc3 ./polaroidme`)

**0.8.2**
- adds free example fonts (source: https://www.dafont.com/ttf.d592)
- support for different fonts via argument

**0.8.0**
- supports for high-res output (argument size, default=800)
- adds `--nocrop` option
- refactoring

**0.1.0**

- initial commit based on https://github.com/thegaragelab/pythonutils/tree/master/polaroid
- converts to python3
