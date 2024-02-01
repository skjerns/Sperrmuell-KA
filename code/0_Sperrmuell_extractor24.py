# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 19:34:46 2018

@author: josch
"""
import json
import requests
import re
import threading
from tqdm import tqdm
from urllib.parse   import quote
from joblib import Parallel, delayed
from bs4 import BeautifulSoup
from joblib.memory import Memory
import ssl
import warnings

mem = Memory('.')
warnings.filterwarnings("ignore", module='urllib3')


if __name__ == '__main__':
    akal_php = 'https://web4.karlsruhe.de/service/abfall/akal/akal_2024.php'

    response = requests.get(akal_php, verify=False)

    streets = response.text.split('strassen_liste = ')[1].split(';')[0].replace(',]', ']')
    streets = streets.replace("'", '"')
    streets = json.loads(streets)
    assert len(streets)>1800, 'should be around 1800 streets or more in KA'

    #streetlist = [i.replace(" ", "%20") for i in streetlist]
    #streetlist = [i.replace(" ", u"\xc3\x9f") for i in streetlist]
    @mem.cache()
    def get_sperrmuell_date(street):
        street=street.strip()
        # street = street.replace('ß', 'ss')
        # not every street has every number, so test a few
        datum = 'unbekannt'

        for number in [1,2,3,4,5,6,7,8,9,9,19,22,25,30,50]:
            try:
                desc = f'Get {street} {number}'
                desc += (' ' * (50-len(desc)))
                max(tqdm._instances).set_description(desc)
            except Exception:
                pass
            try:
                params = {
                            'hausnr': str(number),
                         }
                data = {
                        'strasse_n': street,
                        'hausnr': str(number),
                        'anzeigen': 'anzeigen',
                        'ladeort': '1',
                        }
                response = requests.post(akal_php, params=params, data=data, verify=False)
                assert response.ok
            except Exception as e:
                print(f'ERROR fetching {street} {number}: {e}')
                break

            if 'Adresse ist unbekannt' in response.text:
                threading.Event().wait(0.2)
                continue

            street_verify = response.text.split('ladeort=1\'>')[-1].split('<')[0]
            if not street in street_verify:
                print(f'{street=} not in {street_verify=}')
                return datum
            text = response.text.split('Sperrmüllabholung')[-1]
            dates = re.findall(r'\b\d{2}\.\d{2}\.\d{4}\b', text)
            if len(dates)==1:
                datum = dates[0]
                break

        threading.Event().wait(0.25)
        if datum.isdigit():
            raise Exception(f'{street}')
        return datum

    # run requests in parallel
    dates = Parallel(backend='threading', n_jobs=50)(
                delayed(get_sperrmuell_date)(street) for street in tqdm(streets))

    streets = [x.replace('ß', 'ss') for x in streets]

    liste = {x:[] for x in sorted(set(dates), key=lambda x:x[-4:] + x[3:5] + x[:2])}

    for street, datum in zip(streets, dates, strict=True):
        liste[datum] += [street] #Straßen werden an bisherige Liste eines Datums angehängt
    if 'unbekannt' in liste:
        del liste["unbekannt"]

    with open('sperrmuellkalender.json', 'w') as f:
        json.dump(liste, f, ensure_ascii=False, indent=4)
