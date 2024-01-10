# %%
import geopandas as gpd
import os 
from rasterio import mask
import fiona
import pandas as pd

# %%
# MODIFY THIS 
# (path to directory containing the NHDPLUS_H_1711_HU4_GDB folder)
data_path = "/Users/elischwat/Library/CloudStorage/GoogleDrive-elilouis@uw.edu/My Drive/nooksack-landlab"

# %%
layers = fiona.listlayers(os.path.join(data_path, "NHDPLUS_H_1711_HU4_GDB/NHDPLUS_H_1711_HU4_GDB.gdb"))

# %%
gdf = gpd.read_file(
	os.path.join(data_path, "NHDPLUS_H_1711_HU4_GDB/NHDPLUS_H_1711_HU4_GDB.gdb"), 
	layer=65
)

# %%
gdf.to_file(
	os.path.join(data_path, "huc8.geojson"),
	driver='GeoJSON'
)

# %%
data_path

# %%
nf_poly = gdf.iloc[6].geometry.union(gdf.iloc[106].geometry)
sf_poly = gdf.iloc[54].geometry
mf_poly = gdf.iloc[80].geometry

# %%

gdf_single = gpd.GeoDataFrame(
	pd.DataFrame({'name': ['North Fork Nooksack River', 'Middle Fork Nooksack River', 'South Fork Nooksack River']}),
	geometry = [nf_poly, mf_poly, sf_poly])

# %%
gdf_single

# %%
gdf_single.plot()

# %%
gdf_single = gdf_single.set_crs(gdf.crs)
gdf_single.to_file(
	os.path.join(data_path, "nooksack_forks.geojson"),
	driver='GeoJSON'
)
