#! /usr/bin/env python3

# Author: Hunter Damron
# Purpose: takes a sequence of images and a pixel location of the robot then merges into one image

from sys import argv
import os, os.path
import numpy as np
import cv2

def main():
    if len(argv) != 6:
        print("Usage: framemerge.py <dir> <first> <x> <y> <output>")
        return
    dir, first, startx, starty, output = argv[1:]
    startcenter = (int(startx), int(starty))
    opening_size = 7  # You may have to play with this to get proper division
    if not os.path.isdir(dir):
        print("Invalid dir '%s'" % dir)
    if not os.path.isfile(first):
        print("Invalid file '%s'" % first)
    files = (f for f in map(lambda f: os.path.join(dir, f), os.listdir(dir)) if not os.path.samefile(first, f))
    base_img = cv2.imread(first)
    base_gray = cv2.cvtColor(base_img, cv2.COLOR_BGR2GRAY)
    composite_img = base_img.copy()
    h, w = base_img.shape[:2]
    for f in files:
        above_img = cv2.imread(f)
        above_gray = cv2.cvtColor(above_img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(np.abs(above_gray - base_gray),20,255,cv2.THRESH_BINARY)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((opening_size,opening_size),np.uint8))
        cv2.floodFill(thresh, np.zeros((h + 2, w + 2), np.uint8), startcenter, 0)
        composite_img = cv2.bitwise_and(composite_img, composite_img, mask=cv2.bitwise_not(thresh))
        composite_img += cv2.bitwise_or(above_img, above_img, mask=thresh)

    cv2.imwrite(output, composite_img)

if __name__ == "__main__":
    main()
