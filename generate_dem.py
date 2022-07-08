import geopandas as gpd
import os 
import elevation
import rasterio
from rasterio import mask
import subprocess

# MODIFY THIS 
# (path to directory containing the NHDPLUS_H_1711_HU4_GDB folder)
data_path = "/Volumes/GoogleDrive/My Drive/nooksack-landlab"

dem_data_path = os.path.join(data_path, "dem")


if not os.path.exists(dem_data_path):
    os.makedirs(dem_data_path)

dem_path = os.path.join(dem_data_path, "dem_30m.tif")
dem_clipped_path = dem_path.replace(".tif", "_clipped.tif")
dem_clipped_utm_path = dem_clipped_path.replace(".tif", "_utm10n.tif")
dem_clipped_utm_asc_path = dem_clipped_utm_path.replace(".tif", ".asc")

shape = gpd.read_file(os.path.join(data_path, "nooksack.geojson")).geometry.iloc[0]
elevation.clip(
	bounds=shape.bounds, 
	output=dem_path.replace(" ", "\ ")
)

with rasterio.open(dem_path) as src:
	out_image, out_transform = mask.mask(src, [shape], crop=True)
	out_meta = src.meta

out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

with rasterio.open(dem_clipped_path, "w", **out_meta) as dest:
    dest.write(out_image)

dem_clipped_path = dem_clipped_path.replace(" ", "\ ")
dem_clipped_utm_path = dem_clipped_utm_path.replace(" ", "\ ")
dem_clipped_utm_asc_path = dem_clipped_utm_asc_path.replace(" ", "\ ")

subprocess.run(
	f"gdalwarp -t_srs EPSG:32610 -r cubic {dem_clipped_path} {dem_clipped_utm_path}",
	shell=True
)

subprocess.run(
	f"gdal_translate -of AAIGrid -r cubic {dem_clipped_utm_path} {dem_clipped_utm_asc_path}",
	shell=True
)
