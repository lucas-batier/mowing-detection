import cv2
import numpy as np
from tifffile import imsave, imread
from progressbar import update_progress
import argparse

parser=argparse.ArgumentParser(
    description='''Filter on class 0 and formalizing class 1''')
parser.add_argument('-c0','--class0', help='Image of class 0', required=True)
parser.add_argument('-c1','--class1', help='Image of class 1', required=True)
args=parser.parse_args()

update_progress(0)

# No mowing
# Select only meadows 13, grasslands 18 and woody moorlands 19
# Format each not mowed parcels (pixels) to 0 and everywhere else to white 255
GRT0 = imread(args.class0)
GRT0[np.logical_and(GRT0 != 13, GRT0 != 18, GRT0 != 19)] = 255
GRT0[np.logical_or(GRT0 == 13, GRT0 == 18, GRT0 == 19)] = 0

# Save the image class 0
imsave(args.class0, GRT0.astype(np.uint8))

# Mowing
# Format each mowed parcels (pixels) to 1 and everywhere else to white 255
GRT1 = imread(args.class1)
GRT1[GRT1 > 0] = 1
GRT1[GRT1 == 0] = 255

# Save the image class 1
imsave(args.class1, GRT1.astype(np.uint8))

update_progress(1)
