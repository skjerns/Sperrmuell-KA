# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 21:01:38 2019

@author: josch
"""
import folium
from geopy.geocoders import Nominatim
import time
import json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os
path="C:/Users/joan9/Documents/Python Scripts/Sperrmuell/2025/"
os.chdir(path)

# Ä,Ö,Ü einsetzen
from commons import multiple_replace
#replacements = {"Ã„":"Ä", "Ãœ":"Ü", "Ã–":"Ö", "ã„":"ä", "ãœ":"ü", "ã–":"ö"} #"ã¼":"ü"}
#replacements = {v: k for k, v in replacements.items()} # Zuordnung umdrehen
replacements = {"ã„":"ä", "ãœ":"ü", "ã–":"ö", "ã¼":"ü", "ã¤":"ä", "ã¶":"ö"}

delay=1 # für den Browser

geolocator = Nominatim(user_agent="http")
ka = geolocator.geocode("Karlsruhe")
ka = [ka.latitude, ka.longitude]
#m = folium.Map(location=ka, tiles='OpenStreetMap', zoom_start=14)
#m.save(path+r'\Karlsruhe_map.html')

#############################
# Kalender einlesen aus Hauptdatei
#############################
with open('sperrmuellkalender.json', 'r') as f:
    liste = json.load(f)
with open('street_coords.json', 'r') as f:
    street_coords = json.load(f)
street_coords = {multiple_replace(replacements, k.lower()): v for k, v in street_coords.items()} #Kleinschreibung der keys, weil die Straßennamen im Kalender selten komplett großgeschrieben sind.

monate = ["01","02","03","04","05","06","07","08","09","10","11","12"]

monatsnamen = ['Januar','Februar','Maerz','April','Mai','Juni',
               'Juli','August','September','Oktober','November','Dezember']
mytiles = ["CyclOSM"]*12
#mytiles = ["Stamen Terrain" for i in range(12)]
# mytiles = ["CyclOSM", "CartoDB positron", "OPNVKarte", "OpenStreetMap",
#            "CyclOSM", "CartoDB positron", "OPNVKarte", "OpenStreetMap",
#            "CyclOSM", "CartoDB positron", "OPNVKarte", "OpenStreetMap"]
# alte tiles funktionieren teilweise nicht mehr.
# mytiles = ["CartoDB positron", "Stamen Toner", "Stamen Watercolor", "Stamen Toner",
           # "Stamen Watercolor", "Stamen Terrain", "OpenStreetMap", "Stamen Watercolor",
           # "Stamen Terrain", "OpenStreetMap", "Stamen Toner", "CartoDB positron"]
    # tiles: OpenStreetMap, Stamen Terrain, Stamen Toner, Stamen Watercolor,
    #"CartoDB" (positron and dark_matter), Mapbox Bright, Mapbox Control Room (nur best. Zoomlevel)

karlsruhe_long_lat = [8.4034195, 49.0068705][::-1]

# addr = geolocator.geocode({'street':'...', 'city':'Karlsruhe'})
# addr = [addr.latitude, addr.longitude]
# home_marker = folium.Marker(addr, icon=folium.Icon(color="red", icon="home"))

# eine Straße pro Tag in dict schreiben für Monatsübersicht, Monate als keys
streets = {}
for date in list(liste):
    month = date[3:5]
    #year = date[-4:]
    try:
        streets[month] += [liste[date][0]]
    except KeyError:
        streets[month] = [liste[date][0]]

# benötigt Firefox im System
browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install())) 



#i=0
# eine Karte pro Monat für die Printversion erstellen (als html und png)
for i in range(12):

    m = folium.Map(location=karlsruhe_long_lat, tiles=mytiles[i], zoom_start=13)
    # Einen Marker pro Tag hinzufügen
    for j in streets[monate[i]]:
        j = multiple_replace(replacements, j.lower()) # weil alle Keys von street_coords klein
        addr = street_coords[j]
        try:
            addr = addr[::-1]
        except TypeError: # Straßennamen mit "Gewann" geben None
                addr=[0,0]
        
        # Marker-Optik
        icon_params = folium.Icon(icon='recycle', prefix='fa', color='#FF1111',icon_color='#FFFF00')
        folium.Marker(addr, icon=icon_params).add_to(m)

    fname = path+'png_html/map_'+monate[i]+'_'+monatsnamen[i]
    m.save(fname+'.html')

    browser.get("file:///"+fname+".html")
    #Give the map tiles some time to load
    time.sleep(delay)
    browser.save_screenshot(fname+".png")
browser.quit()
