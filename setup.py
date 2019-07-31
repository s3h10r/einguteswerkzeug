import setuptools

from setuptools.command.install import install

# https://blog.niteo.co/setuptools-run-custom-code-in-setup-py/
class CustomInstallCommand(install):
    def run(self):
        print("Hello, how are you? :)")
        install.run(self)

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

long_description_md = """
einguteswerkzeug - a creative tool for generative artworks
==========================================================

einguteswerkzeug (`egw`) is a **cli-tool for creating minimalistic visual artworks** in
printing quality. it can also simply be used only for **giving your photos a fairly
well & individual vintage polaroid style** by placing an image
into a Polaroid-like frame and optionally put a title / description or meta infos
out of EXIF-data on the bottom. The default font mimics scribbled handwriting
but any (ttf-)font which suits your taste is supported. The tool offers basic
features like auto-scaling up-/downwards and/or cropping, using any (ttf-)font,
supports high-res output and gets it's job done well.

einguteswerkzeug provides some phonky **filters and generative art capabilities**
mostly based on wonderfull open-source-projects and inspiring blog-articles
around (see credits & thanks). in short the software provides:

* generative-art-"generators" which are fun to play with
* chainable filters (`--filter f1,f2,...,fN`)
* reading & processing EXIF-data
* lightweight plugin-framework - makes it simple to use (and write) additional filters & generators
* vintage polaroid style supporting (high-res) templates
* supports your favorite (truetype-)font
* `--help`-option :) + usage-examples as shellscripts

The author's main usecase for einguteswerkzeug is doing minimalistic artworks in
printing quality with it.

To see if it could be usefull for your needs take a look at the project's
github-repo and check out the `examples`_

einguteswerkzeug is actively maintained & developed (2019).

Contributions are welcome, and they are greatly appreciated!

Please feel free to send a pull-request and use the `issue tracker <https://github.com/s3h10r/einguteswerkzeug/issues>`_.

Have fun!

_`examples`: https://github.com/s3h10r/einguteswerkzeug/blob/master/README.md
"""

setuptools.setup(
     name='einguteswerkzeug',
     version='0.3.28',
     scripts=['cli/einguteswerkzeug', 'cli/egw'] ,
     author="Sven Hessenmüller",
     author_email="sven.hessenmueller@gmail.com",
     description="converts an image into vintage polaroid style - and can do some phonky stuff. :D",
     include_package_data=True,
     long_description=long_description_md,
     url="https://github.com/s3h10r/einguteswerkzeug",
     packages=setuptools.find_packages(),
     install_requires=requirements,
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
         "Development Status :: 4 - Beta",
         "Environment :: Console",
         "Topic :: Multimedia :: Graphics",
         "Topic :: Utilities",
     ],
     cmdclass={
        'install': CustomInstallCommand,
     },
)
