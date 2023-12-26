import pandas as pd
import geopandas as gpd
import numpy as np
from pygris import tracts

#Fetch Census Tract Data using pygris
tract_list = []

states = pd.read_csv('https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv')
for abbreviation in states['Abbreviation']:
    print(abbreviation)
    state_tracts = tracts(year=2010, cb=True, cache=True, state=abbreviation)
    tract_list.append(state_tracts)

#geoDataFrame of all tracts
all_tracts = pd.concat(tract_list)

#change all_tracts crs to epsg=3857 -- this doesn't work for some reason 
# all_tracts = all_tracts.to_crs(epsg=3857)

#take string of GEO_ID following US and convert to int for merging
all_tracts['TractFIPS'] = all_tracts['GEO_ID'].str[9:].astype(np.int64)

#Read file with census tract ruggedness ratings
tract_ratings = pd.read_excel('RuggednessScale2010tracts.xlsx') 

#Merge tract info with ratings
merged_data = all_tracts.merge(tract_ratings, on='TractFIPS', how='inner')

# Filter columns 
filtered_data = merged_data[['TractName', 'CountyName','State', 'Population', 'RRS', 'RRSDescription', 'geometry']] 

#Export to GeoJSON
filtered_data.to_file('tract_ratings.geojson', driver='GeoJSON')

