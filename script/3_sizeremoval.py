import cv2
import numpy as np
from tifffile import imsave, imread
from time import time
from progressbar import update_progress
import argparse

parser=argparse.ArgumentParser(
    description='''Remove too big or too small parcels and shrinking''')
parser.add_argument('-g','--groundtruth', help='Groundtruth image', required=True)
args=parser.parse_args()

# Open the groundtuth image
GRT = imread(args.groundtruth)

# Crop each parcels by 3 pixels
kernel = np.ones((3,3),np.uint8)
GRT = cv2.dilate(GRT,kernel,iterations = 1)

# Id image to identify parcels
im_parcels = (GRT < 255).astype(np.uint8)
N, im_parcels = cv2.connectedComponents(im_parcels)

print('Nb of parcels before removal: %d'%(N))

print('Size removal')
update_progress(0)
# Remove too big or too small parcels
for n in range(1, N + 1):
    t_start = time()
    
    parc_size = np.sum(im_parcels == n)
    if parc_size < 100 or parc_size > 10000:
        GRT[im_parcels == n] = 255

    update_progress((n-1)/(N-0.9), (time()-t_start)*(N-n-1))

# Re-Identified image
im_parcels = (GRT < 255).astype(np.uint8)
N, im_parcels = cv2.connectedComponents(im_parcels)

# Save parcels id image
imsave('/'.join(args.groundtruth.split('/')[:-1]) + '/parcels.tif', im_parcels)

# Save groundtruth image
imsave(args.groundtruth, GRT)


update_progress(1)

print('Nb of parcels after removal: %d'%(N))

print()
