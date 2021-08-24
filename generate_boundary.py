import geopandas as gpd
import os 
import elevation
import rasterio
from rasterio import mask
import subprocess

#path to directory containing the NHDPLUS_H_1711_HU4_GDB folder
data_path = "/Volumes/MyDrive/nooksack-landlab"

gdf = gpd.read_file(
	os.path.join(data_path, "NHDPLUS_H_1711_HU4_GDB/NHDPLUS_H_1711_HU4_GDB.gdb"), 
	layer=65
)
nf_poly = gdf.iloc[6].geometry.union(gdf.iloc[106].geometry)
gdf_single = gpd.GeoDataFrame(geometry = [nf_poly])
gdf_single = gdf_single.set_crs(gdf.crs)
gdf_single.to_file(
	os.path.join(data_path, "nf_nooksack.geojson"),
	driver='GeoJSON'
)