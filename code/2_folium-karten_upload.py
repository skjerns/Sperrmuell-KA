# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 21:01:38 2019

@author: josch
"""
import folium
import pandas as pd
from geopy.geocoders import Nominatim
import time
import re


#import os
#cwd = os.getcwd()
path="C:/Users/josch/Documents/Python Scripts/Sperrmuell21"
path_db="C:/Users/josch/Dropbox/Kalender"

delay=1 # für den Browser

geolocator = Nominatim(user_agent="my-app")
ka = geolocator.geocode("Karlsruhe")
ka = [ka.latitude, ka.longitude]
#m = folium.Map(location=ka, tiles='OpenStreetMap', zoom_start=14)
#m.save(path+r'\Karlsruhe_map.html')

#############################
# Kalender einlesen aus Hauptdatei
#############################
liste=pd.read_csv(path+r"/Sperrmuellkalender.csv")
liste=liste.set_index("0")

monate = ["01","02","03","04","05","06","07","08","09","10","11","12"] 
 

monatsnamen = ['Januar','Februar','März','April','Mai','Juni',
               'Juli','August','September','Oktober','November','Dezember']


addr = geolocator.geocode("Uhlandstraße 14, Karlsruhe")
addr = [addr.latitude, addr.longitude]
home_marker = folium.Marker(addr, icon=folium.Icon(color="red", icon="home"))
#browser = webdriver.Firefox()# benötigt geckodriver Datei im Python Verzeichnis (C:\Anaconda) (Bezeichnung PATH), außerdem Python und Visual C++ Redistributable



for j in liste.index:
    monat_z = j.split(".")[1]
    monat_n = monatsnamen[int(monat_z)-1]
    m = folium.Map(location=ka, tiles="OpenStreetMap", zoom_start=12.5)
    home_marker.add_to(m)
    #heute = liste.loc[re.search("\d\d."+i+".2021", j)[0], "Strasse"]
    heute = liste.loc[j, "Strasse"]
    heute = heute.split(", ")
        # diser Teil dauert sehr lange (bildet alle Straßen ab)    
    for k in range(len(heute)):
        #folium.Marker([data.iloc[i]['lon'], data.iloc[i]['lat']], popup=data.iloc[i]['name']).add_to(m)
        try:
            addr = geolocator.geocode(heute[k]+", Karlsruhe")
        except:
            pass
        try:
            addr = [addr.latitude, addr.longitude]
            folium.Marker(addr, popup=heute[k]).add_to(m)
        except AttributeError:
            print(heute[k])
    fname = path_db+"/"+monat_z+"_"+monat_n+'/map_'+j.replace(".","_")        
    m.save(fname+'.html')


    
    
    
#     Beispiele:
#         https://python-visualization.github.io/folium/quickstart.html
# Als pdf/png
# https://github.com/python-visualization/folium/issues/35
# Marker: 
#     https://andrewchallis.co.uk/wp-content/uploads/2017/12/Folium.pdf
#     https://github.com/python-visualization/folium/issues/210
