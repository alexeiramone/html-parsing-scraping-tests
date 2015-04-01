# -*- coding: utf-8 -*-
from bs4_hub_find_alternate import linkify

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    print linkify(u"<p>Bundá Bunda Bünda</p>", "Bunda", "/teste")
    print linkify(u"<p>Bundá Bunda Bünda</p>", "Bundá", "/teste")
    print linkify(u"<p>Bundá Bunda Bünda</p>", "Bünda", "/teste")
    print linkify(u"<p>Ação às vêzes</p>", "ação", "/teste")
    print linkify(u"<p>Ação às vêzes</p>", "às vezes", "/teste")
    print linkify(u"<p>Ação às vêzes</p>", "às vêzes", "/teste")
