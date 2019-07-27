#!/bin/bash -vx
GENS=('psychedelic' 'squares+circles' 'sprites' 'cowsay')

FONT=$(realpath ./einguteswerkzeug/fonts/contrast.ttf)
CONFIG=$(realpath ./einguteswerkzeug/einguteswerkzeug.conf)
TPL=$(realpath ./einguteswerkzeug/templates/random)
MAX_SIZE=600
FOUT="/tmp/test_generators.jpg"

egw --version

egw --generator squares+circles --params-generator='{"shape" : 0}' -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 1, "iterations" : 128}' --config $CONFIG --template $TPL  --max-size 800 || exit 1
feh /tmp/test.jpg
egw --generator squares+circles --params-generator='{"shape" : 0}' -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 2, "iterations" : 128}' --config $CONFIG --template $TPL  --max-size 800 || exit 1
feh /tmp/test.jpg
egw --generator squares+circles --params-generator='{"shape" : 0}' -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 3, "iterations" : 128}' --config $CONFIG --template $TPL  --max-size 800 || exit 1
feh /tmp/test.jpg

egw ./input/DSCF6061.jpg -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 3, "iterations" : 128}' --config $CONFIG --template $TPL --title-meta --max-size 800 || exit 1
feh /tmp/test.jpg
egw ./input/DSCF6061.jpg -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 2, "iterations" : 512}' --config $CONFIG --template $TPL  --title-meta --max-size 800 || exit 1
feh /tmp/test.jpg
egw ./input/DSCF6061.jpg -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 1, "iterations" : 1024}' --config $CONFIG --template $TPL  --title-meta --max-size 800 || exit 1
feh /tmp/test.jpg
