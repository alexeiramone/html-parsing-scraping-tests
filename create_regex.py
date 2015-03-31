# -*- coding: utf-8 -*-
import re, sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Cria regex pra busca

for termo in [u'Texto Composto', 'Palavra', u"Termo com 'single quote'", u'Ação e "Double Quote"']:
    termo = re.sub(r'\s+',' ',termo.strip())
    termo = re.sub(r'\s+','\\s+',termo)
    print termo