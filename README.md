# Mowing modelling
Mowing modelling in Alpine's area from remote sensing images by machine learning algorithm

# Process
1. Download preprocess S1 tiled and S2 corrected images from PEPS
2. Compute vegetation indices from S2 images: vegindex.py
3. Compute the groundtruth from PNE shapefile: groundtruth.py
4. Create the dataset from all remote sensing images and groundtruth data
5. Launch the multimodal-temporal mowing predictor model learning: learning.py
6. Predict mowing from remote sensing images through the model: predict.py

# Preprocessed images downloading

## Criteria selection
1. Go on the [PEPS Explore tab](https://peps.cnes.fr/rocket/#/search?maxRecords=50)

### SENTINEL-1
2. *SENTINEL-1* Select the region of interest by drawing on the map, then select the criteria in the item list on the left (example below for Écrin National Park region of interest on year 2018-2019)

![S1 criteria selection](/Users/batierl/Documents/2-Works/LECA/Git/S1select.png "S1 criteria selection")

3. Select the product you need by the checking boxes in the list below the map and click on `ADD TO PROCESSING CENTER` 

***IMAGE***

### SENTINEL-2
2. *SENTINEL-2* Select the region of interest by tile in the item list on the left, then select the criteria in the item list on the left (example below for tile 31TGK on year 2018-2019)

***IMAGE***

3. Select the product you need by the checking boxes in the list below the map and click on add to processing center

***IMAGE***

### Preprocessing

4. Go to the processing center by clicking on the gears on the top right of the page

5. Select the processing you need (S1Tiling for S1 - MAJA for S2)

6. Select the product you want to process

7. Launch the processing by clicking on `PROCESS PRODUCTS` 

### Downloading

8. When the process is done (you can check its state in `MY JOBS`) go to `MY RESULTS` and download the results
