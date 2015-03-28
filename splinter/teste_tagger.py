# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

titulos = [u'Corinthians é lindo', u'São Paulo é time de bixa', 
    u'Remo, Palmeiras e Náutico são uma merda', u'Alexei Forever Young', ''
    ]

times = ['Corinthians', 'Palmeiras', 'São Paulo', 'Remo', 'Náutico']

for titulo in titulos:
    print titulo, [time for time in times if titulo.find(time) >= 0]
    # for time in times:
    #     if titulo.find(time) >= 0:
    #         print time, '|', 
