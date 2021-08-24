# This notebook needs the `mukey_ksat.csv` file produced by the `ssurgo_ksat_aggregation.py` notebook

import pandas as pd
import rasterio
from matplotlib import pyplot
import holoviews as hv
import numpy as np
from holoviews.operation.datashader import rasterize
hv.extension('bokeh')

# ## Open the gSSURGO mukey and ksat table created in the other notebook

table = pd.read_csv('mukey_soildepth.csv')

table

# ## Open the gSSURGO 1m mukey raster

src = rasterio.open("/Users/elischwat/Downloads/MapunitRaster_10m.tif")
data_array = src.read(1)
img = hv.Image(data_array)
rasterize(img)

# ## Crop the mukey raster to the nf nooksack boundary

# ! gdalwarp -crop_to_cutline \
#     -cutline nf_nooksack.geojson \
#     /Users/elischwat/Downloads/MapunitRaster_10m.tif \
#     /Users/elischwat/Downloads/MapunitRaster_10m_nf_nooksack.tif


src = rasterio.open("/Users/elischwat/Downloads/MapunitRaster_10m_nf_nooksack.tif")
data_array = src.read(1)
img = hv.Image(data_array)
rasterize(img)

# ## Replace mukey raster values with associated ksat values

mukey_raster = rasterio.open("/Users/elischwat/Downloads/MapunitRaster_10m_nf_nooksack.tif")
mukey_array = mukey_raster.read(1)

all_mukeys = list(set(mukey_array.flatten()))

# #### Find which mukeys have associated ksat data in our generated table

len(all_mukeys), len(table[table.mukey.isin(all_mukeys)])

# So 6 are missing ksat data

# ## Create new raster

depthmap = pd.Series(
    table.max_soil_depth.values,
    index=table.mukey
).to_dict()
def get_depth_from_mukey(mukey):
    return depthmap.get(mukey, np.NaN)


depth_array = np.vectorize(get_depth_from_mukey)(mukey_array)

mukey_array

# #### Write to disk

nodata_value = -9999

depth_array = np.nan_to_num(depth_array, nan=nodata_value)

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
    
    
    outfile = '/Users/elischwat/Downloads/soildepth_raster_10m_nf_nooksack.tif'
    print(f"Saving to {outfile}")
    with rasterio.open(
        outfile, 
        'w', **profile) as dst:
        dst.write(depth_array.astype(rasterio.float32), 1)