**0.4.1**
- fixes: --params-generator 

**0.4.0** 
- refactoring: transition to class-based plugins #13
- refactoring: transition to class-based core #13
- unclutters docopts
- fixes #14 : cli-opt --config doesn't work with relative paths
- adds --seed option for reproducing pseudo-randomness
- supports either template-usage or --noframe. kicks out legacy add_frame-feature,
- fixes filter-plugin 'puzzle'
- adds support for greyscale templates
- downsizes template according to --max-size before image processing (closes #11)
- bugfixes

**0.3.2**
- introduces generators (`--generator` option) as an alternative to source-image
  (psychedelic, squares+circles, sprites, cowsay, nlines, mondrian)
- implements a simple to use plugin-mechanism for custom filters & generators.
  => makes it a no-brainer to write a custom plugin (`see plugins/examples/examples.py`).
- adds minimalistic + fun filter-funcs (asciiart, pixelsorting, quads, heehee)
- includes "serious filters" from https://github.com/Tinker-S/SomeImageFilterWithPython
- enables filter-chaining support
- seperates [plugin repository](https://github.com/s3h10r/egw-plugins) from the core-script
- supports random-template choice (`--template <fqdir>/random`, `--template <fqdir>/rand`)
- restructures all the messy parts at least a bit ([packages](https://docs.python.org/3.6/tutorial/modules.html#packages))
- adds `--noframe` option (== do just the plain image processing without pasting it into a template)
- renames the project & migrates latest codebase
- bugfixes & new bugs

**pom-0.9.32**
- option to use high-res scanned blank Polaroid frames as template
  (NEW args `--template` & `--config`). visual output quality
  gains expression by this. :)
- inits tools for template-preparation (trim_, setup_)
- option to use EXIF-data (DateTimeOriginal) as title or append it to the title
  (NEW arg `--title-meta`).
- new args `--size-inner` & `--max-size``
- several minor bugfixes
- contactsheet: sorting options based on EXIF-data

**pom-0.9.2**
- converts into a "real" python-module which exports its core-functionality (`make_polaroid()`-function)
- adds contactsheet-script (thumbnails can be polaroids with filename as caption)
- convinient argparsing (via docopt)
- testbuild-script
- updates docs

**pom-0.9.1**
- argument alignment omitted if `--nocrop option` is set
- updates packaging meta-data & docs
- adds more free fonts. changes default font to [Jakes Handwriting](https://www.dafont.com/jakeshandwriting.font)

**pom-0.9.0**
- packaging (pypi)

**pom-0.8.4**
- updates usage-string
- adds correct file encoding (`pydoc3 ./polaroidme`)

**pom-0.8.2**
- adds free example fonts (source: https://www.dafont.com/ttf.d592)
- support for different fonts via argument

**pom-0.8.0**
- supports for high-res output (argument size, default=800)
- adds `--nocrop` option
- refactoring
