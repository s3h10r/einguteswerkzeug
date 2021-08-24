#!/bin/bash
# btw. 'set nowrap' in vi is your friend
# OR an 'egw-shell' #TODO

# recreating a work of 2020
egw --generator rothko -o /tmp/out.png --nocrop --template ./einguteswerkzeug/templates/fzm-Polaroid.Frame-02.jpg  --text-color 135,106,235 --alpha-blend 1.0 --filter diffuse,oil2 --title="Free Orange, Hazel, and Deep Sea Blue on Dark Blue Grey, 2020" --params-generator='{"seed": 1372403442}' --max-size 400 --params-filter='{"degree":6}{"brush_size" :1, "roughness" : 250}' && feh /tmp/out.png
#egw --generator rothko -o /tmp/out.png --nocrop --template ./einguteswerkzeug/templates/fzm-Polaroid.Frame-02.jpg  --text-color 135,106,235 --alpha-blend 1.0 --filter diffuse,oil2 --title="Free Orange, Hazel, and Deep Sea Blue on Dark Blue Grey, 2020" --params-generator='{"seed": 1372403442}' --max-size 1600 --params-filter='{"degree":6}{"brush_size" :1, "roughness" : 250}' && feh /tmp/out.png


