"""
Created on Sun Aug 18 21:01:38 2019
@author: josch
"""
import os
import folium
import pandas as pd
from geopy.geocoders import Nominatim
import json
import re
import time
from tqdm import tqdm
from joblib.memory import Memory
from commons import get_street_coords
mem = Memory('.')


if __name__=='__main__':
    delay=1 # für den Browser

    geolocator = Nominatim(user_agent="my-app")
    karlsruhe_long_lat = [8.4034195, 49.0068705][::-1]
    #m = folium.Map(location=ka, tiles='OpenStreetMap', zoom_start=14)
    #m.save(path+r'\Karlsruhe_map.html')

    #############################
    # Kalender einlesen aus Hauptdatei
    #############################
    with open('sperrmuellkalender.json', 'r') as f:
        liste = json.load(f)


    monatsnamen = ['Januar','Februar','März','April','Mai','Juni',
                   'Juli','August','September','Oktober','November','Dezember']

    for date in tqdm(list(liste)):
        month = date[3:5]
        print(month)
        year = date[-4:]
        m = folium.Map(location=karlsruhe_long_lat, tiles="OpenStreetMap", zoom_start=12.5)
        streets = [x.replace('ß', 'SS') for x in liste[date]]

        for street in streets:
            loc = get_street_coords(street)
            if loc is None:
                continue
            folium.Marker(loc[::-1], popup=street, tooltip=street).add_to(m)

        html_file = f'../{year}_{month}_{monatsnamen[int(month)-1]}/map_{date.replace(".","_")}.html'
        os.makedirs(os.path.dirname(html_file), exist_ok=True)
        m.save(html_file)





#     Beispiele:
#         https://python-visualization.github.io/folium/quickstart.html
# Als pdf/png
# https://github.com/python-visualization/folium/issues/35
# Marker:
#     https://andrewchallis.co.uk/wp-content/uploads/2017/12/Folium.pdf
#     https://github.com/python-visualization/folium/issues/210
