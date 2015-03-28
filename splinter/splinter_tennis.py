# -*- coding: utf-8 -*-
import codecs, hashlib, time
from splinter import Browser
from splinter_tennis_temp import parse_tennis_table

url = r'http://www.flashscore.com/tennis/'

with Browser('chrome') as browser:
    browser.visit(url)
    print browser.title
    last_hash = ''
    for waiter in range(0,3):
        html_page = browser.html.encode("utf8")
        hash_string = hashlib.md5(html_page).hexdigest()
        if hash_string != last_hash:
            print len(html_page), hash_string
            parse_tennis_table(html_page)
            last_hash = hash_string
        else:
            print 'Sleep'
        time.sleep(20)

    with codecs.open('splinter_tennis.html','w', 'utf-8') as file:
        file.write(browser.html)
    file.close()
