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
TPL_REPO_00=$(realpath ./einguteswerkzeug/templates/square/egw-template_julian-hochgesang-BKACkJLu5Hc-unsplash.jpg)
TPL_REPO_01=$(realpath ./einguteswerkzeug/templates/square/egw-template_david-van-dijk-3LTht2nxd34-unsplash.jpg)
TPL_REPO_02=$(realpath ./einguteswerkzeug/templates/square/egw-template_sarah-dorweiler-7tFlUFGa7Dk-unsplash.jpg)
TPLS=($TPL_REPO_00 $TPL2)
FOUT="/tmp/test_generators.png"
FOUT1="/tmp/test_generators_r1.png"
FOUT2="/tmp/test_generators_r2.png"
FOUT3="/tmp/test_generators_r3.png"

MAX_SIZE=600

VERSION=$(egw --version | tail -1)
echo $VERSION

# --- "view (unfinished)"
TITLE="Plato's Cave (unfinished), 2019 #einguteswerkzeug ${VERSION}"
egw --generator nlines --nopolaroid  --size-inner 8000 --border-size 0.3 --border-color 238,238,238 --params-generator='{"seed" : 197919801989002019, "size" : 8000, "nr_lines" : 24, "thickness" : 80, "x_step" : 100, "color" : [0,0,200,255] }' -o $FOUT  --config $CONFIG --template $TPL_REPO_02 --title "" --max-size 12000 || exit 1
#feh $FOUT
egw $FOUT --nopolaroid  --nocrop --border-size 0.1 --border-color 238,238,238 -o $FOUT1  --config $CONFIG --template $TPL_REPO_02 --title "" --max-size 12000 || exit 1
egw $FOUT1 --nopolaroid  --nocrop --border-size 0.1 --border-color 255,255,255 -o $FOUT2  --config $CONFIG --template $TPL_REPO_01 --title "" --max-size 12000 || exit 1
#feh $FOUT2
egw $FOUT2 --nopolaroid  --nocrop --border-size 0.2 --border-color 238,238,238 -o $FOUT3  --config $CONFIG --template $TPL_REPO_02 --title "" --max-size 12000 || exit 1
#feh $FOUT3
egw $FOUT3 --nopolaroid  --nocrop --border-size 0.1 --border-color 200,200,200 -o $FOUT  --config $CONFIG --template $TPL_REPO_00 --title "" --max-size 12000 || exit 1
feh $FOUT
egw $FOUT --crop --alignment left -o $FOUT1  --config $CONFIG --template $TPL2 --title "$TITLE" || exit 1
feh $FOUT1
# ---

# --- "the joy of doing curves poorly" (variant a & b)
for tpl in "${TPLS[@]}"
do
  TITLE="the joy of doing curves poorly, 2019 #einguteswerkzeug"
  egw --generator nlines --params-generator='{"seed" : 4119882467723926860, "size" : 3200, "nr_lines" : 40, "x_step" : 80, "thickness" : 24, "color" : [255,255,255,255], "bg_color" : [0,0,0,255]}' -o $FOUT  --config $CONFIG --template $tpl  --title "$TITLE" || exit 1
  feh $FOUT
  TITLE="parallelism, 2019 #einguteswerkzeug"
  egw --generator nlines --params-generator='{"seed" : 4119882467723926861, "nr_lines" : 40, "size" : 3200, "nr_lines" : 40, "x_step" : 80, "thickness" : 24, "color" : [0,0,0,255], "bg_color" : [255,255,255,255]}' -o $FOUT  --config $CONFIG --template $tpl  --title "$TITLE" || exit 1
  feh $FOUT
done
# recursive 2
for tpl in "${TPLS[@]}"
do
  TITLE="the joy of doing curves poorly, 2019 #einguteswerkzeug ${VERSION}"
  egw -o $FOUT --generator nlines --params-generator='{"seed" : 4119882467723926860, "size" : 3200, "nr_lines" : 40, "x_step" : 80, "thickness" : 24, "color" : [255,255,255,255], "bg_color" : [0,0,0,255]}' --config $CONFIG --template $tpl  --title "$TITLE" || exit 1
  TITLE="" # recursion 1
  egw $FOUT -o $FOUT1  --config $CONFIG --template $tpl  --title "$TITLE" || exit 1
  feh $FOUT1
  TITLE="" # recursion 2
  egw $FOUT1 -o $FOUT2  --config $CONFIG --template $tpl  --title "$TITLE" || exit 1
  feh $FOUT2
done
for tpl in "${TPLS[@]}"
do
  TITLE="parallelism, 2019 #einguteswerkzeug ${VERSION}"
  egw -o $FOUT --generator nlines --params-generator='{"seed" : 4119882467723926861, "nr_lines" : 40, "size" : 3200, "nr_lines" : 40, "x_step" : 80, "thickness" : 24, "color" : [0,0,0,255], "bg_color" : [255,255,255,255]}' --config $CONFIG --template $tpl  --title "$TITLE" || exit 1
  TITLE="" # recursion 1
  egw $FOUT -o $FOUT1  --config $CONFIG --template $tpl  --title "$TITLE" || exit 1
  feh $FOUT1
  TITLE="" # recursion 2
  egw $FOUT1 -o $FOUT2  --config $CONFIG --template $tpl  --title "$TITLE" || exit 1
  feh $FOUT2
done



# TODO recursive mixof both variants ("knot in the head ;)")! see #9 "support multi-paste-area templates"
# (and btw. fixing the damned manual n-loops to something a computer is made for ;)

# ---


# --- "complementary message"
TITLE="complementary message, 2019 #einguteswerkzeug"
# big output (btw. it gets much much bigger but for testing purpose this is good enough)
egw --generator nlines --params-generator='{"seed" : 197919801989002019, "size" : 3200, "nr_lines" : 24, "thickness" : 32, "x_step" : 40, "color" : [0,0,200,255] }' --output $FOUT --title $TITLE -c $CONFIG --template $TPL2_TRIMMED
feh $FOUT
# small output
egw --generator nlines --params-generator='{"seed" : 197919801989002019, "size" : 800, "nr_lines" : 24, "thickness" : 8, "x_step" : 10, "color" : [0,0,200,255] }' --output $FOUT --title $TITLE -c $CONFIG --template $TPL2_TRIMMED -m 800
feh $FOUT



for tpl in "${TPLS[@]}"
do
  egw --generator squares+circles --params-generator='{"shape" : 0}' -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 1, "iterations" : 128}' --config $CONFIG --template $tpl  --title "quad-filtered generator s+c (variant a), 2019 #einguteswerkzeug" --max-size 800 || exit 1
  feh /tmp/test.jpg
  egw --generator squares+circles --params-generator='{"shape" : 0}' -o /tmp/test.jpg --filter quads --params-filter='{"mode" : 2, "iterations" : 128}' --config $CONFIG --template $tpl  --title "quad-filtered generator s+c (variant b), 2019 #einguteswerkzeug" --max-size 800 || exit 1
  feh /tmp/test.jpg
done

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
