einguteswerkzeug - a creative tool
==================================

einguteswerkzeug (`egw`) is a **tool for creating minimalistic visual artworks** in
printing quality - and learning and mixing fun to use technologies
full-stack around it (raspi, webapis, flutter). :)

<img src="examples/spritething-13x13-10-2000.polaroid-01.small.png" width="90%" title="weiste bescheid... ;)"></img>

The main purpose of the cli-version is to produce high-quality, hand-signed & limited (generative)
art prints. But `egw` can also just be used for giving your photos [a fairly well & individual **vintage polaroid style**](README.md). einguteswerkzeug provides some phonky **filters and generative art capabilities** mostly based on wonderfull open-source-projects and inspiring blog-articles
around (see credits & thanks). in short the software provides:

* generative-art-"generators" which are fun to play with
* chainable filters (`--filter f1,f2,...,fN`)
* reading & processing EXIF-data
* lightweight plugin-framework - makes it simple to use (and write) additional filters & generators
* vintage polaroid style supporting (high-res) templates
* `--help`-option :) + usage-examples as shellscripts

This software is in **beta-status** and therefore some interface-things will
change for sure - but for now `egw` already works just fine for me. So maybe it
can be usefull for you too.


turn einguteswerkzeug into deinguteswerkzeug :)
-----------------------------------------------

It's fun to chain some of the provided filters to get good results
but to get most out of `egw` use its lightweight plugin-mechanism to [simply roll your own **plugin(s)**](https://github.com/s3h10r/egw-plugins) in [Python](https://python.org).

**Contributions are welcome** and they are greatly appreciated!

Please feel free to send a pull-request and use the [issue tracker](https://github.com/s3h10r/polaroidme/issues).


TLDR; show don't tell
---------------------

Some examples of works i am doing with `einguteswerkzeug` are:

<img src="/examples/awork_small_prettyinpink_vb.jpg" width="48%" title=""></img>
<img src="/examples/test_generator-psychedelic.filter-mosaic,oil2.png" width="48%" title="Psychedelisches Öl2"></img>
<img src="/examples/awork_small_sushiinsuhl_vb.jpg" width="48%" title=""></img>
<img src="/examples/awork_small_tagesbefehl_vb.jpg" width="48%" title=""></img>
<img src="/examples/test_generator-psychedelic.filter-pixelsort,oil.png" width="48%" title="Psychedelisches sortiert"></img>
<img src="examples/spritething-13x13-10-2000.polaroid-01.small.png" width="48%" title="weiste bescheid... ;)"></img>

you want to help?
=================

we need free high-res templates
-------------------------------

To get an appealing rugged analogue style you can also make "huge" prints of [use high-resolution scans of polaroid Frames - the ones i use at the moment can be downloaded here for free](http://www.fuzzimo.com/free-hi-res-blank-polaroid-frames/).

Sadly i don't know a source of CreativeCommons (or alike) licensed scans in that
high quality and i don't own a good scanner - if you would like to help:
adding some high-res scans in the FLOSS tradition - means for "free as in freedom, not as in beer" - would be wonderfull! (:


donate
------

You do like einguteswerkzeug and want to support its development but you don't
have the time? Please **consider a small [donation](https://paypal.me/s3h10r)** - every
cent helps me to pay the bills & to continue building awesome software for
creative people.

Thank you very much!


Credits & Thanks
================

filters
-------
The ASCII-art filter relies on codesnippets from the following Open Source projects:

 - [asciify](https://github.com/RameshAditya/asciify)
 - [ImageToAscii](https://github.com/cleardusk/ImageToAscii/blob/master/img_to_ascii.py)
   Copyright (c) 2018 Jianzhu Guo, MIT License

Most filters are adopted from:
     [https://github.com/Tinker-S/SomeImageFilterWithPython](https://github.com/Tinker-S/SomeImageFilterWithPython)

- The quads-filter is a quickndirty py3-port of the wonderfull code by [Michael Fogleman][https://github.com/fogleman/Quads]

generators
----------

The generator 'sprites' is made with [code by Eric Davidson](https://medium.freecodecamp.org/how-to-create-generative-art-in-less-than-100-lines-of-code-d37f379859f).

The generator 'psychedelic' is the wonderfull code of ["Random (Psychedelic) Art, and a Pinch of Python" by Jeremy Kun](http://jeremykun.com/2012/01/01/random-psychedelic-art/).

The generator 'squares+circles' is heavily [inspired by Kevin Howbrook's Squares](https://medium.com/@kevinhowbrook/learning-python-and-being-creative-making-art-with-code-da02880e3738)

**Thank you guys! Live long and prosper!**

All the crap and bugs in the code while quickly porting some old stuff to Py3
is made by me of course. Please feel free to refacture, fix, tinker, ...

changelog
=========

* please see [CHANGELOG.md](./CHANGELOG.md)

License
=======

einguteswerkzeug is made with <3, actively maintained & developed by Sven Hessenmüller.

MIT License

Copyright (c) 2019 Sven Hessenmüller <sven.hessenmueller@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
