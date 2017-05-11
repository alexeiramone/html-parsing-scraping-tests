# -*- coding: utf-8 -*-
# Crawler feito à partir dum Teleport dum site em Wordpress
# Pro Glob funcionar, precisa especificar no teleport não seguir a hierarquia de pastas. Aí ele salva um bando de index-?.htm na raiz.

from glob import glob
from bs4 import BeautifulSoup

site = dict(name=None)

stats = dict(articles=0,others=0)

data_default = None

for arq in glob('C:\\Users\Alexei\\Documents\\pousoautorizado\\index*.htm'):
    entry = dict(titulo=None, imagem=None, tags='')
    with open(arq) as html:
        soup = BeautifulSoup(html,'lxml')

        meta_type = soup.find('meta', property='og:type')

        if meta_type and meta_type.get('content') != 'article':
            print arq, 'não é artigo (meta_type)'
            stats['others'] += 1
            continue

        entry['old_url'] = soup.find('meta', property='og:url').get('content') if soup.find('meta', property='og:url') else None
        if not entry['old_url']:
            print arq, 'não é artigo (não tem url)'
            stats['others'] += 1
            continue

        if not site['name'] and soup.find('meta', attrs={'name':'application-name'}):
            site['name'] = soup.find('meta', attrs={'name':'application-name'}).get('content')

        entry['titulo'] = soup.h1.text
        entry['subtitulo'] = soup.find('meta', attrs={'name':'description'}).get('content') if soup.find('meta', attrs={'name':'description'}) else None
        post = soup.select('div.entry.clear')
        entry['data_publicacao'] = soup.find('meta', property='article:published_time').get('content') if soup.find('meta', property='article:published_time') else data_default
        entry['data_ultima_atualizacao'] = soup.find('meta', property='article:modified_time').get('content') if soup.find('meta', property='article:modified_time') else data_default
        entry['imagem'] = soup.find('meta', property='og:image').get('content') if soup.find('meta', property='og:image') else None

        # for x in soup.select('div.post-footer div.categories a'):
        #     print x.text.encode('utf-8')
        # for x in soup.select('div#content div.tags a'):
        #     print x.text.encode('utf-8')

        tags_cats = set([x.text for x in soup.select('div#content div.tags a')] + [x.text for x in soup.select('div.post-footer div.categories a')])

        entry['tags'] = ','.join(list(tags_cats))

        stats['articles'] += 1

    print arq
    print entry
print site
print stats


