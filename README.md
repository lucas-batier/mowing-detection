# Mowing modelling
Mowing modelling in Alpine's area from remote sensing images by machine learning algorithm

# Process
The following process specify how to collect data, treat them and predict mowing from my end of study project at Laboratoire d'écologie Alpines (Grenoble).

1. Download preprocess S1 tiled and S2 corrected images from PEPS
2. Organize downloaded images in the predefined folder architecture
3. Compute vegetation indices from S2 images
4. Compute the groundtruth from reference files
5. Create the dataset from all remote sensing images and groundtruth data
6. Launch the multimodal-temporal mowing predictor model learning
7. Predict mowing from remote sensing images through the model

# 1. Preprocessed images downloading

## Criteria selection
1. Go on the [PEPS Explore tab](https://peps.cnes.fr/rocket/#/search?maxRecords=50)
### SENTINEL-1
2. Select the region of interest by drawing on the map, then select the criteria in the item list on the left (example below for Écrin National Park region of interest on year 2018-2019)

![S1 criteria selection](https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/S1select.png)

3. Select the product you need by the checking boxes in the list below the map and click on <img src="https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/addtoprocenter.png" alt="drawing" height="27"/>

![S1 list selection](https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/S1list.png)

### SENTINEL-2
2. Select the region of interest by tile in the item list on the left, then select the criteria in the item list on the left (example below for tile 31TGK on year 2018-2019)

![S2 criteria selection](https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/S2select.png)

3. Select the product you need by the checking boxes in the list below the map and click on <img src="https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/addtoprocenter.png" alt="drawing" height="27"/>

![S2 list selection](https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/S2list.png)

### Preprocessing
4. Go to the processing center by clicking on the gears ![PEPS gears](https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/pepsgears.png) on the top right of the page
5. Select the processing you need (S1Tiling for S1 - MAJA for S2)
6. Select the products you want to process
7. Launch the processing by clicking on <img src="https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/procprod.png" alt="drawing" height="27"/> 

### Downloading

8. The process state can be checked in <img src="https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/jobs.png" alt="drawing" height="27"/>
9. When the process is done, go to <img src="https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/results.png" alt="drawing" height="27"/> and download the products

# 2. Folder architecture

1. Save the downloaded products (images or folder of images) by the following folder architecture

<pre>
parentfolder/tile/year/SENTINEL-X/products
</pre>

*SENTINEL-1*
<pre>
parentfolder/tile/year/SENTINEL-1/s1*.tiff
</pre>

*SENTINEL-2*
<pre>
parentfolder/tile/year/SENTINEL-2/SENTINEL2*/
</pre>

2. Move the `Scripts/` directory of this Git in the `Parentfolder`

# 3. Vegetation index

To compute the vegetation index images use the `vegindex.py` script, depending on the number of S2 images it may take a while (1 day for 2 years of images)

*EXAMPLE* for tile 31TGK on year 2018 and 2019

<pre>
python3 vegindex.py ../31TGK/2018/SENTINEL-2/* ../31TGK/2019/SENTINEL-2/*
</pre>

# 4. Groundtruth

## Reference data

The aim for our references is to collect class 1 (mowed) and class 0 (not mowed lands)

### Class 1 (Mowed)
Delphine DB collected global mowing area in Écrins National Park.

### Class 0 (Not Mowed)
The CNES provide the [OSO](https://www.theia-land.fr/en/ceslist/land-cover-sec/) land map who give nice information (woodlands, grasslands and meadows) for class 0. It can be downloaded [here](https://theia.cnes.fr/atdistrib/rocket/#/search?collection=OSO)

## Class merging

Groundtruth image is processed by QGIS, downloadable [here](https://qgis.org/en/site/forusers/download.html)

Thus, open QGIS:

### Class 1
1. Add the Delphine DB raster (`DB/Delphine/Mowing.img`) as a layer (`Layer` - `Add Layer` - `Add Raster Layer`)

<img src="https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/addraslayer.png" alt="drawing" width="520"/>

2. Right click on the Delphine DB layer in the bottom left, go to `Export - Save As...`

<img src="https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/saveas.png" alt="drawing" width="700"/>

3. In the popup menu:
   1. Choose `GEOTIFF` as file format
   2. Write `mowing1.tif` as file name
   3. Choose `EPSG:32631 - WGS 84 / UTM zone 31N` as reference system
   4. Define the `Extent` coordinates as `5000040`N, `809760`E, `699960`W and `4890240`S
   5. Force the resolution to `10` x `10`
   6. Click on `OK`
   7. Move the external file in DB/Mowing/
   
<img src="https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/exportqgis1.png" alt="drawing" width="700"/>

### Class 0
1. Add the OSO raster (`DB/OSO/OSC_20XX.tif`) as a layer (`Layer` - `Add Layer` - `Add Raster Layer`)
2. Right click on the OSO layer in the bottom left, go to `Export - Save As...`
3. In the popup menu: do exactly the same as for class 1 but write `mowing0.tif` as file name

<img src="https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/exportqgis0.png" alt="drawing" width="700"/>

## Parcel filtering

The parcel filtering is performed in 4 steps which can be done separately **in the right order**, or directly by `filtering.py`

1. Select only woody moorlands, grasslands and meadows in OSO images and formalizing class 1 images (`1_osofilter.py`)
2. Remove overlayer parcels (`2_overlayremoval.py`)
3. Remove too small (< 1 hectare) and too big (> 100 hectare) parcels, crop them and save the final parcels' image (`3_sizeremoval.py`)
4. Create the final groundtruth vector (`4_groundtruthvect.py`)

`filtering.py` script:

*Input*

- `--class0` path to the unmowed parcel image
- `--class1` path to the mowed parcel image

*Output* [All in the script folder]

- `parcels.tif` image containing parcels localisation and numbers
- `grt.npy` groundtruth vector containing parcels labels

*Example*

<pre>
python3 filtering.py --class0 path/to/mowing0.tif --class1 path/to/mowing1.tif
</pre>

## Date grid

The dategrid is created by searching for a SENTINEL-1 - SENTINEL-2 correspondancy (according to their high revisit frequency, SENTINEL-1 images are selected by nearest-neighbours approximation)

`dategrid.py` script:

*Input*

- `--folder` path to the parentfolder containing *tile/year/SENTINEL-X/**

*Output* [All in the script folder]

- `dategrid.csv` dategrid correspondancy between SENTINEL-1 and SENTINEL-2

*Example*

<pre>
python3 dategrid.py --folder path/to/parentfolder
</pre>

# 5. Dataset

The dataset creation is truly long (almost 1 week for 17 modes on 144 images, 2 years with a 5 days frequency)

`dataset.py` script:

*Input*

- `--` 

*Output* [All in the script folder]

- ``

*Example*

<pre>
python3 dataset.py -- 
</pre>





