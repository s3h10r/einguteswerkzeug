#!/bin/bash -vx
FILTERS=('quads' 'ascii' 'pixelsort' 'diffuse' 'emboss' 'find_edge' 'glowing_edge' 'ice' 'molten' 'mosaic' 'oil' 'oil2')
FILTERS_MULTI_INPUT=('composite')
CONFIG=$(realpath ./einguteswerkzeug/einguteswerkzeug.conf)
TPL=$(realpath ./einguteswerkzeug/templates/random)
#FONT=$(realpath ./einguteswerkzeug/fonts/contrast.ttf)
FONT=$(realpath ./einguteswerkzeug/fonts/default.ttf)
#FIN="./input/octocat.png"
FIN=$(realpath ./input/IMG_20190720_122246.jpg)
FIN2=$(realpath ./examples/smartphone-endofgreenshirt.png)
FIN3=$(realpath ./examples/smartphone-john.png)
FOUT="/tmp/test_filter.png"
FIN_TMP="/tmp/test_filter_tmp.png"

egw --version

for filter in "${FILTERS[@]}"
do
  echo "testing filter $filter..."
egw $FIN -o $FOUT --size-inner 400 --template $TPL --config $CONFIG --crop --alignment center --title "--filter $filter #einguteswerkzeug" --filter $filter --font $FONT -m 600 || exit 1
feh $FOUT
done

for filter in "${FILTERS_MULTI_INPUT[@]}"
do
  echo "testing multi-input-filter $filter..."
	egw ${FIN},${FIN2} -o $FOUT --size-inner 400 --template $TPL --config $CONFIG --crop --alignment center --title "--filter $filter" --filter $filter --font $FONT -m 600 || exit 1
	egw ${FIN},${FIN2},${FIN3} -o $FOUT --size-inner 400 --template /home/s3h10r/development/egw/egw/templates/random --config egw/egw.conf --crop --alignment center --title "--filter $filter" --filter $filter --font $FONT -m 600 || exit 1
	feh $FOUT
	egw ${FIN} -o $FOUT --size-inner 400 --template $TPL --config $CONFIG --crop --alignment center --title "--filter $filter" --filter $filter --font $FONT -m 600 && echo "ERROR: this should fail but succeeded."
	feh $FOUT
done

cp $FOUT $FIN_TMP
egw ${FIN_TMP} -o $FOUT --size-inner 400 --template $TPL --config $CONFIG --crop --alignment center --title "--filter ice,oil" --filter ice,oil --font $FONT -m 600 || exit 1
feh $FOUT
cp $FOUT $FIN_TMP
egw ${FIN_TMP} -o $FOUT --size-inner 400 --template $TPL --config $CONFIG --crop --alignment center --title "--filter oil2" --filter oil2 --font $FONT -m 600 || exit 1
feh $FOUT
