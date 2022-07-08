# This notebook needs the `mukey_ksat.csv` file produced by the `ssurgo_ksat_aggregation.py` notebook

import pandas as pd
import rasterio
import numpy as np
import rioxarray as rix
import geopandas as gpd
import os

# MODIFY THIS
data_path = "/Volumes/GoogleDrive/My Drive/nooksack-landlab"

# ## Open the gSSURGO mukey and ksat table created in the other notebook

ksat_table = pd.read_csv('mukey_ksat.csv')

# ## Open the gSSURGO 10m mukey raster
src = os.path.join(data_path, "MapunitRaster_10m.tif")
raster_src = rix.open_rasterio(src, chunk=True)
watershed_src = os.path.join(data_path, "MapunitRaster_10m_nooksack.tif")
boundary = gpd.read_file(os.path.join(data_path, "nooksack.geojson")).to_crs(raster_src.rio.crs)

# ## Crop the mukey raster to the nooksack boundary
raster_src.rio.clip(boundary.geometry).rio.to_raster(
    watershed_src
)

# ## Replace mukey raster values with associated ksat values
mukey_raster = rasterio.open(watershed_src)
mukey_array = mukey_raster.read(1)
all_mukeys = list(set(mukey_array.flatten()))

# #### Find which mukeys have associated ksat data in our generated table

len(all_mukeys), len(ksat_table[ksat_table.mukey.isin(all_mukeys)])

# So 6 are missing ksat data

# ## Create new raster

ksat_map = pd.Series(
    ksat_table.ksat_weighted_mean.values,
    index=ksat_table.mukey
).to_dict()
def get_ksat_from_mukey(mukey):
    return ksat_map.get(mukey, np.NaN)


ksat_array = np.vectorize(get_ksat_from_mukey)(mukey_array)

mukey_array

# #### Write to disk

nodata_value = -9999

ksat_array = np.nan_to_num(ksat_array, nan=nodata_value)

# Register GDAL format drivers and configuration options with a
# context manager.
with rasterio.Env():

    # Write an array as a raster band to a new 8-bit file. For
    # the new file's profile, we start with the profile of the source
    profile = mukey_raster.profile

    # And then change the band count to 1, set the
    # dtype to uint8, and specify LZW compression.
    profile.update(
        dtype=rasterio.float32,
        count=1,
        compress='lzw',
        nodata = nodata_value)
    outfile = os.path.join(data_path, "ksat_raster_10m_nooksack.tif")
    print(f"Saving to {outfile}")
    with rasterio.open(
        outfile, 
        'w', **profile) as dst:
        dst.write(ksat_array.astype(rasterio.float32), 1)
