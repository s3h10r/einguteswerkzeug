#!/bin/bash -vx
FQFN=$(realpath $0)
MYPATH=$(dirname $FQFN)
PY_LIB_PATH="../venv/lib/python3.7/site-packages"
DIR_TGT="${MYPATH}/src/"

PYMODULES="einguteswerkzeug einguteswerkzeug.core einguteswerkzeug.helpers einguteswerkzeug.helpers.gfx einguteswerkzeug.plugins einguteswerkzeug.plugins.generators einguteswerkzeug.plugins.filters einguteswerkzeug.shell"
cd $PY_LIB_PATH
for module in $PYMODULES; do
  pydoc3 -w $module
done
rm -Rf $DIR_TGT
mkdir -p $DIR_TGT
mv *html $DIR_TGT
