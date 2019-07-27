#!/bin/bash -vx
GENS=('psychedelic' 'squares+circles' 'sprites' 'cowsay')

FONT=$(realpath ./egw/fonts/contrast.ttf)
CONFIG=$(realpath ./egw/egw.conf)
TPL=$(realpath ./egw/templates/random)
MAX_SIZE=600
FOUT="/tmp/test_generators.jpg"

egw --version

egw --generator squares+circles --params-generator='{"shape" : 0}' -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 1, "iterations" : 128}' --config ./egw/egw.conf --template /home/s3h10r/development/egw/egw/templates/random  --max-size 800 || exit 1
feh /tmp/test.jpg
egw --generator squares+circles --params-generator='{"shape" : 0}' -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 2, "iterations" : 128}' --config ./egw/egw.conf --template /home/s3h10r/development/egw/egw/templates/random  --max-size 800 || exit 1
feh /tmp/test.jpg
egw --generator squares+circles --params-generator='{"shape" : 0}' -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 3, "iterations" : 128}' --config ./egw/egw.conf --template /home/s3h10r/development/egw/egw/templates/random  --max-size 800 || exit 1
feh /tmp/test.jpg

egw ./input/DSCF6061.jpg -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 3, "iterations" : 128}' --config ./egw/egw.conf --template /home/s3h10r/development/egw/egw/templates/random  --title-meta --max-size 800 || exit 1
feh /tmp/test.jpg
egw ./input/DSCF6061.jpg -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 2, "iterations" : 512}' --config ./egw/egw.conf --template /home/s3h10r/development/egw/egw/templates/random  --title-meta --max-size 800 || exit 1
feh /tmp/test.jpg
egw ./input/DSCF6061.jpg -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 1, "iterations" : 1024}' --config ./egw/egw.conf --template /home/s3h10r/development/egw/egw/templates/random  --title-meta --max-size 800 || exit 1
feh /tmp/test.jpg
