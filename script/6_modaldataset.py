import numpy as np
import pandas as pd
import cv2
from glob import glob
from tifffile import imread, imsave
from time import time
from progressbar import update_progress
import argparse

parser=argparse.ArgumentParser(
    description='''Create and save the modal dataset (Sentinel images)''')
parser.add_argument('-g','--groundtruth', help='Groundtruth vector', required=True)
parser.add_argument('-p','--parcels', help='Parcel image', required=True)
parser.add_argument('-d','--datesgrid', help='Dates grid array', required=True)
parser.add_argument('-t','--tiledir', help='Directory to the modal dataset', required=True)
args=parser.parse_args()


update_progress(0)

res_i = (0,7000)
res_j = (2500,9500)

# Open date correspondancy table
df_dates = pd.read_csv(args.datesgrid, index_col='Unnamed: 0')
df_dates = df_dates.drop('dates', axis=1)

# Open the groundtruth vector and the parcel labels image
GRT = np.load(args.groundtruth)
im_parcels = imread(args.parcels)

N = np.max(im_parcels) # nb of parcels
T = len(df_dates) # nb of dates
nbS2_im = len(glob(args.tiledir + '/*/*/*%s*/*.tif'%(df_dates['dateS2str'][0]))) # Number of SENTINEL-2 images
nbS1_pol = 3 # Number of SENTINEL-1 polarisation (from SAR)
nbstat = 3 # Number of statistics to compute (mean, median and standard deviation (std) for now)
m = nbstat * (nbS2_im + nbS1_pol) # nb of features: [mean, median, std] from each S1 pol, each S2 bands and vegindex

mode = np.empty((N, T, m)).astype('float32') # Dataset array with right dimensions
orbit = np.empty((T)).astype('bool') # Orbit information array (ascending or descending)

for t in range(T):
    t_start = time()
    
    path_S1 = glob(args.tiledir + '/*/*/*%s*.tif'%(df_dates['dateS1str'][t]))[0]
    all_path_S2 = glob(args.tiledir + '/*/*/*%s*/*.tif'%(df_dates['dateS2str'][t]))
    all_path_S2.sort()
    
    orbit[t] = ('DES' in path_S1)
    
    # Open and crop SENTINEL-1 image
    S1 = imread(path_S1).astype('float32')[res_i[0]:res_i[1],res_j[0]:res_j[1]]
    for n in range(1, N + 1):        
        parc_mask = (im_parcels == n) # Filter on the current parcels: all pixels to False except the pixels of the current parcel
        # For each polarization compute the statistics values
        for i in range(nbS1_pol):
            # S1 polarization
            mode[n-1,t,i*3+0] = np.mean(S1[:,:,i][parc_mask])
            mode[n-1,t,i*3+1] = np.median(S1[:,:,i][parc_mask])
            mode[n-1,t,i*3+2] = np.std(S1[:,:,i][parc_mask])
    S1 = None
    
    I = len(all_path_S2)
    for i, path_S2 in enumerate(all_path_S2):
        # Open SENTINEL-2 image
        S2 = imread(path_S2).astype('float32')
        # If the SENTINEL-2 image resolution is to low, expansion to the working one (usually from 20m/pix to the standard 10m/pix)
        if S2.shape[0] < 10980:
            S2 = cv2.resize(S2, (10980,10980), cv2.INTER_LINEAR)
        # Crop SENTINEL-2 image
        S2 = S2[res_i[0]:res_i[1],res_j[0]:res_j[1]]
        for n in range(1, N + 1):
            parc_mask = (im_parcels == n) # Filter on the current parcels: all pixels to False except the pixels of the current parcel
            # S2 band or vegindex
            mode[n-1,t,i*3+9] = np.mean(S2[parc_mask])
            mode[n-1,t,i*3+10] = np.median(S2[parc_mask])
            mode[n-1,t,i*3+11] = np.std(S2[parc_mask]) 
    S2 = None
    
    update_progress(t/(T-0.9), ((time()-t_start)*(T-t-1)))

# Save dataset array and orbit info
np.save('/'.join(args.groundtruth.split('/')[:-1]) + '/mode.npy', mode)
np.save('/'.join(args.groundtruth.split('/')[:-1]) + '/orbit.npy', orbit)

update_progress(1)

print()
