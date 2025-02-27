# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 21:15:20 2019

@author: josch
"""
# params
jahr = 2025
path="C:/Users/joan9/Documents/Python Scripts/Sperrmuell/2025/"
path_f = "C:/Users/joan9/AppData/Local/Microsoft/Windows/Fonts/"
#
import json
from PIL import Image
from PIL import ImageDraw, ImageFont

import calendar
import re
import os
import textwrap
os.chdir(path)
from commons import multiple_replace
path_maps = path + "png_html/"
path_imgs = path + "Bilder/"
imgs = os.listdir(path_imgs)
path_out = path + "print/"

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
               "StripesCaps","Today__","Bemydor",
               "CoventryGardenNF","BigLou","UndergroundNF",
               "Alyfe Demo","Beyond Wonderland","Mugnuts"]#,"nauvo__",ExtraOrnamentalNo2
fancy_fonts_mono = "IckyTicketMono"

monatsnamen = ['Januar','Februar','Maerz','April','Mai','Juni',
               'Juli','August','September','Oktober','November','Dezember']
monate = ["01","02","03","04","05","06","07","08","09","10","11","12"]
fcol = (0, 0, 180) # Schriftfarbe



for i in range(12):
    monat = monatsnamen[i]
    
    img = Image.open(path_maps+"map_"+monate[i]+"_"+monat+".png", 'r')
    size = (int(img.size[0]*1.1), int(img.size[1]*2))
    background = Image.new('RGBA', size, (255, 255, 255, 255)) # In etwa DIN A4 Verhältnis
    offset = (int(img.size[0]*0.05),int(img.size[0]*0.15))
    background.paste(img, offset)
    
    # Zusatzbild, Meme
    img = Image.open(path_imgs+imgs[i], 'r')
    offset = (int(size[0]*0.58), int(size[1]*0.57)) 
    background.paste(img, offset)
    #d = ImageDraw.Draw(background)

    
    #Überschrift
    fntp = path_f+fancy_fonts[i]+".ttf"
    fnt = ImageFont.truetype(fntp,72)
    d = ImageDraw.Draw(background)
    d.text((80,50), "Sperrmuell im", font=fnt, fill=fcol)
    fnt = ImageFont.truetype(fntp,130)
    d.text((220,120), monat, font=fnt, fill=fcol)
 
    # Kalender
    fnt = ImageFont.truetype(path_f+fancy_fonts_mono+".ttf",85)
    cal=calendar.month(jahr, i+1)
    cal_pos = (int(size[1]*0.08), int(size[1]*0.68))
    d.text(cal_pos,cal,font=fnt, fill=(200,0,0))

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
    d.text(cal_pos,cal,font=fnt, fill=fcol)
    
    #background.show()
    background.save(path_out+monate[i]+"_"+monat+".png")
    
    
#Kalendersprüche für die Ecke unten rechts (QR Code im vorherigen Design)
# with open('Kalenderspruch.txt', 'r') as f:
#     sprueche = f.read().splitlines() # besser als readlines, weil hier kein \n bleibt.
# replacements = {"Ã¼":"ü", "Ã¶":"ö", "Ã¤":"ä", "Ã–":"Ö", "ÃŸ":"ß", "Ã„":"Ä"}
# sprueche = [multiple_replace(replacements, sprueche[i]) for i in range(12)]

# spruchfont = ImageFont.truetype("C:/Users/josch/AppData/Local/Microsoft/Windows/Fonts/"+fancy_fonts_mono[8]+".ttf",36)

# -> diesen Teil in die for-Schleife
     # # Kalenderspruch
     # spruch = sprueche[i]
     # spruch = spruch[4:] # Zeilen im txt-Dokument beginnen mit "01: "
     # offset = 1100 # y Achse Startpunkt
     # fnt = spruchfont
     # for line in textwrap.wrap(spruch, width=25):
     #     d.text((830, offset), line, font=fnt, fill=(0, 80, 0))
     #     offset += 45#fnt.getsize(line)[1] + 10
