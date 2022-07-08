import geopandas as gpd
import pandas as pd
import numpy as np

# MODIFY THIS
gdb_path = "/Users/elischwat/Downloads/gSSURGO_WA/gSSURGO_WA.gdb"

component_table = gpd.read_file(gdb_path, layer='component')
param_table = gpd.read_file(gdb_path, layer='chorizon')

component_param_table = pd.merge(
    component_table[['mukey','cokey', 'majcompflag', 'comppct_r']],
    param_table[['cokey', 'hzdept_r', 'hzdepb_r', 'hzthk_r', 'ksat_r']],
    on='cokey'
)

# ## Drop soil layers with NaN ksat values, so we find the soil depth as the bottom of the observed deepest permeable layer

component_param_table = component_param_table[~component_param_table.ksat_r.isna()]

# ## Aggregate layers for each component, finding the maximum soil depth value

component_depth_table = component_param_table.groupby(
    ['mukey', 'cokey', 'comppct_r']
).agg(
    soil_depth = ("hzdepb_r", "max")
).reset_index()
component_depth_table

# ## Aggregate components for each map unit (mukey):
# For each mukey - find each component's deepest soil layer, weight average those depths by component percent}

mapunit_depth_table = component_depth_table.groupby(
    'mukey'
).agg(
    max_soil_depth=("soil_depth", 'mean') #or 'max', or 'min'
)

# ## Convert depth to integers - Changes of Accetable magnitude...right?

mapunit_depth_table.max_soil_depth = mapunit_depth_table.max_soil_depth.astype('int')
mapunit_depth_table

file = 'mukey_soildepth.csv'
print(f'Writing to {file}')

mapunit_depth_table.to_csv(file)
