#!/bin/bash
pip install -r requirements.txt
rm -Rf ./build/
rm -Rf ./dist/
rm -Rf ./egw.egg-info
rm -Rf __pycache__
./docs/build.sh
#python3 setup.py sdist --formats=gztar,bztar,zip
python3 setup.py sdist --formats=gztar
pip uninstall einguteswerkzeug 
pip install ./dist/einguteswerkzeug-*.tar.gz
