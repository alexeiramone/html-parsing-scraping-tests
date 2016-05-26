# -*- coding: utf-8 -*-

import codecs
import requests
import sys

from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

# h = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}
# r = requests.get("http://www.uol.com.br/", headers=h)
# html = r.text
# print r.status_code, r.headers

# with codecs.open('uol.com.br.html','wb') as f:
#   f.write(html)

with codecs.open('uol.com.br.html') as f:
    html = f.read()

soup = BeautifulSoup(html,"lxml")

links = soup.find_all('a', attrs={'data-metrics': True, 'href':True})

print len(links), "links no total."

for i,link in enumerate(links):
    print i, link.get('data-metrics'), link.get('href'), link.get('name')
    x = link.find(attrs={'class': 'link'})
    if x:
        print list(x.stripped_strings)
    # for xs in link.stripped_strings:
    #     print repr(xs)