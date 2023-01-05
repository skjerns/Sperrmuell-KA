# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 15:51:19 2022

@author: Simon
"""
import os
import time
import folium
import pandas as pd
from geopy.geocoders import Nominatim
from geojson import Point, Feature, FeatureCollection, Polygon
import json
from tqdm import tqdm
from folium.plugins import TimeSliderChoropleth
import geopandas as gpd
import numpy as np
from datetime import datetime 
from joblib.memory import Memory
from commons import get_street_coords

#countries = gpd.read_file('C:/Users/Simon/Desktop/sampledata/99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp')
mem = Memory('.')

def circle(x, y, r=0.001):
    polygons = []
    for i in range(32):
        x_t = x + np.sin(i/5)*r
        y_t = y + np.cos(i/5)*r
        polygons.append([x_t, y_t])
    return polygons

if __name__ == '__main__':
    html_file = '../interactive_map.html'    
    
    delay=1 # für den Browser
    
    karlsruhe_long_lat = [8.4034195, 49.0068705]
    
    #############################
    # Kalender einlesen aus Hauptdatei
    #############################
    with open('sperrmuellkalender.json', 'r') as f:
        liste = json.load(f)
        
    m = folium.Map(location=karlsruhe_long_lat[::-1], tiles="OpenStreetMap", zoom_start=12.5)
    
    streets = [a.replace('ß', 'SS') for tup in liste.values() for a in tup]
    features = []
    for i, street in tqdm(list(enumerate(streets))):
        loc = get_street_coords(street)
        if loc is None: continue
        long, lat = loc
        geometry = Polygon([circle(long, lat)], popup=street,
                           tooltip='Vehicle_1',
                           color='blue',
                           weight=10)
        feat = Feature(id=street, geometry=geometry, 
                       properties={})
        features.append(feat)
    
    data = FeatureCollection(features)

    dates = [datetime.strptime(date, '%d.%m.%Y') for date in  list(liste.keys())]
    datetime_index = pd.to_datetime(dates)
    dt_index_epochs = datetime_index.astype(int) // 10 ** 9
    dt_index = dt_index_epochs.astype("U10")
        
    styledata = {}
    for street in streets:
        df = pd.DataFrame(
            {
                "color": 0,
                "opacity": 0,
            },
            index=dt_index,
        )
        df = df.cumsum()
        styledata[street] = df
        
    styledict = {
        str(street): data.to_dict(orient="index") for street, data in styledata.items()
    }
    
    all_dates = dt_index.to_list()
    for date, active_streets in zip(dates, liste.values()):
        date_ns = pd.to_datetime(date, unit='ns').value//10**9
        for street in active_streets:
            street = street.replace('ß', 'SS')
            idx_date = all_dates.index(str(date_ns))
            for i, poss_date in enumerate(list(styledict[street].keys())):
                if i==idx_date:
                    styledict[street][str(date_ns)]['color']='#8B0000'
                    styledict[street][str(date_ns)]['opacity']=0.7
                # elif not abs(i-idx_date)<5:
                #     del styledict[street][poss_date]
        
    # folium.GeoJson(data=data, style_function=lambda x:{'color':'#8B0000'}).add_to(m)
    
        
    g = TimeSliderChoropleth(
        name='Sperrmüllkarte Karlsruhe 2023',
        data=data,
        styledict=styledict,
    ).add_to(m)

    # folium.Popup({'name'}).add_to(g)
    
    # g
    m.save(html_file)
    

with open(html_file, 'r') as f:
    html = f.read()

html = html.replace('<div class="folium-map"', 
                    '''<b>Sperrmüllkarte Karlsruhe 2023</b><br>
                    Verschiebe den Regler auf das gewünschte Datum. Sperrmüllregion wird rot eingezeichnet
                    
                    <div class="folium-map"''')
with open(html_file, 'w') as f:
    f.write(html)
