#!/bin/bash -vx
VERSION=$(egw --version | tail -1)
echo "egw $VERSION"
FOUT="HOWTO_--alpha-blend.png"
TITLE="HOWTO --alpha-blend, 2019 #einguteswerkzeug $VERSION"
SEED=991635567650411077
BORDER_SIZE="0.00"
#egw --seed 991635567650411077 --generator psychedelic -o $FOUT --filter puzzle -c ./einguteswerkzeug/egw.conf --template ./einguteswerkzeug/templates/square/roland-deason-S2Zg5RMXl1I-unsplash.jpg -s 200 --nopolaroid --noframe --text-color 35,105,225 --title="$TITLE" --params-filter='{"block_size" : 600}' --alpha-blend 8 --border-size $BORDER_SIZE || exit 1
#feh $FOUT

# --- produces a serie to show what effect the change of one param (here --alpha-blend has)
END_LOOP=8
for i in $(seq 1 7 $END_LOOP)
do
  PARAM_ALPHA_BLEND=$i
  BORDER_SIZE="0.10"
  TITLE="alpha-blend $i, 2019 #einguteswerkzeug $VERSION"
  egw --seed $SEED --alpha-blend $PARAM_ALPHA_BLEND --generator psychedelic --filter puzzle --params-filter='{"block_size" : 600}' -o $FOUT  -c ./einguteswerkzeug/egw.conf --template ./einguteswerkzeug/templates/square/roland-deason-S2Zg5RMXl1I-unsplash.jpg -s 200 --noframe --text-color 35,105,225 --title="$TITLE" --border-size $BORDER_SIZE || exit 1
  feh $FOUT
  TITLE="alpha-blend -$i, 2019 #einguteswerkzeug $VERSION"
  egw --seed $SEED --alpha-blend -${PARAM_ALPHA_BLEND} --generator psychedelic --filter puzzle --params-filter='{"block_size" : 600}' -o $FOUT  -c ./einguteswerkzeug/egw.conf --template ./einguteswerkzeug/templates/square/roland-deason-S2Zg5RMXl1I-unsplash.jpg -s 200 --noframe --text-color 35,105,225 --title="$TITLE" --border-size $BORDER_SIZE || exit 1
  feh $FOUT

  echo $i
done
