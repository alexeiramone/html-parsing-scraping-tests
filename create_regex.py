# -*- coding: utf-8 -*-
import re, sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Cria regex pra busca

for termo in [u'Texto Composto', 'Palavra', u"Termo com 'single quote'", u'Ação e "Double Quote"', u"Pergunta?", 'Bunda.+', 'R$50', 'CP\\500', 'Assim (assado D|X)']:
    termo = re.sub(r'\s+',' ',termo.strip())
    termo = re.sub(r'([\\\.\+\^\$\*\?\[\]\(\)\{\}\|])',r'\\\1',termo)
    termo = re.sub(r'\s+','\\s+',termo) # Vem por último senão ele escapa \ e +
    print termo