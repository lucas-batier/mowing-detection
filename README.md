# Mowing modelling
Mowing modelling in Alpine's area from remote sensing images by machine learning algorithm

# Process
1. Download preprocess S1 tiled and S2 corrected images from PEPS
2. Organize downloaded images in the predefined folder architecture
3. Compute vegetation indices from S2 images
4. Compute the groundtruth from reference files
5. Create the dataset from all remote sensing images and groundtruth data
6. Launch the multimodal-temporal mowing predictor model learning
7. Predict mowing from remote sensing images through the model

# Preprocessed images downloading

## Criteria selection
1. Go on the [PEPS Explore tab](https://peps.cnes.fr/rocket/#/search?maxRecords=50)
### SENTINEL-1
2. *SENTINEL-1* Select the region of interest by drawing on the map, then select the criteria in the item list on the left (example below for Écrin National Park region of interest on year 2018-2019)

![S1 criteria selection](https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/S1select.png)

3. Select the product you need by the checking boxes in the list below the map and click on `ADD TO PROCESSING CENTER` 

![S1 list selection](https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/S1list.png)

### SENTINEL-2
2. *SENTINEL-2* Select the region of interest by tile in the item list on the left, then select the criteria in the item list on the left (example below for tile 31TGK on year 2018-2019)

![S2 criteria selection](https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/S2select.png)

3. Select the product you need by the checking boxes in the list below the map and click on add to processing center

![S2 list selection](https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/S2list.png)

### Preprocessing
4. Go to the processing center by clicking on the gears ![PEPS gears](https://github.com/lucasbat20/Grazing-modelling/blob/master/Images/pepsgears.png) on the top right of the page
5. Select the processing you need (S1Tiling for S1 - MAJA for S2)
6. Select the products you want to process
7. Launch the processing by clicking on `PROCESS PRODUCTS` 

### Downloading

8. The process state can be checked in `MY JOBS`
9. When the process is done, go to `MY RESULTS` and download the products

# Folder architecture

Save the downloaded products (images or folder of images) by the following folder architecture

<pre>
Parentfolder/Tile/Year/SENTINEL-X/Products
</pre>

*SENTINEL-1*
<pre>
Parentfolder/Tile/Year/SENTINEL-1/s1*.tiff
</pre>

*SENTINEL-2*
<pre>
Parentfolder/Tile/Year/SENTINEL-2/SENTINEL2*/
</pre>

Save 

Copy this git directory in the `Parentfolder`

# Vegetation index

To compute the vegetation index images launch the `vegindex.py` script, depending on the number of S2 images it may take a while (1 day for 2 years)

N.B.: if the folder architecture is correct, everything should work instantly

# Groundtruth

## Reference data

The aim for our references is to collect class 1 (mowed or grazed) and class 0 (woodlands, grasslands and meadows)

### Class 1 (Mowed)
Delphine DB collected global mowing and grazing area in Écrins National Park.

### Class 0 (not mowed)
The CNES provide the [OSO](https://www.theia-land.fr/en/ceslist/land-cover-sec/) map who give nice information for class 0. It can be downloaded [here](https://theia.cnes.fr/atdistrib/rocket/#/search?collection=OSO)

## Class merging

Groundtruth image is processed by QGIS, downloadable [here](https://qgis.org/en/site/forusers/download.html)

Then, in QGIS:
1. Add the S2 raster (`DB/S2Tile/S2Tile.tiff`) as a layer (`Layer` - `Add Layer` - `Add Raster Layer`)
### Class 1
2. Add the Delphine DB raster (`DB/Delphine/Mowing.img`) as a layer (`Layer` - `Add Layer` - `Add Raster Layer`)
3. Right click on the Delphine DB layer in the bottom left go to `Export - Save As...`
4. In the popup menu:
   1. Choose GEOTIFF as file format
   2. Choose mowing1_qgis.tif as file name
   3. Choose EPSG:32631 - WGS 84 / UTM zone 31N
   4. Click on `Calculate from Layer` in the Extent rectangle and choose the S2 layer
   5. Force the resolution to `10` `10`
   6. Click on `OK`
   7. Move the external file in DB/Mowing/
   
***IMAGE***

### Class 0
2. Add the OSO raster (`DB/OSO/OSC_20XX.tif`) as a layer (`Layer` - `Add Layer` - `Add Raster Layer`)
3. Right click on the Delphine DB layer in the bottom left go to `Export - Save As...`
4. In the popup menu: do exactly the same as for class 1 but put mowing0_qgis.tif as file name

***IMAGE***

## Parcel filtering
1. Select only woodlands, grasslands and meadows OSO parcels (**1_MOW_osofilter.py**)
2. Remove overlayer parcels (**2_MOW_overlayremoval.py**)
3. Remove too small (< 1 hectare) and too big (> 100 hectare) parcels (**3_MOW_sizeremoval.py**)
3. Create the final groundtruth vector (**4_MOW_groundtruthvect.py**)

# Dataset

The dataset is automatically created (**5_MOW_dataset.py**), nevertheless it can be truly long, almost 1 week for 3 S1 polarization, 10 S2 images and 4 vegetation indices on 2 years





