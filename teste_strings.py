# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

def teste_string(html_doc, parser="html.parser", debug=False):
	soup = BeautifulSoup(html_doc, parser)
	for item in soup(text=True):
		print type(item), len(item), "|", item, "|"

	return soup



if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    print teste_string(u"texto <b>forever<b>, texto sei lá, texto composto que preciso trocar pelo texto composto que precisa ser trocado.")
