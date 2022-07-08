# %%
import geopandas as gpd
import os 
from rasterio import mask

# %%
# MODIFY THIS 
# (path to directory containing the NHDPLUS_H_1711_HU4_GDB folder)
data_path = "/Volumes/GoogleDrive/My Drive/nooksack-landlab"

# %%
import fiona

# %%
layers = fiona.listlayers(os.path.join(data_path, "NHDPLUS_H_1711_HU4_GDB/NHDPLUS_H_1711_HU4_GDB.gdb"))

# %%
gdf = gpd.read_file(
	os.path.join(data_path, "NHDPLUS_H_1711_HU4_GDB/NHDPLUS_H_1711_HU4_GDB.gdb"), 
	layer=72
)
nooksack_poly = gdf.iloc[14:15]

# %%
nooksack_poly.to_file(
	os.path.join(data_path, "nooksack.geojson"),
	driver='GeoJSON'
)

# %%
