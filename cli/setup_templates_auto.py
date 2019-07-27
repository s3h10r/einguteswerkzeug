#!/usr/bin/env python3
"""
TODOP3

try to determine the part of the template where the
image should be put in.

!!! THIS DOESNT WORK YET !!! TODOP3
"""
import logging
import statistics
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


if __name__ == '__main__':
    fn = sys.argv[1]
    img = Image.open(fn)
    log.info("source image {} size : {}".format(fn, img.size))
    # turn into numbers
    # log first (0,0,0) and last (0,0,0)
    pixelmap = img.load()
    [xs, ys] = img.size
    colors_rgb = []

    # ---
    img_bw = Image.open(fn).convert('1') #open as black and white version
    pixels_bw = img_bw.load()
    img_bw.save("test_bw.png")

    x_list = []
    y_list = []
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixels_bw[x, y] == 0: # a black pixel
                x_list.append(x)
                y_list.append(y)
    # ---try to identify the continiously black pixels by using basic statistics
    # (mean, standard deviation, median)
    #
    x_mean = statistics.mean(x_list)
    x_median = statistics.median(x_list)
    x_stdev = statistics.stdev(x_list)
    y_mean = statistics.mean(y_list)
    y_median = statistics.median(y_list)
    y_stdev = statistics.stdev(y_list)
    log.debug("x_mean: {} x_xstdev: {} x_median: {}".format(x_mean, x_stdev,x_median))
    log.debug("y_mean: {} y_xstdev: {} y_median: {}".format(y_mean, y_stdev,y_median))

    x_list_plot = [x_mean, x_stdev, x_median]
    y_list_plot = [y_mean, y_stdev, y_median]
    point_sizes = [200,150,100]
    colors = [(255,0,0), (0,255,0), (0,0,255)]
    plt.scatter(x_list_plot,y_list_plot,s = point_sizes, c= colors, alpha=0.5)
    plt.savefig("test.scatterplot-stats.png")

    point_sizes = [1]*len(x_list) # point radius #TODO bigger if nearer to stdev etc.
    plt.scatter(x_list,y_list,s = point_sizes,alpha=0.5)
    #plt.show()
    plt.savefig("test.scatterplot-data.png")
    # ---

    #4 corners of the black square
    xleft = min(x_list)
    xright = max(x_list)
    ytop = min(y_list)
    ybot = max(y_list)
    # ---
    print(xleft,ytop,xright,ybot)

    guess_upper_left = None
    guess_lower_right = None
    for x in range(0, xs):
      for y in range(0, ys):
        [r, g, b] = pixelmap[x, y]
        if [r,g,b] == [0,0,0]:
            if not guess_upper_left:
                guess_upper_left = (x,y)
            else:
                guess_lower_right = (x,y)

    print("guess is: {},{}".format(guess_upper_left, guess_lower_right))
    print("guess is: {},{}".format((xleft,ytop), (xright,ybot)))
    box = (xleft,ytop, xright, ybot)
    # test draw box into center
    #delta = (img.size[1] - img.size[0]) / 2
    #box = (0, delta, img.size[0], img.size[1] - delta)

    draw = ImageDraw.Draw(img)
    draw.rectangle(box, fill="green")
#    draw.rectangle((guess_upper_left, guess_lower_right), fill="green")

#    for x in range(0, xs):
#      for y in range(0, ys):
#          if (x >= guess_upper_left[0]) and (x <= guess_lower_right[0]) and (y >= guess_upper_left[1]) and (y <= guess_lower_right[1]):
#             print("we're inside our guess %i,%i" % (x,y))
#             pixelmap[x, y] = (0,255,0)

    # print process the guess and show for manual check
    #box = (guess_upper_left[0],guess_upper_left[1],guess_lower_right[0],guess_lower_right[1]) # (left, upper, right, lower)
    #img_bbox = img.getbbox()
    #img.crop(box)
    #img_new.show()
    img.save("test.png")
