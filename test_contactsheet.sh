#!/bin/bash

contactsheet ./input/ --output out.png  --size-thumb 600 --ratio free --polaroid --sort-by time && feh out.png
contactsheet ./input/ out.png --polaroid --sort-by exif_time && feh out.png
contactsheet ./examples/ out.png && feh out.png
contactsheet ./examples/ out.png --ratio free --polaroid --font=/home/s3h10r/development/egw/egw/fonts/contrast.ttf && feh out.png.contactsheet ./examples/ out.png --ratio square --polaroid --size=400 && feh out.png
