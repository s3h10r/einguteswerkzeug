#!/bin/bash -vx
FOUT="/tmp/eval-rothko.txt"
while :
do

    TITLE=$(egw --generator rothko -o /tmp/out.png --nocrop --template ./einguteswerkzeug/templates/fzm-Polaroid.Frame-02.jpg  --text-color 135,106,235 --alpha-blend 1.0 --filter diffuse,oil2 --title="rothko permutation script, 2020" --params-generator='{"palette":"/home/s3h10r/development/einguteswerkzeug/einguteswerkzeug/plugins/generators/rothko/huge_palette.txt"}' --max-size 600 --params-filter='{"degree":1}{"brush_size" :1, "roughness" : 10}' 2>&1 | grep -i "stitle" | cut -d ":" -f 4)
    feh -Z -F /tmp/out.png
    echo "title: $TITLE"
    read -p "keep this for rendering high-res?[y,n,x] " answer
    case $answer in
        [yY]* ) echo $TITLE >> $FOUT
                echo "Okay, added ${TITLE} to ${FOUT}";;
        [xX]* ) exit;;

        * ) echo "Dude, just enter Y or N or X, please.";;
    esac
done
