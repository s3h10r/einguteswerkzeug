#!/usr/bin/env python3
"""
create a einguteswerkzeug.conf output for user-defined --template

1. shows template to the user
2. user has to define the box/rectangle where the image should be pasted into by click
3. config for given points is printed to stdout

example:

./setup_templates_manually.py ../einguteswerkzeug/templates/fzm-Polaroid.Frame-04.jpg | tee /tmp/einguteswerkzeug.conf
2019-07-18 17:22:19,953 - __main__ - INFO - source image ../einguteswerkzeug/templates/fzm-Polaroid.Frame-04.jpg size : 26568900
Please click 2 Points to define the area to fill the image into
okidoki, you clicked: [(576.0584415584408, 532.9902597402597), (4208.011904761905, 4240.295454545455)]
TEMPLATE_BOXES = {"fzm-Polaroid.Frame-04.jpg": [576.0584415584408, 532.9902597402597, 4208.011904761905, 4240.295454545455]}
"""
import json
import logging
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

__version__ = (0,1,0)

if __name__ == '__main__':
    fn = sys.argv[1]
    img = np.array(Image.open(fn).convert('L'))
    log.info("source image {} size : {}".format(fn, img.size))
    # show histogram
#    plt.figure()
#    plt.hist(img.flatten(),128)
#    plt.show()
    # ---

    # --- interactive annotation to identify the box for the picture
    plt.imshow(img)
    print('Please click 2 Points to define the area to fill the image into', file=sys.stderr)
    x = plt.ginput(2)
    print("okidoki, you clicked: {}".format(x), file = sys.stderr)
    #plt.show()
    # ---

    TEMPLATE_BOXES = {
        # box = left, upper, right, lower
        os.path.basename(fn) : [x[0][0],x[0][1],x[1][0],x[1][1]]
    }
    #print('TEMPLATE_BOXES = ' + json.dumps(TEMPLATE_BOXES,indent=4,sort_keys=True))
    print('TEMPLATE_BOXES = ' + json.dumps(TEMPLATE_BOXES))
