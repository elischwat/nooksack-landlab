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
component_param_table['thickness'] = component_param_table['hzdepb_r'] - component_param_table['hzdept_r']

# ## Aggregate layers for each component, finding the maximum ksat value

component_ksat_table = component_param_table.groupby(
    ['mukey', 'cokey', 'comppct_r']
).agg(
    ksat_component_max=("ksat_r", 'max')
).reset_index()
component_ksat_table

# ### Drop components with NaN ksat values
#
# This makes sure we end up with as much data as possible. If we do not remove components with NaN, those NaNs propagate into the mukey, leaving no ksat value for the associated mapunit.

component_ksat_table = component_ksat_table.dropna()
component_ksat_table

# ## Aggregate components for each map unit (mukey), weight-averaging by component percent

# +
wm = lambda x: np.average(x, weights= component_ksat_table.loc[x.index, "comppct_r"])

mapunit_ksat_table = component_ksat_table.groupby(
    ['mukey']
).agg(
    ksat_weighted_mean=("ksat_component_max", wm)
).reset_index()
# -

mapunit_ksat_table = mapunit_ksat_table.dropna()

mapunit_ksat_table

file = 'mukey_ksat.csv'
print(f'Writing to {file}')

mapunit_ksat_table.to_csv(file)


