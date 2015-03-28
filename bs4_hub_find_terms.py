# -*- coding: utf-8 -*-
import sys, re
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup

html_doc = """
<h2>Heading2</h2>
<p>Texto como viria do TinyMCE. Preciso enfiar um link para o termo Salame Amarelo, mas não posso linkar o outro termo que já faz parte de um elemento A</p>
<p>Nesse parágrafo não posso relinkar <a href="teste" data-hub="1">Salame Amarelo</a> porque já faz parte de um link</p>
<p>Aqui também <a href="teste">não porque Salame Amarelo está dentro</a> de um A</p>
<p>Aqui é mais complexo: <a href="teste">Não posso mexer porque <b>Salame Amarelo</b> está dentro dum B que está dentro dum A</a></p>
<table><tr><td><div><span><b>Esse Salame Amarelo tem que retornar</b></span></div></td></tr></table>
"""


def linkify(html_doc, texto_encontrar, link):
    soup = BeautifulSoup(html_doc, "html.parser")
    a_nodes_with_text = soup('a', text=texto_encontrar)
    cool_nodes = set()

    for node in soup.find_all(True):
        # print node.name
        if node.string:
            if node.name != 'a':
                text_find_pos = unicode(node.string).find(texto_encontrar)
                if text_find_pos >= 0:
                    inside_a = 'a' in [n.name for n in node.parents]
                    if not inside_a:
                        cool_nodes.add(node)
                        # print node.name, node.string, text_find_pos, inside_a, 'added'
                    if node.parent in cool_nodes:
                        cool_nodes.remove(node.parent)
                        # print node.parent, 'removed'
                        # print node.name, node.string, '::', text_find_pos, inside_a

    # print len(cool_nodes)
    # print cool_nodes
    if type(link) in (str, unicode):
        new_tag = soup.new_tag("a", href=link)
    elif type(link) is dict:
        new_tag = soup.new_tag("a", **link)
        # new_tag['data-hub'] = 1
    new_tag.string = texto_encontrar

    # print unicode(new_tag)

    for sel_node in cool_nodes:
        # print '----', sel_node.contents
        node_replace = unicode(sel_node.string).replace(texto_encontrar, unicode(new_tag))
        node_replace = BeautifulSoup(node_replace, "html.parser")
        sel_node.string.replace_with(node_replace)
        # print '----', node_replace

    # print soup
    return soup

# print linkify(html_doc, u"Salame Amarelo", "/bunda.html")
print linkify(html_doc, u"Salame Amarelo", {'href':'ostra.html', 'target':'_blank', 'data-hub':1})
print linkify(html_doc, u"Bunda Verde", "/000.html")
