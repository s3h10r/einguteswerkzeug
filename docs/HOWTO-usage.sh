#!/bin/bash -vx
VERSION=$(egw --version | tail -1)
echo "egw $VERSION"
FOUT_PRE="HOWTO_alpha-blend_"
FOUT_POST=".jpg"
TITLE="HOWTO --alpha-blend, 2019 #einguteswerkzeug $VERSION"
SEED=991635567650411077
BORDER_SIZE="0.00"

# --- producing a series to show what effect the change of one param (here --alpha-blend) has
END_LOOP=8
for i in $(seq 1 7 $END_LOOP)
do
  echo $i
  PARAM_ALPHA_BLEND=$i
  BORDER_SIZE="0.10"
  TITLE="alpha-blend $i, 2019 #einguteswerkzeug $VERSION"
  FOUT=${FOUT_PRE}${i}.noframe${FOUT_POST}
  echo "... $FOUT"
  egw --seed $SEED --alpha-blend $PARAM_ALPHA_BLEND --generator psychedelic --filter puzzle --params-filter='{"block_size" : 600}' -o $FOUT  -c ./einguteswerkzeug/egw.conf --template ./einguteswerkzeug/templates/square/roland-deason-S2Zg5RMXl1I-unsplash.jpg -s 200 --noframe --text-color 35,105,225 --title="$TITLE" --border-size $BORDER_SIZE || exit 1
  feh $FOUT
  TITLE="alpha-blend -$i, 2019 #einguteswerkzeug $VERSION"
  FOUT=${FOUT_PRE}-${i}.noframe${FOUT_POST}
  egw --seed $SEED --alpha-blend -${PARAM_ALPHA_BLEND} --generator psychedelic --filter puzzle --params-filter='{"block_size" : 600}' -o $FOUT  -c ./einguteswerkzeug/egw.conf --template ./einguteswerkzeug/templates/square/roland-deason-S2Zg5RMXl1I-unsplash.jpg -s 200 --noframe --text-color 35,105,225 --title="$TITLE" --border-size $BORDER_SIZE || exit 1
  feh $FOUT

  # --- same as above but with complete template
  TITLE="alpha-blend $i, 2019 #einguteswerkzeug $VERSION"
  FOUT=${FOUT_PRE}${i}${FOUT_POST}
  egw --seed $SEED --alpha-blend $PARAM_ALPHA_BLEND --generator psychedelic --filter puzzle --params-filter='{"block_size" : 600}' -o $FOUT  -c ./einguteswerkzeug/egw.conf --template ./einguteswerkzeug/templates/square/roland-deason-S2Zg5RMXl1I-unsplash.jpg -s 200 --text-color 35,105,225 --title="$TITLE" --border-size $BORDER_SIZE || exit 1
  feh $FOUT
  TITLE="alpha-blend -$i, 2019 #einguteswerkzeug $VERSION"
  FOUT=${FOUT_PRE}-${i}${FOUT_POST}
  egw --seed $SEED --alpha-blend -${PARAM_ALPHA_BLEND} --generator psychedelic --filter puzzle --params-filter='{"block_size" : 600}' -o $FOUT  -c ./einguteswerkzeug/egw.conf --template ./einguteswerkzeug/templates/square/roland-deason-S2Zg5RMXl1I-unsplash.jpg -s 200 --text-color 35,105,225 --title="$TITLE" --border-size $BORDER_SIZE || exit 1
  feh $FOUT
  # ---
done
