# EXDECUTE ALL FILTERING SCRIPTS
import os
import argparse

parser=argparse.ArgumentParser(
    description='''Complete filtering on groundtruth images''')
parser.add_argument('-c0','--class0', help='Image of class 0', required=True)
parser.add_argument('-c1','--class1', help='Image of class 1', required=True)
args=parser.parse_args()

os.system('python3 1_osofilter.py -c0 ' + args.class0 + ' -c1 ' + args.class1)

os.system('python3 2_overlayremoval.py -c0 ' + args.class0 + ' -c1 ' + args.class1)

os.system('python3 3_sizeremoval.py -g ' + '/'.join(args.class0.split('/')[:-1]) + '/groundtruth.tif')

os.system('python3 4_groundtruthvect.py -g ' + '/'.join(args.class0.split('/')[:-1]) + '/groundtruth.tif' + ' -p ' + '/'.join(args.class0.split('/')[:-1]) + '/parcels.tif')



