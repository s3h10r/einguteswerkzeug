einguteswerkzeug - a creative tool #inprogress
==============================================

einguteswerkzeug (`egw`) is my latest personal tool for doing minimalistic visual artworks in
printing quality - and learning and mixing fun to use technologies
full-stack around it (raspi, webapis, flutter). :)
einguteswerkzeug startet as a simple Python-script for creating high-resolution contactsheets,
evolved into [something which **creates vintage polaroid style** fairly well](https://github.com/s3h10r/polaroidme)
then and recently i am hacking some **filters and
generative art capabilities** mostly based on wonderfull open-source-projects and
inspiring blog-articles around (see credits) as **plugins** into it.

einguteswerkzeug is far from stable yet and maybe i'll need to rewrite it
from scratch later again - but for now `egw` works just fine for me. :)
So maybe it can be usefull for you too - but don't put any blame on me if it
toasts your hamster or so.

**Contributions are welcome** and they are greatly appreciated!

Please feel free to
send a pull-request and use the [issue tracker](https://github.com/s3h10r/polaroidme/issues).


show don't tell
---------------

Some works i made with `egw` are:

<img src="/examples/awork_small_prettyinpink_vb.jpg" width="48%" title=""></img>
<img src="/examples/test_generator-psychedelic.filter-mosaic,oil2.png" width="48%" title="Psychedelisches Öl2"></img>
<img src="/examples/awork_small_sushiinsuhl_vb.jpg" width="48%" title=""></img>
<img src="/examples/awork_small_tagesbefehl_vb.jpg" width="48%" title=""></img>
<img src="/examples/test_generator-psychedelic.filter-pixelsort,oil.png" width="48%" title="Psychedelisches sortiert"></img>
<img src="examples/spritething-13x13-10-2000.polaroid-01.small.png" width="48%" title="weiste bescheid... ;)"></img>

Credits
=======

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


**Thank you guys!** Live long and prosper!

All the crap and bugs in the code is made by me of course. Please feel free to refacture, fix, tinker, ...

 changelog
 ---------

* please see [CHANGELOG.md](./CHANGELOG.md)

License
-------

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
