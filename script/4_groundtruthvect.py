import numpy as np
from tifffile import imsave, imread
from time import time
from progressbar import update_progress
import argparse

parser=argparse.ArgumentParser(
    description='''Create final groundtruth vector''')
parser.add_argument('-g','--groundtruth', help='Groundtruth image', required=True)
parser.add_argument('-p','--parcels', help='Parcel image', required=True)
args=parser.parse_args()

# Open parcels label and value
GRT = imread(args.groundtruth)
im_parcels = imread(args.parcels)


update_progress(0)
N = np.max(im_parcels)
labels = np.zeros((N))
# Compute the groudtruth image in a vector according to the parcel labels
for n in range(1, N + 1):
    t_start = time()
    labels[n-1] = np.min(GRT[im_parcels == n])
    update_progress((n-1)/(N-0.9), (time()-t_start)*(N-n-1))
    
np.save('/'.join(args.groundtruth.split('/')[:-1]) + '/labels.npy', labels.astype('uint8'))

update_progress(1)

print()
