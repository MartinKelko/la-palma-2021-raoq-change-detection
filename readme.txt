WORKFLOW

SINGLE-BAND ANALYSIS
|
|---> Spectral ---> bands
			   ---> indices

|---> RaoQ c   ---> bands
			   ---> indices
			   
RaoQ MULTIDIMENSIONAL ANALYSIS
|
|---> multidimensional combinations of best bands & indices
---------------------------

0 INITIALIZATION & ENVIRONMENT SETUP
0.1 imports and install libraries
0.2 Google Earth Engine initialization and authentication
0.3 Google Drive mount + listing TIFFs
0.4 Helpers

1 DATA ACQUISITION AND AOI

2 SINGLE-BAND ANALYSIS
2.1 Spectral approach

2.1.1 Spectral bands

2.1.1.1 Sentinel-1 SAR: VV, VH polarization
preprocessing
data preparation
change detection
binary maps and tables (spectral only)

2.1.1.2 Sentinel-2 MSI: B8A (NIR), B11 (SWIR1), B12 (SWIR2)
preprocessing
data preparation
change detection
binary maps and tables (spectral only)

2.1.1.3 Landsat: Thermal Infrared (TIR)
preprocessing
data preparation
change detection
binary maps and tables (spectral only)

2.1.1.4 VIIRS: night-time radiance VIIRS_NT
preprocessing
data preparation
change detection
binary maps and tables (spectral only)

2.1.1.5 VIIRS: Black Marble VIIRS_BM
preprocessing
data preparation
change detection
binary maps and tables (spectral only)

2.1.1.6 MODIS: Land Surface Temperature (MODIS)
preprocessing
data preparation
change detection
binary maps and tables (spectral only)

2.1.2 Spectral indices

2.1.2.1 NDVI (Normalized Difference Vegetation Index)
preprocessing
data preparation
change detection
binary maps and tables (spectral only)

2.1.2.2 NBR (Normalized Burn Ratio)
preprocessing
data preparation
change detection
binary maps and tables (spectral only)

2.1.2.3 MIRBI (Mid-Infrared Burn Index)
preprocessing
data preparation
change detection
binary maps and tables (spectral only)

2.1.2.4 BAIS2 (Burned Area Index for Sentinel-2)
preprocessing
data preparation
change detection
binary maps and tables (spectral only)

2.1.2.5 NIR–SWIR1 (NHI_SWNIR)
preprocessing
data preparation
change detection
binary maps and tables (spectral only)

2.1.2.6 SWIR1–SWIR2 (NHI_SWIR)
preprocessing
data preparation
change detection
binary maps and tables (spectral only)

ACCURACY ASSESMENT - spectral approach
Export spectral approach results

2.2 RaoQ classic approach

2.2.1 RaoQ classic from spectral bands

2.2.1.1  Sentinel-1 SAR: VV, VH polarization
preprocessing
data preparation
change detection
binary maps and tables (RaoQ only)

2.2.1.2 Sentinel-2 MSI: B8A (NIR), B11 (SWIR1), B12 (SWIR2)
preprocessing
data preparation
change detection
binary maps and tables (RaoQ only)

2.2.1.3 Landsat: Thermal Infrared (TIR)
preprocessing
data preparation
change detection
binary maps and tables (RaoQ only)

2.2.1.4 VIIRS: night-time radiance VIIRS_NT
preprocessing
data preparation
change detection
binary maps and tables (RaoQ only)

2.2.1.5 VIIRS: Black Marble VIIRS_BM
preprocessing
data preparation
change detection
binary maps and tables (RaoQ only)

2.2.1.6 MODIS: Land Surface Temperature (MODIS)
preprocessing
data preparation
change detection
binary maps and tables (RaoQ only)

2.2.2 RaoQ classic from spectral indices

2.2.2.1 NDVI (Normalized Difference Vegetation Index)
preprocessing
data preparation
change detection
binary maps and tables (RaoQ only)

2.2.2.2 NBR (Normalized Burn Ratio)
preprocessing
data preparation
change detection
binary maps and tables (RaoQ only)

2.2.2.3 MIRBI (Mid-Infrared Burn Index)
preprocessing
data preparation
change detection
binary maps and tables (RaoQ only)

2.2.2.4 BAIS2 (Burned Area Index for Sentinel-2)
preprocessing
data preparation
change detection
binary maps and tables (RaoQ only)

2.2.2.5 NIR–SWIR1 (NHI_SWNIR)
preprocessing
data preparation
change detection
binary maps and tables (RaoQ only)

2.2.2.6 SWIR1–SWIR2 (NHI_SWIR)
preprocessing
data preparation
change detection
binary maps and tables (RaoQ only)

ACCURACY ASSESMENT - RaoQ classic approach
Export RaoQ classic approach results
---------------------------
QGIS - ACCURACY ASSESSMENT

1  
1.1 Add CEMS reference binary data 'ref_CEMS_2021.tif' 
1.2 Add ESA WORLDCOVER reference binary data 'ESA_LULC.tif' 
1.3 Add lava flow area 'laPalma_lavaflow.gpkg'
1.4 Add outside lava flow area 'laPalma_outside_lavaflow.gpkg'

2 Clip raster by mask layer: clip 'ESA_LULC.tif' and 'laPalma_outside_lavaflow.gpkg' 

3A
3.1 Pixels values with 1 (change) within the CEMS (must be in binary format)
Processing → Raster pixels to points
Input: 'ref_CEMS_2021.tif'
Filter on vector points layer: use SQL command 'value = 1'
Processing → Random selection:  50 points
Export - Save selected features

3.2 Pixels values with 0 (no change) within the ESA WorldCover LULC (must be in binary format)
Processing → Raster pixels to points
Input: 'ESA_LULC.tif'
Filter on vector points layer: use SQL command 'value = 0'
Processing → Random selection: 250 points
Export - Save selected features

3.3 Processing → Merge vector layers → merge 'validation_points_CEMS_change_1.gpkg' and 'validation_points_ESA_LULC_nochange_0.gpkg' into 'validation points.gpkg' (attribute table must contain 150 points with 1 values and 100 points with 0 values)

3B
...or simply add 'validation_points.gpkg' from GitHub repository

4 Confusion Matrix calculations
Use Python codes in QGIS plugin for each approach (single spectral, RaoQ classic, RaoQ multidimensional)
'sample_raster_values_to_validation_points_single_md_raoq.py'
'sample_raster_values_to_validation_points_single_raoq.py'
'sample_raster_values_to_validation_points_single_spectral.py'
---------------------------
run Accuracy Assessment and Export Results blocks in Google Colab for each approach

3 RAOQ MULTIDIMENSIONAL ANALYSIS 

3.1 Helpers - in the beginning of the block, configure best single spectral bands and indices from previous results

3.2 DATA ACQUISITION AND AOI

ACCURACY ASSESMENT - RaoQ multidimensional approach
Export RaoQ multidimensional approach results
---------------------------
new accuracy metric tables will be exported to your directory path

