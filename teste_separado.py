# -*- coding: utf-8 -*-
from bs4_hub_find_alternate import linkify

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    print linkify(u"<p>Bundá</p>", "Bunda", "/bunda")
    print linkify(u"<p>Bundá Bunda Bünda</p>", "Bunda", "/bunda")
    print linkify(u"<p>Bundá Bunda Bünda</p>", "Bundá", "/bunda")
    print linkify(u"<p>Bundá Bunda Bünda</p>", "Bünda", "/bunda")
    # print linkify(html_doc, "link", "/link.html", True)
    # print linkify(html_doc, u"Fulano Gonçalves", {'href':'ostra.html', 'target':'_blank', 'data-hub':1}, True)
    # print linkify(html_doc, u"Bunda Verde", "/000.html")
