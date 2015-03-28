# -*- coding: utf-8 -*-
import sys, re
reload(sys)
sys.setdefaultencoding('utf-8')

html_doc = """
<h2>Heading2</h2>
<p>Texto como viria do TinyMCE. Preciso enfiar um link para o termo Salame Amarelo, mas não posso linkar o outro termo que já faz parte de um elemento A</p>
<p>Nesse parágrafo não posso relinkar <a href="teste" data-hub="1">Salame Amarelo</a> porque já faz parte de um link</p>
<p>Aqui também <a href="teste">não porque Salame Amarelo está dentro</a> de um A</p>
<p>Aqui é mais complexo: <a href="teste">Não posso mexer porque <b>Salame Amarelo</b> está dentro dum B que está dentro dum A</a></p>
<table>
    <tr>
        <td>
            <div><span><b>Esse Salame Amarelo tem que retornar</b></span></div>
        </td>
    </tr>
</table>
"""

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc)

texto_encontrar = u"Salame Amarelo"

def get_nodes_not_parent_of(soupnode, tag):
    good = set()
    for tx in soupnode.find_all(tag):
        pai = tx.parent
        pai_direto = pai
        print tx, pai, ':',
        good.add(pai_direto)
        while pai:
            print pai.name,
            if pai.name == 'a':
                good.remove(pai_direto)
                print '|'
                break
            pai = pai.parent
    return good

def find_nodes(text):
    good = set()
    for tx in soup.find_all(True):
        print tx.name

# print find_nodes(texto_encontrar)
# print get_nodes_not_parent_of(texto_encontrar)

# print soup.prettify()

# print soup.find_all('a')
# print get_nodes_not_parent_of(soup, 'a')

a_nodes_with_text = soup('a', text=texto_encontrar)

cool_nodes = set()

for node in soup.find_all(True):
    if node.string:
        if node.name != 'a':
            has_text = unicode(node.string).find(texto_encontrar)
            if has_text:
                inside_a = 'a' in [n.name for n in node.parents]
                print node.name, node.string, '::', has_text, inside_a
                cool_nodes.add(node)

print len(cool_nodes)

