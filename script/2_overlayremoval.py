import cv2
import numpy as np
from tifffile import imsave, imread
from time import time
from progressbar import update_progress
import argparse

parser=argparse.ArgumentParser(
    description='''Remove overlaying parcels''')
parser.add_argument('-c0','--class0', help='Image of class 0', required=True)
parser.add_argument('-c1','--class1', help='Image of class 1', required=True)
args=parser.parse_args()


res_i = (0,7000)
res_j = (2500,9500)

# Not mowed
GRT0 = imread(args.class0)
# Mowed
GRT1 = imread(args.class1)
# Resizing
GRT0 = GRT0[res_i[0]:res_i[1],res_j[0]:res_j[1]]
GRT1 = GRT1[res_i[0]:res_i[1],res_j[0]:res_j[1]]

# Pixel identification
# Each not mowed parcels will get a unique value in an id image
im_parcels = (GRT0 < 255).astype(np.uint8)
N0, im_parcels0 = cv2.connectedComponents(im_parcels)

# Each mowed parcels will get a unique value in an id image
im_parcels = (GRT1 < 255).astype(np.uint8)
N1, im_parcels1 = cv2.connectedComponents(im_parcels)


print('Overlay removal')
update_progress(0)

# Removing overlaying unmowed parcels
nbrem = 0
for n in range(1, N0):
    t_start = time()
    
    if np.min(GRT1[im_parcels0 == n]) == 1:
        GRT0[im_parcels0 == n] = 255
        nbrem += 1
        
    update_progress((n-1)/(N0-0.9), (time()-t_start)*(N0-n-1))

####################
## Pixel identification
#im_parcels = (GRT0 < 255).astype(np.uint8)
#N0, im_parcels0 = cv2.connectedComponents(im_parcels)

#im_parcels = (GRT1 < 255).astype(np.uint8)
#N1, im_parcels1 = cv2.connectedComponents(im_parcels)

#im_parcels1[im_parcels1 != 0] = im_parcels1[im_parcels1 != 0] + np.max(im_parcels0)
#im_parcels = im_parcels0 + im_parcels1

## Save parcels
#imsave(args.class0.split('/')[:-1] + '/parcels.tif', im_parcels)
###################

# Merge groundtruth mowed and unmowed images
GRT = np.minimum(GRT0, GRT1)
# Save the final groundtruth image
imsave('/'.join(args.class0.split('/')[:-1]) + '/groundtruth.tif', GRT)

update_progress(1)

print('Nb of parcels removed %d'%(nbrem))

print()
