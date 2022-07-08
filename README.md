# Download Raw Data Sources for the Nooksack Watershed
Download the following datasets from external sources. Unzip all the files when they are done downloading so that the following steps can be completed. Place them in a single directory.

## GSSURGO
gSSURGO_WA.zip
Downloaded from...
https://nrcs.app.box.com/v/soils/file/699219396665

## National Hydrography Dataset
NHDPLUS_H_1711_HU4_GDB-20210202T161301Z-001.zip
To download again
Find relevant HUC8 watershed code by going through the maps here
https://water.usgs.gov/wsc/map_index.html

Download data for that area here
http://prd-tnm.s3-website-us-west-2.amazonaws.com/?prefix=StagedProducts/Hydrography/NHD/HU4/HighResolution/GDB/

## National Land Cover Dataset
NLCD_2016_Land_Cover_L48_20190424.zip
Downloaded from...
https://www.mrlc.gov/data?f%5B0%5D=category%3Aland%20cover

# Generate data for the Nooksack watershed
These steps take the raw data that we downloaded from external sources and generates the data we need 
to actually run Landlab.

## Modifying scripts to run on your local machine
Inline comments saying "MODIFY THIS" in the python scripts indicate where one must change a file/folder path to their local path.

## Boundary shapefile
Generate the polygon boundary of the NF Nooksack watershed by running the python script.
This script simply takes two watersheds from the HU4 level (upper and lower NF Nooksack watersheds)
and combines them into one polygon, saving the result to a geojson file.
```
python generate_boundary.py
```

## DEM
Create a 30m DEM in the ESRI/ASCII Grid format for the NF Nooksack watershed by running the python script.
```
python generate_dem.py
```
This script: 
1. Downloads SRTM DEM data for the envelope of the boundary created in the previous step and saves the DEM to a file "dem_30m.tif".
2. Masks the DEM created in step 1 to the extent of the boundary and saves the result to a file "dem_30m_clipped.tif".
3. Creates a DEM warped to CRS EPSG 32610 (UTM 10N) using gdalwarp and saves the result to a file "dem_30m_clipped_utm10n.tif"
4. Converts this file to AAIGrid format, saving the result to a file "dem_30m_clipped_utm10n.asc" (along with other metadata files required by the AAIGrid format).

## Create tables of gSSURGO data
Run the following two scripts:
ssurgo_ksat_aggregation.py
ssurgo_soildepth_aggregation.py

## Create rasters of ksat and soil depth
ssurgo_ksat_rasterization.py
ssurgo_soildepth_rasterization.py
