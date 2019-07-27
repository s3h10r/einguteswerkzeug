#!/bin/bash
rm ./input/DSCF2330.polaroid.png
rm ./input/DSCF2313.polaroid.png
rm ./input/DSCF4700.polaroid.png

# the output of the following should be exactly the same (because we feed a perfect sqare in)
./egw --crop ./input/DSCF4700.jpg 800 --alignment center --title "--crop option (square in)" -o ./input/DSCF4700.polaroid.jpg
./egw --nocrop ./input/DSCF4700.jpg 800 --alignment center --title "--nocrop option (square in)" -o ./input/DSCF4700.polaroid.nocrop.jpg
feh ./input/DSCF4700.polaroid.png
feh ./input/DSCF4700.polaroid.nocrop.png

# --#

#./egw --crop ./input/DSCF2330.jpg 800 center "--crop option center (landscape)"
#./egw --crop ./input/DSCF2313.jpg 800 center "--crop option center (portrait)"
#./egw --nocrop ./input/DSCF2330.jpg 800 center "--nocrop option (landscape in)"
#./egw --nocrop ./input/DSCF2313.jpg 800 center "--nocrop option (portrait in)"

#feh ./input/DSCF2330.polaroid.png
#feh ./input/DSCF2313.polaroid.png

#mv ./input/DSCF2330.polaroid.png ./examples/DSCF2330.polaroid.nocrop.png
#mv ./input/DSCF2313.polaroid.png ./examples/DSCF2313.polaroid.nocrop.png
#mv ./input/DSCF4700.polaroid.png ./examples/DSCF4700.polaroid.png
#mv ./input/DSCF2330.polaroid.png ./examples/
#mv ./input/DSCF2313.polaroid.png ./examples/

#feh ./input/DSCF2330.polaroid.png
#feh ./input/DSCF2313.polaroid.png
