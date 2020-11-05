import numpy as np
from tifffile import imread
from time import time
from progressbar import update_progress
import argparse

parser=argparse.ArgumentParser(
    description='''Create and save the contextual dataset (altitude only for now)''')
parser.add_argument('-a','--altitude', help='Altitude map', required=True)
parser.add_argument('-p','--parcels', help='Parcel image', required=True)
#EXEMPLE-parser.add_argument('-r','--rain', help='Rain map', required=True)
args=parser.parse_args()


update_progress(0)

res_i = (0,7000)
res_j = (2500,9500)

# Open the altitude image and the parcel label image
im_alti = imread(args.altitude)
im_parcels = imread(args.parcels)
#EXEMPLE-im_rain = imread(args.rain)

# Crop the altitude image to match the parcel label one
im_alti = im_alti[res_i[0]:res_i[1],res_j[0]:res_j[1]]
#EXEMPLE-im_rain = im_rain[res_i[0]:res_i[1],res_j[0]:res_j[1]]

N = np.max(im_parcels) # nb of parcels
context = np.zeros((N, 1))
#EXEMPLE-context = np.zeros((N, 2))

# Collecting mean altitude for each parcels in an array of contextual data (we may add other data to this array by using the coments 'EXEMPLE-' code in this file)
for n in range(1, N+1):
    t_start = time()
    parc_mask = (im_parcels == n)
    context[n-1, 0] = np.mean(im_alti[parc_mask]) # Mean altitude over the entire parcel
    #EXEMPLE-context[n-1, 1] = np.mean(im_rain[parc_mask]) # Mean rain over the entire parcel
    update_progress((n-1)/(N-0.9), (time()-t_start)*(N-n-1))
    
context = context.astype('uint16')

np.save('/'.join(args.altitude.split('/')[:-1]) + '/context.npy', context)

update_progress(1)

print()
