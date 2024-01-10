# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import rasterio as rio
import pandas as pd
import seaborn as sans
import altair as alt

with rio.open("/Users/elischwat/Downloads/NLCD_2016_nooksack/NLCD_2016_Land_Cover_nooksack.asc") as src:
     arr = src.read()

# https://www.mrlc.gov/data/legends/national-land-cover-database-2016-nlcd2016-legend

names = {
    0: "Unclassified",
    11: "Open Water",
    12: "Perennial Ice/Snow",
    21: "Developed, Open",
    22: "Developed, Low Intensity",
    23: "Developed, Medium Intensity",
    24: "Developed, High Intensity",
    31: "Barren Land (Rock/Sand/Clay)",
    41: "Deciduous Forest",
    42: "Evergreen Forest",
    43: "Mixed Forest",
    52: "Shrub/Scrub",
    71: "Grassland/Herbaceous",
    81: "Pasture/Hay",
    82: "Cultivated Crops",
    90: "Woody Wetlands",
    95: "Emergent Herbaceous Wetlands",
}

# Filter out 0 (no category).

series = pd.Series(arr.flatten())
series = series[series != 0]
series.replace(names, inplace=True)
series = series.value_counts()

df = pd.DataFrame(series).reset_index().rename(
    {
        'index': 'Category',
        0: 'Frequency'
    },
    axis='columns'
)

alt.Chart(df).mark_bar().encode(
    x = alt.X('Category', axis=alt.Axis(labelAngle=30), sort='-y'),
    y = 'Frequency'
).properties(width=500)
