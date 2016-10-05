# -*- coding: utf-8 -*-
from pprint import pprint as pp
import cPickle as pickle

import re
import requests
from bs4 import BeautifulSoup

h = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.335 Safari/537.36 Edge/12.346'}

url = 'http://corretorportoseguro.com/Index.aspx?corretor={}'

# Em https://corretorportoseguro.com/AreaPortalInstitucional/Contato/Default.aspx?pgn=206894&corretor=1976
# Esse formulário teoricamente só rola se o ID estiver ativo. Testar
# <span id="ctl00_ContentPlaceHolder1__UCContatoCadastro__lblDadosContatoAvancado" class="dadosContatoForm"><span>Av. baden Powell, 876 - Bairro Jd. Nova Europa<br>CEP: 13040093 / Campinas - SP / Tel.: (19)3238-7121<br>E-mail: <a href="mailto:pointseg@pointseg.com.br"><u>pointseg@pointseg.com.br</u></a></span></span>

try:
    dataset = pickle.load(open("grab_porto.pickle","rb"))
except IOError:
    dataset = {}

myrange = list(set(range(1,9000)) - set(dataset.keys()))
myrange = range(7677,7688)

print len(myrange), myrange[:200]

for id, site in ([(x,url.format(x)) for x in myrange[:200]]):
    grab_data = dict(url=site,status_code=0)

    print site

    try:
        r = requests.get(site, headers=h)
    except requests.exceptions.ConnectionError, e:
        print e
    except Exception, e:
        raise e

    if r.url != site:
        print '->', r.url,
        grab_data['url'] = r.url

    grab_data['status_code'] = r.status_code
    print grab_data['status_code'], 

    if grab_data['status_code'] == 200:

        soup = BeautifulSoup(r.text,"html.parser")
        grab_data['nome'] = soup.title.string.strip() if soup.title and soup.title.string else None

        em = soup.find_all(href=re.compile("mailto:"))

        if em:
            grab_data['emails'] = [ee.href.lower().strip().replace('mailto:','') for ee in em]

        x = soup.find('div',class_='logo')
        if x:
            print x
            y = x.find('img')
            if y:
                if y['alt'].strip() and not grab_data['nome']:
                    grab_data['nome'] = y['alt'].strip()
                grab_data['logo'] = y['src']

            dmn = x.find('a')
            if dmn:
                grab_data['domain'] = dmn['href']
                print repr(grab_data['domain']),

        print repr(grab_data['nome']),

        print
    dataset[id] = grab_data

    if id % 10 == 0:
        pickle.dump(dataset,open("grab_porto.pickle","wb"))

# print pp(dataset)
pickle.dump(dataset,open("grab_porto.pickle","wb"))
