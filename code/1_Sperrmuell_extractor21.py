# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 19:34:46 2018

@author: josch
"""

import urllib
import re
import pandas as pd
from urllib.parse   import quote
from datetime import date, timedelta


d1 = date(2021, 1, 1)  # start date
d2 = date(2021, 12, 31)  # end date
delta = d2 - d1         # timedelta
dates = []
for i in range(delta.days + 1):
    dates.append((d1 + timedelta(i)).strftime('%d.%m.%Y'))
liste = pd.DataFrame(dates+["unbekannt<"]) #unbekannt als letzter Eintrag, steht bei Straßen anstelle des Datums im HTML Code
liste = liste.set_index([0])
liste.loc[:, "Strasse"] = "" # dataframe mit leeren Einträgen füllen, an die angehängt wird

path = r"C:\Users\josch\Documents\Python Scripts\Sperrmuell21"
with open(path+r"\Ka_A-Z.txt") as f:
    links = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
links = [x.strip() for x in links] 
# for straßen links extrahieren
for i in links:
    #i=links[0]
    response = urllib.request.urlopen(i)
    data = response.read()
    split1 = "<option selected value=1>" # Anfang der Straßenliste
    split2 = "</option></select>\t\t</TD>" # Ende der Straßenliste
    splitted=data.decode().split(split1)
    try:
        splitted=splitted[1].split(split2)[0]
    except IndexError:
        print(i)
        
    streetlist = re.split("</option><option value=\d+>", splitted) # \d+ : eine oder mehr Zahlen aus HTML Code
    #streetlist = [i.replace(" ", "%20") for i in streetlist]
    #streetlist = [i.replace(" ", u"\xc3\x9f") for i in streetlist]

    for j in streetlist:#range(0,5):
        #j=streetlist[38]
        url = "https://web3.karlsruhe.de/service/abfall/akal/akal.php?strasse=" + quote(j)
        response = urllib.request.urlopen(url)
        data= response.read()
        try:
            datum_j = data.decode().split("ll auf Abruf</td><td valign=top><br><br>")[1][0:10]
        except UnicodeDecodeError:
            datum_j = "unbekannt<"
        except IndexError:
            datum_j = "unbekannt<"
        liste.loc[datum_j, "Strasse"] = liste.loc[datum_j, "Strasse"]+", "+ j #Straßen werden an bisherige Liste eines Datums angehängt    

liste.to_csv(path+r"\Sperrmuellkalender.csv")
        
liste=pd.read_csv(path+r"\Sperrmuellkalender.csv")
liste=liste.set_index("0")

#liste_kopie = liste
liste= liste.drop(["unbekannt<"])
liste=liste.fillna('')
liste = liste[liste["Strasse"]!=""]



for i in liste.index:
    #i=liste.index[0]
    temp=liste.loc[i,"Strasse"].split(", ")[1:]
    temp1=[]
    for j in temp:
        temp1.append(re.split(" \d", j)[0])  
    liste.loc[i,"Strasse"] = ", ".join(pd.unique(temp1))
        
liste.to_csv(path+r"\Sperrmuellkalender.csv")
        
