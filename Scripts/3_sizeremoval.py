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

print('[Size] Parcels removal')

GRT = imread(args.groundtruth)
GRT0 = np.array(GRT)
GRT0[GRT0 == 1] = 255
im_parcels = (GRT0 < 255).astype(np.uint8)
N0, im_parcels0 = cv2.connectedComponents(im_parcels)

GRT1 = np.array(GRT)
GRT1[GRT1 == 0] = 255
im_parcels = (GRT1 < 255).astype(np.uint8)
N1, im_parcels1 = cv2.connectedComponents(im_parcels)

print('Nb of parcels before removal: %d'%(N0 + N1))

print('Mowed')
update_progress(0)
for n in range(1, N1 + 1):
    t_start = time()
    
    parc_size = np.sum(im_parcels1 == n)
    if parc_size < 100 or parc_size > 10000:
        GRT1[im_parcels1 == n] = 255

    update_progress((n-1)/(N1-0.9), (time()-t_start)*(N1-n-1))
update_progress(1)

print('Not mowed')
update_progress(0)
for n in range(1, N0 + 1):
    t_start = time()
    
    parc_size = np.sum(im_parcels0 == n)
    if parc_size < 100 or parc_size > 10000:
        GRT0[im_parcels0 == n] = 255

    update_progress((n-1)/(N0-0.9), (time()-t_start)*(N0-n-1))
update_progress(1)

print('Shrinking')
update_progress(0)
kernel = np.ones((3,3),np.uint8)
GRT0 = cv2.dilate(GRT0,kernel,iterations = 1)
GRT1 = cv2.dilate(GRT1,kernel,iterations = 1)
update_progress(1)

GRT = np.minimum(GRT0, GRT1)

im_parcels = (GRT0 < 255).astype(np.uint8)
N0, im_parcels0 = cv2.connectedComponents(im_parcels)

im_parcels = (GRT1 < 255).astype(np.uint8)
N1, im_parcels1 = cv2.connectedComponents(im_parcels)

im_parcels1[im_parcels1 != 0] = im_parcels1[im_parcels1 != 0] + np.max(im_parcels0)
im_parcels = im_parcels0 + im_parcels1

print('Nb of parcels after removal: %d'%(N0 + N1))


# Save parcel id
imsave('/'.join(args.groundtruth.split('/')[:-1]) + '/parcels.tif', im_parcels)

# Save groundtruth & parcels size
imsave(args.groundtruth, GRT)