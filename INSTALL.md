Installation
------------

```
# -- fetch latest source 

$ git clone --recurse-submodules -j8 https://github.com/s3h10r/einguteswerkzeug.git
$ cd einguteswerkzeug

# -- install & build into a dedicated virtualenv 
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ ./build.sh 
(venv) $ pip install ./dist/einguteswerkzeug-0.4.0.tar.gz

# -- ready! (:

(venv) $ egw
Usage:
egw <source-image> --output=<filename>
egw (<source-image> | --generator=<str>) [--output=<filename>]
egw (<source-image> | --generator=<str>) [--config=<fqfn>] [--template=<str>] [--noframe]
    [--filter <name>] [--params-filter <fparams>] [--params-generator <params>]
    [--title=<str>] [--title-meta] [--font=<fqfn>] [--text-color=<rgb>]
    [--alpha-blend=<float>] [--border-size=<int>] [--border-color=<rgb>]
    [--size-inner=<n>] [--max-size=<w>]
    [--crop | --nocrop] [--alignment=<str>] [--clockwise | --anticlock] -o <fout>
    [--seed=<int>]

```

Have fun! (:


cheatsheet
----------

Generate an output by using a generator (here `sprites`):

```
$ egw --generator sprites -o /tmp/out.png --template ./einguteswerkzeug/templates/fzm-Polaroid.Frame-01.jpg --title "einguteswerkzeug $(egw --version)" && feh /tmp/out.png
```

Generate output by using an image:

```
egw Screenshot\ from\ 2020-03-02\ 19-53-55.png -o /tmp/out.png --nocrop --template ./einguteswerkzeug/templates/fzm-Polaroid.Frame-01.jpg --title "einguteswerkzeug $(egw --version)" && feh /tmp/out.png
```


