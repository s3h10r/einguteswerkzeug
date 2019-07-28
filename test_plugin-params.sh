#!/bin/bash -vx
GENS=('psychedelic' 'squares+circles' 'sprites' 'cowsay')

#FONT=$(realpath ./einguteswerkzeug/fonts/contrast.ttf)
FONT=$(realpath ./einguteswerkzeug/fonts/default.ttf)
CONFIG=$(realpath ./einguteswerkzeug/einguteswerkzeug.conf)
TPL=$(realpath ./einguteswerkzeug/templates/random)
TPL1=$(realpath ./einguteswerkzeug/templates/fzm-Polaroid.Frame-01.jpg)
TPL2=$(realpath ./einguteswerkzeug/templates/fzm-Polaroid.Frame-02.jpg)
TPL4=$(realpath ./einguteswerkzeug/templates/fzm-Polaroid.Frame-04.jpg)
TPL10=$(realpath ./einguteswerkzeug/templates/fzm-Polaroid.Frame-10.jpg)
TPL2_TRIMMED=$(realpath ./einguteswerkzeug/templates/trimmed-fzm-Polaroid.Frame-02.jpg)

MAX_SIZE=600
FOUT="/tmp/test_generators.jpg"

egw --version

# filtering is fun! (:
egw --generator nlines --anticlock --params-generator='{"seed" : 5269546439996500824, "nr_lines" : 9, "x_step" : 20, "thickness" : 6, "color" : [0,255,0,255], "bg_color" : [0,0,200,255]}' -o $FOUT  --filter quads,invert,oil,find_edge --params-filter='{"mode" : 1, "iterations" : 256}{}{"brush_size" : 2, "roughness" : 50}' --config $CONFIG --template $TPL2  --title "g. nlines with 4 chained filters, 2019 #einguteswerkzeug" --max-size 800 || exit 1
feh $FOUT

# -- reproducing a picture by setting randseet
egw --generator nlines --params-generator='{"seed" : 4119882467723926860, "nr_lines" : 40, "x_step" : 20, "thickness" : 6, "color" : [255,255,255,255], "bg_color" : [0,0,0,255]}' -o $FOUT  --config $CONFIG --template $TPL  --title "generator nlines (variant a), 2019 #einguteswerkzeug" --max-size 800 || exit 1
feh $FOUT
# -- creating a very similar one (mostly identical params, but because we dunnot set seed the shape of line should be differently random
egw --generator nlines --params-generator='{"nr_lines" : 40, "x_step" : 20, "thickness" : 6, "color" : [255,255,255,255], "bg_color" : [0,0,0,255]}' -o $FOUT  --config $CONFIG --template $TPL  --title "generator nlines (variant a), 2019 #einguteswerkzeug" --max-size 800 || exit 1
feh $FOUT


egw --generator squares+circles --params-generator='{"shape" : 0}' -o $FOUT --filter quads --params-filter='{"mode" : 1, "iterations" : 128}' --config $CONFIG --template $TPL  --title "quad-filtered generator s+c (variant a), 2019 #einguteswerkzeug" --max-size 800 || exit 1
feh $FOUT
egw --generator squares+circles --params-generator='{"shape" : 0}' -o $FOUT --filter quads --params-filter='{"mode" : 2, "iterations" : 128}' --config $CONFIG --template $TPL  --title "quad-filtered generator s+c (variant b)i, 2019 #einguteswerkzeug" --max-size 800 || exit 1
feh $FOUT
egw --generator squares+circles --params-generator='{"shape" : 0}' -o $FOUT --filter quads --params-filter='{"mode" : 3, "iterations" : 128}' --config $CONFIG --template $TPL  --title "quad-filtered generator s+c (variant c)i, 2019 #einguteswerkzeug" --max-size 800 || exit 1
feh $FOUT

egw ./input/DSCF6061.jpg -o $FOUT --filter quads --params-filter='{"mode" : 3, "iterations" : 128}' --config $CONFIG --template $TPL --title-meta --max-size 800 || exit 1
feh $FOUT
egw ./input/DSCF6061.jpg -o $FOUT --filter quads --params-filter='{"mode" : 2, "iterations" : 512}' --config $CONFIG --template $TPL  --title-meta --max-size 800 || exit 1
feh $FOUT
egw ./input/DSCF6061.jpg -o $FOUT --filter quads --params-filter='{"mode" : 1, "iterations" : 1024}' --config $CONFIG --template $TPL  --title-meta --max-size 800 || exit 1
feh $FOUT
