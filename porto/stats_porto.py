# -*- coding: utf-8 -*-
from pprint import pprint as pp
import cPickle as pickle

try:
    dataset = pickle.load(open("grab_porto.pickle","rb"))
except IOError:
    dataset = {}

unique_names = set()

print 'TOTAL', len(dataset.keys()), 

for k,v in dataset.iteritems():
    unique_names.add(v.get('nome',None))
    if v.has_key('domain'):
        print v['domain']

print 'UNIQUE_NAMES', len(unique_names), 

# print pp(dataset)
