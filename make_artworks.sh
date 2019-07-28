#!/bin/bash -vx
# https://anypla.net

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

# --- "complementary message"
# big output (btw. it gets much much bigger but for testing purpose this is good enough)
egw --generator nlines --params-generator='{"seed" : 197919801989002019, "size" : 3200, "nr_lines" : 24, "thickness" : 32, "x_step" : 40, "color" : [0,0,200,255] }' --output $FOUT --title "complementary message, 2019 #einguteswerkzeug" -c $CONFIG --template $TPL2_TRIMMED
feh $FOUT
# small output
egw --generator nlines --params-generator='{"seed" : 197919801989002019, "size" : 800, "nr_lines" : 24, "thickness" : 8, "x_step" : 10, "color" : [0,0,200,255] }' --output $FOUT --title "complementary message, 2019 #einguteswerkzeug" -c $CONFIG --template $TPL2_TRIMMED -m 800
feh $FOUT

# --- "the joy of doing curves poorly" (variant a & b)
egw --generator nlines --params-generator='{"seed" : 4119882467723926860, "size" : 3200, "nr_lines" : 40, "x_step" : 80, "thickness" : 24, "color" : [255,255,255,255], "bg_color" : [0,0,0,255]}' -o $FOUT  --config $CONFIG --template $TPL2  --title "the joy of doing curves poorly, 2019 #einguteswerkzeug" || exit 1
feh $FOUT
egw --generator nlines --params-generator='{"seed" : 4119882467723926861, "nr_lines" : 40, "size" : 3200, "nr_lines" : 40, "x_step" : 80, "thickness" : 24, "color" : [0,0,0,255], "bg_color" : [255,255,255,255]}' -o $FOUT  --config $CONFIG --template $TPL2  --title "parallelism, 2019 #einguteswerkzeug" || exit 1
feh $FOUT
# ---

egw --generator squares+circles --params-generator='{"shape" : 0}' -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 1, "iterations" : 128}' --config $CONFIG --template $TPL  --title "quad-filtered generator s+c (variant a), 2019 #einguteswerkzeug" --max-size 800 || exit 1
feh /tmp/test.jpg
egw --generator squares+circles --params-generator='{"shape" : 0}' -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 2, "iterations" : 128}' --config $CONFIG --template $TPL  --title "quad-filtered generator s+c (variant b), 2019 #einguteswerkzeug" --max-size 800 || exit 1
feh /tmp/test.jpg


egw ./input/DSCF0593.jpg -o /tmp/test.jpg -c ${CONFIG} --template ${TPL}  --title "pretty in pink, 2018" --max-size 800 --nocrop || exit 1
feh /tmp/test.jpg
egw ./input/DSCF0593.jpg -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 2, "iterations" : 1024}' -c ${CONFIG} --template ${TPL}  --title "pretty in pink (variant b), 2019 #einguteswerkzeug" --max-size 800 || exit 1
feh /tmp/test.jpg

egw ./input/IMG_20180901_105615-01.jpg -o /tmp/test.jpg --crop --alignment center -c ${CONFIG} --template ${TPL}  --title "sushi in suhl, 2018" --max-size 800 --nocrop || exit 1
feh /tmp/test.jpg
egw ./input/IMG_20180901_105615-01.jpg -o /tmp/test.jpg --filter invert --crop --alignment center -c ${CONFIG} --template ${TPL}  --title "sushi in suhl (variant b), 2019 #einguteswerkzeug" --max-size 800 --nocrop || exit 1
feh /tmp/test.jpg
egw ./input/IMG_20180901_105615-01.jpg -o /tmp/test.jpg --filter invert,ascii --crop --alignment center -c ${CONFIG} --template ${TPL}  --title "sushi in suhl (variant d), 2019 #einguteswerkzeug" --max-size 800 --nocrop || exit 1
feh /tmp/test.jpg
#egw ./input/IMG_20180901_105615-01.jpg -o /tmp/test.jpg --filter invert,oil2 --params-filter='{}{"brush_size" :8, "roughness" : 200}' --crop --alignment center -c ${CONFIG} --template ${TPL}  --title "sushi in suhl (variant c), 2019" --max-size 800 --nocrop || exit 1
#feh /tmp/test.jpg

egw ./input/DSCF3228.jpg -o /tmp/test.jpg --crop --alignment center -c ${CONFIG} --template ${TPL}  --title "natural recursion, 2018" --max-size 800 --nocrop || exit 1
feh /tmp/test.jpg
egw ./input/DSCF3228.jpg -o /tmp/test.jpg --filter invert --crop --alignment center -c ${CONFIG} --template ${TPL}  --title "natural recursion (variant b), 2019 #einguteswerkzeug" --max-size 800 --nocrop || exit 1
feh /tmp/test.jpg
#egw ./input/DSCF3228.jpg -o /tmp/test.jpg --filter invert,oil2 --params-filter='{}{"brush_size" :4, "roughness" : 20 }' --crop --alignment center -c ${CONFIG} --template ${TPL}  --title "natural recursion (variant b), 2019" --max-size 800 --nocrop || exit 1
#feh /tmp/test.jpg

egw ./input/DSCF9073.jpg -o /tmp/test.jpg --filter invert --crop --alignment center -c ${CONFIG} --template ${TPL}  --title "Tagesbefehl: enjoy the silence (variant b), 2019 #einguteswerkzeug" --max-size 800 --nocrop || exit 1
feh /tmp/test.jpg


exit 0


egw ./input/DSCF0593.jpg -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 1, "iterations" : 64}' -c ${CONFIG} --template ${TPL}  --title "pretty in pink (variant c), 2019 #einguteswerkzeug" --max-size 800 --nocrop || exit 1
feh /tmp/test.jpg

egw ./input/DSCF0593.jpg -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 1, "iterations" : 1024}' -c ${CONFIG} --template ${TPL}  --title "pretty in pink 02B" --title-meta --max-size 800 || exit 1
feh /tmp/test.jpg
egw ./input/DSCF0593.jpg -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 3, "iterations" : 1024}' -c ${CONFIG} --template ${TPL}  --title "pretty in pink 02B" --title-meta --max-size 800 || exit 1
feh /tmp/test.jpg
