# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 21:15:20 2019

@author: josch
"""
import json
from PIL import Image
from PIL import ImageDraw, ImageFont
# import qrcode # den lassen wir ab 2022 weg.
import calendar
import pandas as pd
import re
import os
import textwrap
path="C:/Users/josch/Documents/Python Scripts/Sperrmuell/2022/"
os.chdir(path)
from commons import multiple_replace
path_maps = path + "png_html/"
path_out = path + "output_print/"

jahr = 2022

# Daten, an denen Sperrmüll stattfindet
with open('sperrmuellkalender.json', 'r') as f:
    liste = json.load(f)

months = {}
for date in list(liste):
    month = date[3:5]
    #year = date[-4:]
    try: 
        months[month] += [date]
    except KeyError:
        months[month] = [date]

fancy_fonts = ["Bemydor","Autumn Moon - TTF","Alyfe Demo",
               "StripesCaps","Today__","Malache Crunch",
               "CoventryGardenNF","BigLou","UndergroundNF",
               "ExtraOrnamentalNo2","Beyond Wonderland","Mugnuts"]#,"nauvo__",

fancy_fonts_mono = "IckyTicketMono,Kingthings Trypewriter 2,Vanthian Ragnarok,Beccaria,Harting Plain,software_tester,Kingthings Trypewriter 2,Harting Plain,IckyTicketMono,Kingthings Trypewriter 2,Vanthian Ragnarok,Beccaria".split(",")
#fancy_fonts_mono = "IckyTicketMono,Kingthings Trypewriter 2,Vanthian Ragnarok,Beccaria,Harting Plain,EXITFONTFORAFILM,software_tester,hydrogen,Harting Plain,IckyTicketMono,Kingthings Trypewriter 2,EXITFONTFORAFILM".split(",")
monatsnamen = ['Januar','Februar','Maerz','April','Mai','Juni',
               'Juli','August','September','Oktober','November','Dezember']
monate = ["01","02","03","04","05","06","07","08","09","10","11","12"]
fcol = (0, 0, 180) # Schriftfarbe

#Kalendersprüche für die Ecke unten rechts (QR Code im vorherigen Design)
with open('Kalenderspruch.txt', 'r') as f:
    sprueche = f.read().splitlines() # besser als readlines, weil hier kein \n bleibt.
replacements = {"Ã¼":"ü", "Ã¶":"ö", "Ã¤":"ä"}
spruchfont = ImageFont.truetype("C:/Users/josch/AppData/Local/Microsoft/Windows/Fonts/"+fancy_fonts_mono[8]+".ttf",36)


for i in range(12):
    monat = monatsnamen[i]
    
    img = Image.open(path_maps+"map_"+monate[i]+"_"+monat+".png", 'r')
    background = Image.new('RGBA', (1284, 1450), (255, 255, 255, 255)) # In etwa DIN A4 Verhältnis
    offset = (0,200) # // gibt ganze Zahlen
    background.paste(img, offset)
    #d = ImageDraw.Draw(background)
    #d.text((10,10), "Hello World", fill=(255,255,0))
    
    #Überschrift
    #fnt = ImageFont.truetype("C:/Windows/Fonts/"+fancy_fonts[i]+".ttf",100)
    fntp="C:/Users/josch/AppData/Local/Microsoft/Windows/Fonts/"+fancy_fonts[i]+".ttf"
    fnt = ImageFont.truetype(fntp,50)
    d = ImageDraw.Draw(background)
    d.text((70,5), "Sperrmuell im", font=fnt, fill=fcol)
    fnt = ImageFont.truetype(fntp,100)
    d.text((200,50), monat, font=fnt, fill=fcol)
    #d.text((100,1000),"1234567891011",font=fnt, fill=(0, 0, 180))
 
    # Kalender
    fnt = ImageFont.truetype("C:/Users/josch/AppData/Local/Microsoft/Windows/Fonts/"+fancy_fonts_mono[i]+".ttf",60)
    cal=calendar.month(jahr, i+1)
    d.text((80,940),cal,font=fnt, fill=(200,0,0))

    daten = months[monate[i]]
    daten = [j[:2] for j in daten]
    daten = ",".join(daten)
    daten = re.sub("(0)(\d)","\\2",daten).split(",") #führende 0 beim Datum entfernen
    # Daten durchgehen und aus cal entfernen -> dann erst normalen cal in rot, dann lückenhaften in blau
    for j in daten:
        repl=" "
        if len(j)==2:
            repl="  "
        cal = re.sub(" "+j+" "," "+repl+" ",cal)
        cal = re.sub("\n"+j+" ","\n"+repl+" ",cal)
        cal = re.sub(" "+j+"\n"," "+repl+"\n",cal)
        cal = re.sub("\n"+j+"\n","\n"+repl+"\n",cal)
    d.text((80,940),cal,font=fnt, fill=fcol)
    
    # Kalenderspruch
    spruch = multiple_replace(replacements, sprueche[i]) #ä,ö,ü
    spruch = '"'+spruch[4:]+'"' # Zeilen im txt-Dokument beginnen mit "01: "
    offset = 1050 # y Achse Startpunkt
    fnt = spruchfont
    for line in textwrap.wrap(spruch, width=21):
        d.text((830, offset), line, font=fnt, fill=(0, 80, 0))
        offset += fnt.getsize(line)[1]


    #background.show()
    background.save(path_out+monate[i]+"_"+monat+".png")
    

    