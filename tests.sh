#!/bin/bash

egw --version
egw --help 

#egw --generator mondrian -o /tmp/1.png --params-generator '{"size" : [1024,768]}' --noframe && feh /tmp/1.png
#egw --generator nlines -o /tmp/2.png --filter puzzle -s 800 --noframe && feh /tmp/2.png
egw --generator psychedelic --filter pixelsort,mosaic,oil2 --params-filter '{"algo":10}{"block_size":16}{"brush_size":8, "roughness" : 80}' -o /tmp/egw_tests_3.png -c ./einguteswerkzeug/egw.conf --template ./einguteswerkzeug/templates/square/roland-deason-S2Zg5RMXl1I-unsplash.jpg --border-size 0.10 --text-color 35,105,225 --title="egw selftest $(date +%Y%m%d%H:%M:%S)" --size-inner 600 && feh /tmp/egw_tests_3.png

