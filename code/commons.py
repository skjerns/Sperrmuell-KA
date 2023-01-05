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
    street = street.upper()
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
    
def multiple_replace(dict, text):
  # Create a regular expression  from the dictionary keys
  #https://stackoverflow.com/questions/15175142/how-can-i-do-multiple-substitutions-using-regex  
  regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
  # For each match, look-up corresponding value in dictionary
  return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 