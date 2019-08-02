#!/bin/bash -vx
GENERATORS=('mondrian' 'nlines' 'psychedelic' 'squares+circles' 'sprites' 'cowsay')
CONFIG=$(realpath ./einguteswerkzeug/einguteswerkzeug.conf)
TPL=$(realpath ./einguteswerkzeug/templates/random)
TPL10=$(realpath ./einguteswerkzeug/templates/fzm-Polaroid.Frame-10.jpg)
FONT=$(realpath ./einguteswerkzeug/fonts/default.ttf)
FIN=$(realpath ./input/IMG_20190720_122246.jpg)
FIN2=$(realpath ./examples/smartphone-endofgreenshirt.png)
FIN3=$(realpath ./examples/smartphone-john.png)
FOUT="/tmp/test_generators_basic.png"
FIN_TMP="/tmp/test_filter_tmp.png"

egw --version

for generator in "${GENERATORS[@]}"
do
  egw --generator $generator -o $FOUT --config "$CONF" --template "$TPL10" --size-inner 400 --max-size 800 || exit 1
done

exit 0
