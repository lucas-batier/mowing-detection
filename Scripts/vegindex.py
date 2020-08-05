import numpy as np
import cv2
from PIL import Image
from glob import glob
from progressbar import update_progress
import sys
import argparse

parser=argparse.ArgumentParser(
    description='''Compute vegetation indices from SENTINEL-2 multispectral bands''')
parser.add_argument('-f','--folders', nargs='+', help='List of folders to be processed', required=True)
args=parser.parse_args()


def nari(G, R_E):
    np.seterr(divide='ignore', invalid='ignore') # Unset divide by 0 and inf-inf error
    NARI = (1/G - 1/R_E)/(1/G + 1/R_E) # Computation of the index
    NARI[np.isnan(NARI)] = 0 # Dealing with nan values
    NARI = np.clip(NARI, NARI[NARI!=-np.inf].min(), NARI[NARI!=np.inf].max()) # Dealing with inf values
    return np.clip(NARI, -1., 1)

def evi(B, R, NIR, G=2.5, C1=6., C2=7.5, L=1.):
    np.seterr(divide='ignore', invalid='ignore')
    EVI = G*(NIR-R)/(NIR+C1*R-C2*B+L)
    EVI[np.isnan(EVI)] = 0
    return np.clip(EVI, -1., 1.)

def ndvi(R, NIR):
    np.seterr(divide='ignore', invalid='ignore')
    NDVI = (NIR-R)/(NIR+R)
    NDVI[np.isnan(NDVI)] = 0
    return np.clip(NDVI, -1., 1)

def savi(R, NIR, L=0.5):
    np.seterr(divide='ignore', invalid='ignore')
    SAVI = (1+L)*(NIR-R)/(NIR+R+L)
    SAVI[np.isnan(SAVI)] = 0
    return np.clip(SAVI, -1., 1)



def folder(images_directory, res_type='FRE', im_format='tif'):
    '''
    Input: Images directory (location of SENTINEL-2 *FOLDER*)
           Resolution type (default FRE : Full REsolution)
           Image format (default TIF)
    Process: Writting of vegetation index images in specified format and in specified folder
    Output: Surprise (if it works well TT)
    '''
    
    images_dir = glob(images_directory + '/*')

    I = len(images_dir)
    for i, im_dir in enumerate(images_dir):
        
        update_progress(max(0,(i-4/5))/(I-0.9))
        B3 = cv2.imread(glob(im_dir + '/*_' + res_type + '_' + 'B3.' + im_format)[0], -1).astype('float32')
        B5 = cv2.imread(glob(im_dir + '/*_' + res_type + '_' + 'B5.' + im_format)[0], -1).astype('float32')
        B5 = cv2.resize(B5, (10980,10980), 2, 2, cv2.INTER_CUBIC)
        
        im = Image.fromarray(nari(B3, B5).astype('float32'))
        im.save(glob(im_dir + '/*_FRE_B2.tif')[0][:-6] + 'NARI.' + im_format)
        im = None # release memory
        
        B3 = None # release memory
        B5 = None # release memory
        
        
        update_progress(max(0,(i-3/5))/(I-0.9))
        B4 = cv2.imread(glob(im_dir + '/*_' + res_type + '_' + 'B4.' + im_format)[0], -1).astype('float32')
        B8 = cv2.imread(glob(im_dir + '/*_' + res_type + '_' + 'B8.' + im_format)[0], -1).astype('float32')
        
        im = Image.fromarray(ndvi(B4, B8).astype('float32'))
        im.save(glob(im_dir + '/*_FRE_B2.tif')[0][:-6] + 'NDVI.' + im_format)
        im = None # release memory
        
        
        update_progress(max(0,(i-2/5))/(I-0.9))
        im = Image.fromarray(savi(B4, B8).astype('float32'))
        im.save(glob(im_dir + '/*_FRE_B2.tif')[0][:-6] + 'SAVI.' + im_format)
        im = None # release memory
        
        
        update_progress(max(0,(i-1/5))/(I-0.9))
        B2 = cv2.imread(glob(im_dir + '/*_' + res_type + '_' + 'B2.' + im_format)[0], -1).astype('float32')
        im = Image.fromarray(evi(B2, B4, B8).astype('float32'))
        im.save(glob(im_dir + '/*_FRE_B2.tif')[0][:-6] + 'EVI.' + im_format)
        im = None # release memory
        
        B2 = None # release memory
        B4 = None # release memory
        B8 = None # release memory
        
        update_progress(i/(I-0.9))

    return True

for images_directory in args.folders:
    print()
    print('Processing of ''%s'''%(images_directory))
    
    update_progress(0)
    if folder(images_directory):
        update_progress(1)

print('Everything''s done !')
    
