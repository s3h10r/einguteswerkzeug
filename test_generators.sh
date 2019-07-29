#!/bin/bash -vx
GENS=('mondrian' 'nlines' 'psychedelic' 'squares+circles' 'sprites' 'cowsay')

#FONT=$(realpath ./einguteswerkzeug/fonts/contrast.ttf)
FONT=$(realpath ./einguteswerkzeug/fonts/default.ttf)
CONFIG=$(realpath ./einguteswerkzeug/einguteswerkzeug.conf)
TPL=$(realpath ./einguteswerkzeug/templates/random)
MAX_SIZE=600
FOUT="/tmp/test_generators.png" #jpeg doesn't support 'RGBA'

egw --version

for gen in "${GENS[@]}"
do
  echo "testing generator $gen..."
  egw --generator $gen -o $FOUT --title "--generator=${gen} #einguteswerkzeug" --template $TPL -c $CONFIG -f $FONT -m $MAX_SIZE|| exit 1
  feh $FOUT
  egw --generator $gen -o $FOUT -m $MAX_SIZE --noframe || exit 1
  feh $FOUT
done

for gen in "${GENS[@]}"
do
  echo "testing generator $gen..."
  egw --generator $gen -o $FOUT --title "--generator=${gen}" --template $TPL -c $CONFIG -f $FONT -m $MAX_SIZE|| exit 1
  feh $FOUT
  egw --generator $gen -o $FOUT --title "--generator=${gen} + --filter=pixelsort,oil" --filter pixelsort,oil --template $TPL -c $CONFIG -f $FONT -m $MAX_SIZE || exit 1
  feh $FOUT
  egw --generator $gen -o $FOUT --title "--generator=${gen} + --filter=mosaic" --filter mosaic --template $TPL -c $CONFIG -f $FONT -m $MAX_SIZE || exit 1
  feh $FOUT
  egw --generator $gen -o $FOUT --title "--generator=${gen} + --filter=mosaic,oil" --filter mosaic,oil2 --template $TPL -c $CONFIG -f $FONT -m $MAX_SIZE || exit 1
  feh $FOUT
  egw --generator $gen -o $FOUT --title "--generator=${gen} + --filter=mosaic,oil2" --filter mosaic,oil2 --template $TPL -c $CONFIG -f $FONT -m $MAX_SIZE || exit 1
  feh $FOUT
  egw --generator $gen -o $FOUT --title "--generator=${gen} + --filter=pixelsort" --filter pixelsort --template $TPL -c $CONFIG -f $FONT -m $MAX_SIZE || exit 1
  feh $FOUT
  egw --generator $gen -o $FOUT --title "--generator=${gen} + --filter=pixelsort,oil2" --filter pixelsort,oil2 --template $TPL -c $CONFIG -f $FONT -m $MAX_SIZE || exit 1
  feh $FOUT
  egw --generator $gen -o $FOUT --title "--generator=${gen} + --filter=pixelsort,ascii,mosaic" --filter pixelsort,ascii,mosaic --template $TPL -c $CONFIG -f $FONT -m $MAX_SIZE || exit 1
  feh $FOUT
  egw --generator $gen -o $FOUT --title "--generator=${gen} + --filter=ascii" --filter ascii --template $TPL -c $CONFIG -f $FONT -m $MAX_SIZE || exit 1
  feh $FOUT
  egw --generator $gen -o $FOUT --title "--generator=${gen} + --filter=ascii,oil2" --filter ascii,oil2 --template $TPL -c $CONFIG -f $FONT -m $MAX_SIZE || exit 1
  feh $FOUT
done
