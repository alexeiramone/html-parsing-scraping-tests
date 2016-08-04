# -*- coding: utf-8 -*-
from pprint import pprint as pp
import cPickle as pickle

import requests
from bs4 import BeautifulSoup

h = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}

url = 'http://corretorportoseguro.com/Index.aspx?corretor={}'

# Em https://corretorportoseguro.com/AreaPortalInstitucional/Contato/Default.aspx?pgn=206894&corretor=1976
# Esse formulário teoricamente só rola se o ID estiver ativo. Testar

try:
    dataset = pickle.load(open("grab_porto.pickle","rb"))
except IOError:
    dataset = {}

myrange = list(set(range(1,7000)) - set(dataset.keys()))

print len(myrange), myrange[:200]

for id, site in ([(x,url.format(x)) for x in myrange[:200]]):
    grab_data = dict(url=site,status_code=0)

    print site

    r = requests.get(site, headers=h)

    grab_data['status_code'] = r.status_code
    print grab_data['status_code'], 

    if grab_data['status_code'] == 200:

        soup = BeautifulSoup(r.text,"html.parser")
        grab_data['nome'] = soup.title.string.strip() if soup.title and soup.title.string else None

        x = soup.find('div',class_='logo')
        if x:
            y = x.find('img')
            if y:
                if y['alt'].strip() and not grab_data['nome']:
                    grab_data['nome'] = y['alt'].strip()
                grab_data['logo'] = y['src']

        print repr(grab_data['nome']),

        print
    dataset[id] = grab_data

    if id % 10 == 0:
        pickle.dump(dataset,open("grab_porto.pickle","wb"))

# print pp(dataset)
