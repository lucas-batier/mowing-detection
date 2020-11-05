# Mowing/Grazing detection
Automatic detection of mowing and grazing from Sentinel images in the French Alps through deep learning approaches.

# Process
The following process specify how to collect data, treat them and predict mowing from my end of study project at Laboratoire d'écologie Alpines (LECA) (Grenoble). This process is created for computer scientist or people who, at least, know how to use python3 and install needed packages with pip.


1. Download preprocess S1 tiled and S2 corrected images from PEPS
2. Organize downloaded images in the predefined folder architecture
3. Compute vegetation indices from S2 images
4. Compute and filter the groundtruth and the dataset from reference files and Sentinel images
5. Launch the learning and testing of the multimodal-temporal detector


# 1 Preprocessed images downloading

## Criteria selection
1. Go on the [PEPS Explore tab](https://peps.cnes.fr/rocket/#/search?maxRecords=50)
### SENTINEL-1
2. Select the region of interest by drawing on the map, then select the criteria in the item list on the left (example below for Écrin National Park region of interest on years 2018-2019)

![S1 criteria selection](https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/S1select.png)

3. Select the product you need by the checking boxes in the list below the map and click on <img src="https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/addtoprocenter.png" alt="drawing" height="27"/>

![S1 list selection](https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/S1list.png)

### SENTINEL-2
2. Select the region of interest by tile in the item list on the left, then select the criteria in the item list on the left (example below for tile 31TGK on years 2018-2019)

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


# 2 Folder architecture

The folder architecture is essential for the further processing such as the vegetation index.

1. Save the downloaded products (images or folder of images) by the following folder architecture

<pre>
parentfolder/tile/year/SENTINEL-X/products
</pre>

*Example for SENTINEL-1, tile 31TGK and year 2018*
<pre>
parentfolder/31TGK/2018/SENTINEL-1/s1*.tiff
</pre>

*Example for SENTINEL-2, tile 31TGK and year 2019*
<pre>
parentfolder/31TGK/2019/SENTINEL-2/SENTINEL2*/
</pre>

NB: The SENTINEL-2 products are folders while SENTINEL-1's are images)

2. Move the `Scripts/` directory of this Git in the `Parentfolder`


# 3 Vegetation index

To compute the vegetation index images use the `vegindex.py` script. Depending on the number of S2 images it may take a while (1 day for 2 years of images). Moreover it takes a lot of memory (openning and writing of multiple bands in the same time), therefore we put many 'memory release' code but with a processor with less than 16GB of RAM it will crash anyway for this resolution (10980 x 10980).

*EXAMPLE* for tile 31TGK on year 2018 and 2019

<pre>
python3 vegindex.py ../31TGK/2018/SENTINEL-2/* ../31TGK/2019/SENTINEL-2/*
</pre>


# 4 Groundtruth and Dataset

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

## Parcel filtering and dataset computation

The parcel filtering and dataset creation is performed in 6 steps which can be done separately **in the right order**, or directly by `filtering_n_dataset.py`

1. Select only meadows, grasslands and woody moorlands in OSO images and formalizing class 1 images (`1_prefilter.py`)
2. Remove overlayer parcels (`2_overlayremoval.py`) NB: the images are also resized to decrease the computation time of next process
3. Remove too small (< 1 hectare) and too big (> 100 hectares) parcels, crop them and save the final parcels' image (`3_sizeremoval.py`)
4. Compute the groundtruth vector (`4_groundtruthvect.py`)
5. Compute the contextual dataset (`5_contextualdataset.py`), for now only altitude
6. Compute the modal dataset (`6_modaldataset.py`), this step is truly long (almost 1 week for 4000 parcels with 17 modes on 144 images, 2 years with a 5 days frequency) it could be a good idea to do it separately

`filtering_n_dataset.py` script:

*Input*

- `--class0` path to the unmowed parcel image
- `--class1` path to the mowed parcel image
- `--altitude` path to the altitude map image
- `--datesgrid` path to dates grid csv file
- `--tiledir` path to the tile **directory** (e.g. 31TGK shown in section [2 Folder architecture](#2-folder-architecture))

*Output* [All in the script folder]

- `parcels.tif` image containing parcels localisation and labels (from 1 to the number of parcels)
- `grt.npy` groundtruth vector containing parcels groudtruth values (1 for mowed, 0 for unmowed)

*Example*

<pre>
python3 filtering_n_dataset.py --class0 path/to/mowing0.tif --class1 path/to/mowing1.tif --altitude path/to/alti.tif --datesgrid path/to/dategrid.csv --tiledir path/to/31TGK
</pre>

# 5 Learning and testing

Launch the learning and the testing of the model by the `model.py` script:

*Input*

- `--mode` path to the modal dataset array
- `--context` path to the contextual dataset array
- `--labels` path to the groundtruth labels array

*Output*

- AUC results for each folds

*Example*

<pre>
python3 model.py --mode path/to/mode.npy --context path/to/context.npy --labels path/to/labels.npy
</pre>

NB: This model was made in a truly coarse manner (in less than 2 months), do not rely a lot on it




