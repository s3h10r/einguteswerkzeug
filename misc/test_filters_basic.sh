#!/bin/bash -vx
FILTERS=('puzzle' 'oil2' 'oil' 'mosaic' 'molten' 'invert' 'ice' 'glowing_edge' 'find_edge' 'emboss' 'diffuse' 'ascii' 'quads' 'pixelsort')
CONFIG=$(realpath ./einguteswerkzeug/einguteswerkzeug.conf)
TPL=$(realpath ./einguteswerkzeug/templates/random)
TPL10=$(realpath ./einguteswerkzeug/templates/fzm-Polaroid.Frame-10.jpg)
FONT=$(realpath ./einguteswerkzeug/fonts/default.ttf)
FIN=$(realpath ./input/IMG_20190720_122246.jpg)
FIN2=$(realpath ./examples/smartphone-endofgreenshirt.png)
FIN3=$(realpath ./examples/smartphone-john.png)
FOUT="/tmp/test_filters_basic.png"
FIN_TMP="/tmp/test_filter_tmp.png"

egw --version

for filter in "${FILTERS[@]}"
do
  egw $FIN -o $FOUT --filter $filter --config "$CONF" --template "$TPL10" --size-inner 400 --max-size 800 || exit 1
done

exit 0
