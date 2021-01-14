# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 21:15:20 2019

@author: josch
"""

from PIL import Image
from PIL import ImageDraw, ImageFont
import qrcode
import calendar
import pandas as pd
import re
path_maps = "C:/Users/josch/Documents/Python Scripts/Sperrmuell21/png_html/map_"
path_out = "C:/Users/josch/Documents/Python Scripts/Sperrmuell21/output_print/"
path= "C:/Users/josch/Documents/Python Scripts/Sperrmuell21/"
liste=pd.read_csv(path+r"\Sperrmuellkalender.csv")
liste=liste.set_index("0")

last=""
monate = [] # sieht nachher so aus: monate = [["07.01","31.01"],["04.02","28.02"]...]
first=liste.index[0]
for j in liste.index:
    if j[3:5]!=first[3:5]: # j gehört zum neuen Monat
        monate.append([first,last])
        first=j
    else: # j gehört zum alten Monat
        last=j
monate.append([first,last]) # noch den Dezember anhängen    
jahr = int(last[6:])

fancy_fonts = ["Bemydor","Autumn Moon - TTF","Alyfe Demo",
               "StripesCaps","Today__","Malache Crunch",
               "CoventryGardenNF","BigLou","UndergroundNF",
               "ExtraOrnamentalNo2","Beyond Wonderland","Mugnuts"]#,"nauvo__",
fancy_fonts_mono = "IckyTicketMono,Kingthings Trypewriter 2,Vanthian Ragnarok,Beccaria,Harting Plain,EXITFONTFORAFILM,software_tester,Kingthings Trypewriter 2,Harting Plain,IckyTicketMono,Kingthings Trypewriter 2,EXITFONTFORAFILM".split(",")
#fancy_fonts_mono = "IckyTicketMono,Kingthings Trypewriter 2,Vanthian Ragnarok,Beccaria,Harting Plain,EXITFONTFORAFILM,software_tester,hydrogen,Harting Plain,IckyTicketMono,Kingthings Trypewriter 2,EXITFONTFORAFILM".split(",")
monatsnamen = ['Januar','Februar','Maerz','April','Mai','Juni',
               'Juli','August','September','Oktober','November','Dezember']

f=open(path+"Dropbox_Links.txt","r")
links = f.read()
#i=0
fcol = (0, 0, 180)
qr_offs = (1000,932) 
qr_box=7
qr_col="#5080EF"
for i in range(12):
    monat = monatsnamen[i]
    
    img = Image.open(path_maps+monat+".png", 'r')
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
    anfang = monate[i][0]
    ende = monate[i][1]
    daten = liste.loc[anfang:ende].index.tolist()
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
    
    #QR Code
    link=links.split(monat+"-")[1]
    link=link.split("\n")[0]
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=qr_box,
        border=0,
        )
    qr.add_data(link)
    qrc = qr.make_image(fill_color=qr_col, back_color="white")
    offset = qr_offs
    background.paste(qrc, offset)
    fnt = ImageFont.truetype("C:/Users/josch/AppData/Local/Microsoft/Windows/Fonts/neon_pixel-7.ttf",35)
    d.text((qr_offs[0],qr_offs[1]+qr_box*34),"komplette Karte",font=fnt, fill=qr_col)
    
    #background.show()
    background.save(path_out+str(i+1)+"_"+monat+".png")
    

    