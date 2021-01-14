# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 21:01:38 2019

@author: josch
"""
import folium
import pandas as pd
from geopy.geocoders import Nominatim
import time
from selenium import webdriver
import re

#import os
#cwd = os.getcwd()
path="C:/Users/josch/Documents/Python Scripts/Sperrmuell21"

delay=1 # für den Browser

geolocator = Nominatim(user_agent="my-application")
ka = geolocator.geocode("Karlsruhe")
ka = [ka.latitude, ka.longitude]
#m = folium.Map(location=ka, tiles='OpenStreetMap', zoom_start=14)
#m.save(path+r'\Karlsruhe_map.html')


#############################
# Kalender einlesen aus Hauptdatei
#############################
liste=pd.read_csv(path+r"\Sperrmuellkalender.csv")
daten = liste["0"]
liste=liste.set_index("0")

monate = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    
monatsnamen = ['Januar','Februar','Maerz','April','Mai','Juni',
               'Juli','August','September','Oktober','November','Dezember']
#mytiles = ["Stamen Terrain" for i in range(12)]
mytiles = ["CartoDB positron", "Stamen Toner", "Stamen Watercolor", "Stamen Toner", 
           "Stamen Watercolor", "Stamen Terrain", "OpenStreetMap", "Stamen Watercolor", 
           "Stamen Terrain", "OpenStreetMap", "Stamen Toner", "CartoDB positron"]
    # tiles: OpenStreetMap, Stamen Terrain, Stamen Toner, Stamen Watercolor, 
    #"CartoDB" (positron and dark_matter), Mapbox Bright, Mapbox Control Room (nur best. Zoomlevel)


addr = geolocator.geocode("Uhlandstraße 14, Karlsruhe")
addr = [addr.latitude, addr.longitude]
home_marker = folium.Marker(addr, icon=folium.Icon(color="red", icon="home"))
try:
    browser = webdriver.Firefox()# benötigt geckodriver Datei im Python Verzeichnis (C:\Anaconda) (Bezeichnung PATH), außerdem Python und Visual C++ Redistributable
except WebDriverException:
    pass

counter=0

#i=monate[8]
# eine Karte pro Monat für die Printversion erstellen (als html und png)
for i in monate:

    m = folium.Map(location=ka, tiles=mytiles[counter], zoom_start=13)
    for j in liste.index: # schlimmste Schleife ever!!! bitte beheben! Inspiration siehe 2_...
        try:
            heute = liste.loc[re.search("\d\d."+i+".2021", j)[0], "Strasse"] # 
        except TypeError:
            pass #heute=""
        heute = heute.split(", ")[0] # pro Tag wird nur die erste Straße eingetragen (übersichtlicher)
        #test.append(heute)
        addr = geolocator.geocode(heute+", Karlsruhe")
        try:
            addr = [addr.latitude, addr.longitude]
            folium.Marker(addr, popup=heute, color="darkred").add_to(m)
        except AttributeError:
            print(heute)
    home_marker.add_to(m)
    fname = path+'/png_html/map_'+monatsnamen[counter]        
    m.save(fname+'.html')
    
    browser.get("file:///"+fname+".html")    
    #Give the map tiles some time to load
    time.sleep(delay)
    browser.save_screenshot(fname+".png")
    counter+=1
browser.quit()   


#     Beispiele:
#         https://python-visualization.github.io/folium/quickstart.html
# Als pdf/png
# https://github.com/python-visualization/folium/issues/35
# Marker: 
#     https://andrewchallis.co.uk/wp-content/uploads/2017/12/Folium.pdf
#     https://github.com/python-visualization/folium/issues/210
