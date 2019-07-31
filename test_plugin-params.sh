#!/bin/bash -vx
GENS=('psychedelic' 'squares+circles' 'sprites' 'cowsay')

#FONT=$(realpath ./einguteswerkzeug/fonts/contrast.ttf)
FONT=$(realpath ./einguteswerkzeug/fonts/default.ttf)
CONFIG=$(realpath ./einguteswerkzeug/einguteswerkzeug.conf)
GENS=('mondrian' 'nlines' 'psychedelic' 'squares+circles' 'sprites' 'cowsay')
TPL=$(realpath ./einguteswerkzeug/templates/random)
TPL1=$(realpath ./einguteswerkzeug/templates/fzm-Polaroid.Frame-01.jpg)
TPL2=$(realpath ./einguteswerkzeug/templates/fzm-Polaroid.Frame-02.jpg)
TPL4=$(realpath ./einguteswerkzeug/templates/fzm-Polaroid.Frame-04.jpg)
TPL10=$(realpath ./einguteswerkzeug/templates/fzm-Polaroid.Frame-10.jpg)
TPL2_TRIMMED=$(realpath ./einguteswerkzeug/templates/trimmed-fzm-Polaroid.Frame-02.jpg)
TPL_REPO_00=$(realpath ./einguteswerkzeug/templates/square/egw-template_julian-hochgesang-BKACkJLu5Hc-unsplash.jpg)
TPL_REPO_01=$(realpath ./einguteswerkzeug/templates/square/egw-template_david-van-dijk-3LTht2nxd34-unsplash.jpg)
TPL_REPO_02=$(realpath ./einguteswerkzeug/templates/square/egw-template_sarah-dorweiler-7tFlUFGa7Dk-unsplash.jpg)
TPL_REPO_03=$(realpath ./einguteswerkzeug/templates/square/egw-template_rodion-kutsaev-IJ25m7fXqtk-unsplash.jpg)

MAX_SIZE=600
FOUT="/tmp/test_generators.png"
FOUT1="/tmp/test_generators_r1.png"
FOUT2="/tmp/test_generators_r2.png"
FOUT3="/tmp/test_generators_r3.png"

VERSION=$(egw --version | tail -1) || exit 1
echo $VERSION

egw --generator mondrian --nopolaroid  --alpha-blend 0.4 --border-size 0.05 --border-color 238,238,238 -o $FOUT  --config $CONFIG --template $TPL_REPO_03 --title "" --max-size 800 || exit 1
feh $FOUT

egw --generator nlines --nopolaroid  --border-size 0.3 --border-color 238,238,238 --params-generator='{"seed" : 197919801989002019, "size" : 800, "nr_lines" : 24, "thickness" : 8, "x_step" : 10, "color" : [0,0,200,255] }' -o $FOUT  --config $CONFIG --template $TPL_REPO_02 --title "" --max-size 800 || exit 1
feh $FOUT

egw $FOUT --nopolaroid  --nocrop --border-size 0.1 --border-color 238,238,238 -o $FOUT1  --config $CONFIG --template $TPL_REPO_02 --title "" --max-size 800 || exit 1
egw $FOUT1 --nopolaroid  --nocrop --border-size 0.1 --border-color 255,255,255 -o $FOUT2  --config $CONFIG --template $TPL_REPO_01 --title "" --max-size 800 || exit 1
egw $FOUT2 --nopolaroid  --nocrop --border-size 0.1 --border-color 238,238,238 -o $FOUT3  --config $CONFIG --template $TPL_REPO_02 --title "" --max-size 800 || exit 1
feh $FOUT3

egw --generator mondrian --nopolaroid --border-size 0.2 --params-generator='{"seed" : 341053573249448960, "width" :800, "height" : 800 }' -o $FOUT  --config $CONFIG --template $TPL_REPO_01 --title "generator mondrian, 2019 #einguteswerkzeug" --max-size 800 || exit 1
feh $FOUT
egw --generator mondrian --nopolaroid --params-generator='{"seed" : 341053573249448960, "width" :800, "height" : 800 }' -o $FOUT  --config $CONFIG --template $TPL_REPO_00 --title "generator mondrian, 2019 #einguteswerkzeug" --max-size 800 || exit 1
feh $FOUT

egw --generator nlines --nopolaroid  -o $FOUT  --config $CONFIG --template $TPL_REPO_00 --title "generator nlines, 2019 #einguteswerkzeug" --max-size 800 || exit 1
feh $FOUT

egw --generator nlines --noframe --params-generator='{"seed" : 197919801989002019, "size" : 400, "nr_lines" : 24, "thickness" : 8, "x_step" : 10, "color" : [0,0,200,255] }' -o $FOUT  --config $CONFIG --template $TPL_REPO_00 --title "complementary message, 2019 #einguteswerkzeug" --max-size 800 || exit 1
feh $FOUT

TITLE="complementary message, 2019 #einguteswerkzeug ${VERSION}"
egw --generator nlines --nopolaroid --params-generator='{"seed" : 197919801989002019, "size" : 800, "nr_lines" : 24, "thickness" : 8, "x_step" : 10, "color" : [0,0,200,255] }' -o $FOUT  --config $CONFIG --template $TPL_REPO_00 --title "${TITLE}" --max-size 800 || exit 1
feh $FOUT

egw --generator mondrian --params-generator='{"seed" : 341053573249448960, "width" :1200, "height" : 1200 }' -o $FOUT  --filter oil2 --config $CONFIG --template $TPL_REPO_00 --title "generator mondrian, 2019 #einguteswerkzeug" --max-size 800 || exit 1
feh $FOUT

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
