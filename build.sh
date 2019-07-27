#!/bin/bash
rm -Rf ./build/
rm -Rf ./dist/
rm -Rf ./egw.egg-info
rm -Rf __pycache__

# apt-get install python3-setuptools
#python3 setup.py bdist_wheel
#python3 setup.py sdist --formats=gztar,bztar,zip
python3 setup.py sdist --formats=gztar
