"""
Created on Sun jan 11 21:01:38 2022
@author: skjerns
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
mem = Memory('.')

@mem.cache
def get_street_coords(street):
    max(tqdm._instances).set_description(f'getting coords for {street}')
    streets_json = 'street_coords.json'
    coords = {}
    if os.path.isfile(streets_json):
        with open(streets_json, 'r') as f:
            coords = json.load(f)
            
    if street in coords: 
        return coords[street]
    
    geolocator = Nominatim(user_agent=f"sperrmuell_ka_{street}")
    loc = geolocator.geocode({'street':street, 'city': 'Karlsruhe', 'country':'Germany'})
    if loc is not None:
        coords[street] = [loc.longitude, loc.latitude]
    else:
        coords[street] = loc
    with open(streets_json, 'w') as f:
        json.dump(coords, f, indent=4, ensure_ascii=False)
    time.sleep(0.5)
    return coords[street]