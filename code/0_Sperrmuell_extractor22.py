# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 19:34:46 2018

@author: josch
"""
import json
import urllib
import re
import threading
from tqdm import tqdm
from urllib.parse   import quote
from joblib import Parallel, delayed
from bs4 import BeautifulSoup
from joblib.memory import Memory

mem = Memory('.')


if __name__ == '__main__':
    akal_php = 'https://web6.karlsruhe.de/service/abfall/akal/akal.php'
    

    # this url contains all street names in karlsruhe
    streets_url = f'{akal_php}?von=A&bis=['
    response = urllib.request.urlopen(streets_url).read().decode()
    soup = BeautifulSoup(response)
    scripttags = [opt.text.strip() for opt in soup.findAll('script')]
    streets = response.split('strassenliste = ')[1].split(';')[0].replace(',]', ']')
    streets = streets.replace("'", '"')
    streets = json.loads(streets)
    assert len(streets)>1800, 'should be around 1800 streets or more in KA'
        
    #streetlist = [i.replace(" ", "%20") for i in streetlist]
    #streetlist = [i.replace(" ", u"\xc3\x9f") for i in streetlist]
    @mem.cache()
    def get_sperrmuell_date(street):
        street=street.strip()
        # not every street has every number, so test a few
        datum = 'unbekannt'
        for number in [1,2,3,4,5,6,7,8,9,9,19,22,25,30,50]:
            try:
                desc = f'Get {street} {number}'
                desc += (' ' * (50-len(desc)))
                max(tqdm._instances).set_description(desc)
            except Exception:
                pass
            url = f"{akal_php}?strasse={quote(street.strip())}&hausnr={number}"
            try:
                response = urllib.request.urlopen(url).read().decode()
            except Exception as e:
                print(f'ERROR fetching {street} {number}: {e}')
                break
            dates = re.findall(r'<br><br>(\d+.\d+.\d+)<br><br>', response)
            if len(dates)==1:
                datum = dates[0]
                break
            threading.Event().wait(0.2)

        threading.Event().wait(0.25)
        return datum
    
    # run requests in parallel
    dates = Parallel(backend='threading', n_jobs=50)(
                delayed(get_sperrmuell_date)(street) for street in tqdm(streets))
    
    streets = [x.replace('ß', 'SS') for x in streets]

    liste = {x:[] for x in sorted(set(dates), key=lambda x:x[-4:] + x[3:5] + x[:2])}
    
    for street, datum in zip(streets, dates):
        liste[datum] += [street] #Straßen werden an bisherige Liste eines Datums angehängt    
    del liste["unbekannt"]

    with open('sperrmuellkalender.json', 'w') as f:
        json.dump(liste, f, ensure_ascii=False, indent=4)            
