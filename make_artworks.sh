#!/bin/bash -vx
# searching a new name for the project because it turns out to go into
# another direction than "just doing polaroids"... so what about
# "a good digital (expressive) tool" => #agodiet #agodit
# einguteswerkzeug
# https://anypla.net/einguteswerkzeug

GENS=('psychedelic' 'squares+circles' 'sprites' 'cowsay')
FONT=$(realpath ./einguteswerkzeug/fonts/contrast.ttf)
CONFIG=$(realpath ./einguteswerkzeug/einguteswerkzeug.conf)
TPL=$(realpath ./einguteswerkzeug/templates/random)
MAX_SIZE=600
FOUT="/tmp/test_generators.jpg"

egw --version

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
