# -*- coding: utf-8 -*-
"""IPRO Maps.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NWLV4Lqu05-gGg2AR9ZApiqJEyQamhND

# TIF Demographics Team

## Packages
"""

# Import packages
import numpy as np
import pandas as pd
import geopandas as gpd
import statsmodels.api as sm

# import mapping packages
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# import google drive folder
from google.colab import drive
drive.mount('/content/drive')

"""## Loading Data"""

#read census income data by census tract
censusIncome = gpd.read_file('/content/drive/My Drive/480-497-Demographic TIF Team/Demographic/Census/censusIncomeFinalcopy.csv')

# read intersecting boundaries of tracts and tifs
censusTIF = gpd.read_file('/content/drive/My Drive/480-497-Demographic TIF Team/Demographic/Census/intersecting_geojson_file_2.geojson')

#censusTIF = gpd.read_file("/content/drive/My Drive/480-497-Demographic TIF Team/Demographic/Census/CensusTractsByTIF.csv")

# read demogrpahic data by census tract
censusDemo = gpd.read_file("/content/drive/My Drive/480-497-Demographic TIF Team/Demographic/ct22_data_01.csv")

# read tif data from Civic Lab
tifLab = gpd.read_file("/content/drive/My Drive/480-497-Demographic TIF Team/Demographic/2022_out.csv")

"""## Merging Data"""

censusIncome.sample(2)

censusDemo.sample(2)

censusIncome.drop(columns=['geometry'], inplace=True)
censusDemo.drop(columns=['geometry'], inplace=True)

# Merge the two census DataFrames on the common column
census_tract = pd.merge(censusIncome, censusDemo, left_on='name10_x', right_on='Census Tract', how='left')

census_tract.sample(2)

census_tract.dtypes

census_tract.drop(columns=['name10_x', 'commarea_n_x'], inplace=True)

# Save census_tract as a csv to my computer
census_tract.to_csv('census_tract.csv', index=False)

census_tract.sample(1)

censusTIF.sample(1)

filtered_rows = censusTIF[censusTIF['name10'] == 620]

print(filtered_rows)

censusTIF.drop(columns=['Median_Household_Income','statefp10','commarea_n','notes','countyfp10'], inplace=True)

new_census_tract = pd.merge(census_tract, censusTIF, on='namelsad10', how='left')

new_census_tract.sample(5)

# Save census_tract as a csv to my computer
new_census_tract.to_csv('census_tract_new.csv', index=False)

new_census_tract.dtypes

new_census_tract.drop(columns=['geoid10','commarea'], inplace=True)

"""This dataframe conssits of every census tract with demographic information along with what TIF district it may overlap with."""

new_census_tract

# Pull census tracts that are inside a TIF
census_in_TIF = new_census_tract[new_census_tract['TIF-bound'].notna()]

# This dataset contains all Census Tracts within a TIF district along with meaningful demographic information
census_in_TIF.sample(5)

"""Now I will merge the census_in_TIF with the civic lab TIF district data"""

tifLab.sample(1)

unique_values = tifLab["tif_number"].unique()
unique_values

tifLab.drop(columns=['geometry'], inplace=True)

census_tif_merge = pd.merge(census_in_TIF, tifLab, left_on='TIF-bound', right_on='tif_name' , how='left')

census_tif_merge.sample(1)

filtered_rows = census_tif_merge[census_tif_merge['name10'] == 8432]

print(filtered_rows["TIF-bound"])

# Save census_tract as a csv to my computer
census_tif_merge.to_csv('census_tif_merge.csv', index=False)

"""This dataframe consists of every census tract that overlaps with a TIF District. This also contans all demographic data within each tract and TIF along with its geometry."""

census_tif_merge

"""## Mapping"""

# Read the DataFrame into a GeoDataFrame
gdf = gpd.GeoDataFrame(census_tif_merge, geometry='geometry')

# Plot the GeoDataFrame
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
gdf.plot(column='Median value (dollars)', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.3')

# Add a legend
vmin, vmax = census_tif_merge['Median value (dollars)'].min(), census_tif_merge['Median value (dollars)'].max()
sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=vmin, vmax=1000000))
sm._A = []  # fake up the array of the scalar mappable
cbar = plt.colorbar(sm)
cbar.set_label('Median Property Value ($)')

# Set plot title
plt.title('Median Property Value ($)')

# Show the plot
plt.show()

# Plot the GeoDataFrame
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
gdf.plot(column='Median real estate taxes', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.3')

# Add a legend
vmin, vmax = census_tif_merge['Median real estate taxes'].min(), census_tif_merge['Median real estate taxes'].max()
sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=vmin, vmax=8000))
sm._A = []  # fake up the array of the scalar mappable
cbar = plt.colorbar(sm)
cbar.set_label('Median Real Estate Taxes')

# Set plot title
plt.title('Median Real Estate Taxes')

# Show the plot
plt.show()

# Plot the GeoDataFrame
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
gdf.plot(column='Hispanic or Latin Pop. Est.', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.3')

# Add a legend
vmin, vmax = census_tif_merge['Hispanic or Latin Pop. Est.'].min(), census_tif_merge['Hispanic or Latin Pop. Est.'].max()
sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=vmin, vmax=6000))
sm._A = []  # fake up the array of the scalar mappable
cbar = plt.colorbar(sm)
cbar.set_label('Hispanic or Latin Pop. Est.')

# Set plot title
plt.title('Hispanic or Latin Population Estimate')

# Show the plot
plt.show()

# Plot the GeoDataFrame
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
gdf.plot(column='White (Not Hispanic or Latin) Pop. Est.', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.3')

# Add a legend
vmin, vmax = census_tif_merge['White (Not Hispanic or Latin) Pop. Est.'].min(), census_tif_merge['White (Not Hispanic or Latin) Pop. Est.'].max()
sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=vmin, vmax=6000))
sm._A = []  # fake up the array of the scalar mappable
cbar = plt.colorbar(sm)
cbar.set_label('White Pop. Est.')

# Set plot title
plt.title('White Population Estimate')

# Show the plot
plt.show()

# Plot the GeoDataFrame
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
gdf.plot(column='Black or African American Pop. Est.', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.3')

# Add a legend
vmin, vmax = census_tif_merge['Black or African American Pop. Est.'].min(), census_tif_merge['Black or African American Pop. Est.'].max()
sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=vmin, vmax=6000))
sm._A = []  # fake up the array of the scalar mappable
cbar = plt.colorbar(sm)
cbar.set_label('Black Pop. Est.')

# Set plot title
plt.title('Black Population Estimate')

# Show the plot
plt.show()

"""## Creating TIF Dataframe

Take what demographic group is in a majority in each census tract, calculate for each TIF district, and merge with Civic Lab TIF data.
"""

census_tif_merge.dtypes

# First, make sure the relevant columns are numeric
numeric_columns = ["Hispanic or Latin Pop. Est.","White (Not Hispanic or Latin) Pop. Est.","Black or African American Pop. Est.","Asian Pop. Est.","Total Pop. Est."]

census_tif_merge[numeric_columns] = census_tif_merge[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Now, handle NaN values by replacing them with zeros or another appropriate value
census_tif_merge[numeric_columns] = census_tif_merge[numeric_columns].fillna(0)

numeric_columns = ["Hispanic or Latin Pop. Est.","White (Not Hispanic or Latin) Pop. Est.","Black or African American Pop. Est.","Asian Pop. Est."]

census_tif_merge2 = census_tif_merge

# Calculate the majority demographic group using the idxmax() function along the appropriate columns
census_tif_merge2['majority_group'] = census_tif_merge2[numeric_columns].idxmax(axis=1)

census_tif_merge2.sample(5)

# Calculate demographic population estimates for each race in each census tract
census_tif_merge2['Hispanic Demographic Population'] = census_tif_merge2['Hispanic or Latin Pop. Est.'] * census_tif_merge['intersection_ratio']
census_tif_merge2['White Demographic Population'] = census_tif_merge2['White (Not Hispanic or Latin) Pop. Est.'] * census_tif_merge['intersection_ratio']
census_tif_merge2['Black Demographic Population'] = census_tif_merge2['Black or African American Pop. Est.'] * census_tif_merge['intersection_ratio']
census_tif_merge2['Asian Demographic Population'] = census_tif_merge2['Asian Pop. Est.'] * census_tif_merge['intersection_ratio']
census_tif_merge2['Total Population'] = census_tif_merge2['Total Pop. Est.'] * census_tif_merge['intersection_ratio']

# Group by district and sum the demographic population estimates for each race
TIF_population = census_tif_merge2.groupby('TIF-bound').agg({
    'Hispanic Demographic Population': 'sum',
    'White Demographic Population': 'sum',
    'Black Demographic Population': 'sum',
    'Asian Demographic Population': 'sum',
    'Total Population': 'sum'
}).reset_index()

TIF_population.sample(4)

# Calculate the majority demographic group using the idxmax() function along the appropriate columns
TIF_population['Majority Demographic'] = TIF_population[['Hispanic Demographic Population','White Demographic Population','Black Demographic Population','Asian Demographic Population']].idxmax(axis=1)

TIF_population.sample(5)

TIF_population

# Save TIF_population as a csv to my computer
TIF_population.to_csv('TIF_population.csv', index=False)

# Merge the two census DataFrames on the common column
full_tif = pd.merge(TIF_population, tifLab, left_on='TIF-bound', right_on='tif_name', how='left')

full_tif

# Pull TIFs that are merged with demographics for 2022
full_tif_2022 = full_tif[full_tif['tif_name'].notna()]

full_tif_2022

full_tif_2022.to_csv('full_tif_2022.csv', index = False)

"""## Interactive Maps

"""

import json
import geopandas as gpd
from shapely import wkt
from branca.colormap import linear
from branca.colormap import LinearColormap
import folium
from folium import Choropleth, Popup
from branca.colormap import StepColormap

with open('/content/drive/My Drive/480-497-Demographic TIF Team/Demographic/interactive_maps_census_tif_merge.geojson') as f:
    census_merge_txt = f.read()

census_tif_merge_geojson = json.loads(census_merge_txt)

filter_census_tif_merge = census_tif_merge.dropna(subset=["Median value (dollars)"])
filter_census_tif_merge["Median value (dollars)"] = pd.to_numeric(filter_census_tif_merge["Median value (dollars)"], errors='coerce')

min_income = filter_census_tif_merge["Median value (dollars)"].min()
max_income = filter_census_tif_merge["Median value (dollars)"].max()
sorted_thresholds = sorted(filter_census_tif_merge["Median value (dollars)"].dropna().unique())
colormap = linear.RdYlGn_11.scale(min_income, max_income)
colormap = colormap.to_step(index=sorted_thresholds)

print("Max:"+str(max_income))
print("Min:"+str(min_income))

filter_census_tif_merge_unique = filter_census_tif_merge.drop_duplicates(subset="name10")
pop_dict = filter_census_tif_merge_unique.set_index("name10")["Median value (dollars)"].to_dict()


m = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

def highlight_function(feature):
    return {
        "fillColor": "#BEFFF7",
        "color": "black",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.4,
    }

popup = folium.GeoJsonPopup(fields=["tif_name", "Census Tract", "Median value (dollars)"])

folium.GeoJson(
    census_tif_merge_geojson,
    style_function=lambda feature: {
        "fillColor": colormap(pop_dict[feature["properties"]["name10"]]) if feature["properties"]["name10"] in pop_dict else 'gray',
        "color": "#A8A196",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.9,
    },
    highlight_function=highlight_function,
    popup=popup
).add_to(m)

colormap.caption = "Median Value Color Scale"
colormap.add_to(m)

m

filter_census_tif_merge = census_tif_merge.dropna(subset=["Median real estate taxes"])
filter_census_tif_merge["Median real estate taxes"] = pd.to_numeric(filter_census_tif_merge["Median real estate taxes"], errors='coerce')

min_income = filter_census_tif_merge["Median real estate taxes"].min()
max_income = filter_census_tif_merge["Median real estate taxes"].max()
sorted_thresholds = sorted(filter_census_tif_merge["Median real estate taxes"].dropna().unique())
colormap = linear.RdYlGn_11.scale(min_income, max_income)
colormap = colormap.to_step(index=sorted_thresholds)

print("Max:"+str(max_income))
print("Min:"+str(min_income))

filter_census_tif_merge_unique = filter_census_tif_merge.drop_duplicates(subset="name10")
pop_dict = filter_census_tif_merge_unique.set_index("name10")["Median real estate taxes"].to_dict()

m = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

def highlight_function(feature):
    return {
        "fillColor": "#BEFFF7",
        "color": "black",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.4,
    }

popup = folium.GeoJsonPopup(fields=["tif_name","Census Tract","Median real estate taxes"])
folium.GeoJson(
    census_tif_merge_geojson,
    style_function=lambda feature: {
        "fillColor": colormap(pop_dict[feature["properties"]["name10"]]) if feature["properties"]["name10"] in pop_dict else 'gray',
        "color": "#A8A196",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.9,
    },
    highlight_function=highlight_function,
    popup=popup
).add_to(m)

colormap.caption = "Median Real Estate Taxes Color Scale"
colormap.add_to(m)

m

filter_census_tif_merge = census_tif_merge.dropna(subset=["Hispanic or Latin Pop. Est."])
filter_census_tif_merge["Hispanic or Latin Pop. Est."] = pd.to_numeric(filter_census_tif_merge["Hispanic or Latin Pop. Est."], errors='coerce')

min_income = filter_census_tif_merge["Hispanic or Latin Pop. Est."].min()
max_income = filter_census_tif_merge["Hispanic or Latin Pop. Est."].max()
sorted_thresholds = sorted(filter_census_tif_merge["Hispanic or Latin Pop. Est."].dropna().unique())
colormap = linear.RdYlGn_11.scale(min_income, max_income)
colormap = colormap.to_step(index=sorted_thresholds)

print("Max:"+str(max_income))
print("Min:"+str(min_income))

filter_census_tif_merge_unique = filter_census_tif_merge.drop_duplicates(subset="name10")
pop_dict = filter_census_tif_merge_unique.set_index("name10")["Hispanic or Latin Pop. Est."].to_dict()

m = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

def highlight_function(feature):
    return {
        "fillColor": "#BEFFF7",
        "color": "black",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.4,
    }

popup = folium.GeoJsonPopup(fields=["tif_name","Census Tract","Hispanic or Latin Pop. Est."])

folium.GeoJson(
    census_tif_merge_geojson,
    style_function=lambda feature: {
        "fillColor": colormap(pop_dict[feature["properties"]["name10"]]) if feature["properties"]["name10"] in pop_dict else 'gray',
        "color": "#A8A196",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.9,
    },
    highlight_function=highlight_function,
    popup=popup
).add_to(m)

colormap.caption = "Hispanic Population Estimate Color Scale"
colormap.add_to(m)
m

filter_census_tif_merge = census_tif_merge.dropna(subset=["White (Not Hispanic or Latin) Pop. Est."])
filter_census_tif_merge["White (Not Hispanic or Latin) Pop. Est."] = pd.to_numeric(filter_census_tif_merge["White (Not Hispanic or Latin) Pop. Est."], errors='coerce')

min_income = filter_census_tif_merge["White (Not Hispanic or Latin) Pop. Est."].min()
max_income = filter_census_tif_merge["White (Not Hispanic or Latin) Pop. Est."].max()
sorted_thresholds = sorted(filter_census_tif_merge["White (Not Hispanic or Latin) Pop. Est."].dropna().unique())
colormap = linear.RdYlGn_11.scale(min_income, max_income)
colormap = colormap.to_step(index=sorted_thresholds)

print("Max:"+str(max_income))
print("Min:"+str(min_income))

filter_census_tif_merge_unique = filter_census_tif_merge.drop_duplicates(subset="name10")
pop_dict = filter_census_tif_merge_unique.set_index("name10")["White (Not Hispanic or Latin) Pop. Est."].to_dict()

m = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

def highlight_function(feature):
    return {
        "fillColor": "#BEFFF7",
        "color": "black",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.4,
    }

popup = folium.GeoJsonPopup(fields=["tif_name","Census Tract","White (Not Hispanic or Latin) Pop. Est."])

folium.GeoJson(
    census_tif_merge_geojson,
    style_function=lambda feature: {
        "fillColor": colormap(pop_dict[feature["properties"]["name10"]]) if feature["properties"]["name10"] in pop_dict else 'gray',
        "color": "#A8A196",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.9,
    },
    highlight_function=highlight_function,
    popup=popup
).add_to(m)

colormap.caption = "White Population Estimate Color Scale"
colormap.add_to(m)
m

filter_census_tif_merge = census_tif_merge.dropna(subset=["Black or African American Pop. Est."])
filter_census_tif_merge["Black or African American Pop. Est."] = pd.to_numeric(filter_census_tif_merge["Black or African American Pop. Est."], errors='coerce')

min_income = filter_census_tif_merge["Black or African American Pop. Est."].min()
max_income = filter_census_tif_merge["Black or African American Pop. Est."].max()
sorted_thresholds = sorted(filter_census_tif_merge["Black or African American Pop. Est."].dropna().unique())
colormap = linear.RdYlGn_11.scale(min_income, max_income)
colormap = colormap.to_step(index=sorted_thresholds)

print("Max:"+str(max_income))
print("Min:"+str(min_income))

filter_census_tif_merge_unique = filter_census_tif_merge.drop_duplicates(subset="name10")
pop_dict = filter_census_tif_merge_unique.set_index("name10")["Black or African American Pop. Est."].to_dict()

m = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

def highlight_function(feature):
    return {
        "fillColor": "#BEFFF7",
        "color": "black",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.4,
    }

popup = folium.GeoJsonPopup(fields=["tif_name","Census Tract","Black or African American Pop. Est."])

folium.GeoJson(
    census_tif_merge_geojson,
    style_function=lambda feature: {
        "fillColor": colormap(pop_dict[feature["properties"]["name10"]]) if feature["properties"]["name10"] in pop_dict else 'gray',
        "color": "#A8A196",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.9,
    },
    highlight_function=highlight_function,
    popup=popup
).add_to(m)

colormap.caption = "Black/African American Population Estimate Color Scale"
colormap.add_to(m)
m

filter_census_tif_merge = census_tif_merge.dropna(subset=["cumulative_property_tax_extraction"])
filter_census_tif_merge["cumulative_property_tax_extraction"] = pd.to_numeric(filter_census_tif_merge["cumulative_property_tax_extraction"], errors='coerce')

min_income = filter_census_tif_merge["cumulative_property_tax_extraction"].min()
max_income = filter_census_tif_merge["cumulative_property_tax_extraction"].max()
sorted_thresholds = sorted(filter_census_tif_merge["cumulative_property_tax_extraction"].dropna().unique())
colormap = linear.RdYlGn_11.scale(min_income, max_income)
colormap = colormap.to_step(index=sorted_thresholds)

print("Max:"+str(max_income))
print("Min:"+str(min_income))

filter_census_tif_merge_unique = filter_census_tif_merge.drop_duplicates(subset="name10")
pop_dict = filter_census_tif_merge_unique.set_index("name10")["cumulative_property_tax_extraction"].to_dict()

m = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

def highlight_function(feature):
    return {
        "fillColor": "#BEFFF7",
        "color": "black",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.4,
    }

popup = folium.GeoJsonPopup(fields=["tif_name","Census Tract","cumulative_property_tax_extraction"])

folium.GeoJson(
    census_tif_merge_geojson,
    style_function=lambda feature: {
        "fillColor": colormap(pop_dict[feature["properties"]["name10"]]) if feature["properties"]["name10"] in pop_dict else 'gray',
        "color": "#A8A196",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.9,
    },
    highlight_function=highlight_function,
    popup=popup
).add_to(m)

colormap.caption = "Cumulative Property Tax Distribution Color Scale"
colormap.add_to(m)
m