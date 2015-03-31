# -*- coding: utf-8 -*-
import sys, re
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup

html_doc = """
<h2>Heading2</h2>
<p>Texto como viria do TinyMCE. Preciso enfiar um link para o termo Fulano Gonçalves, mas não posso linkar o outro termo que já faz parte de um elemento A</p>
<p>Nesse parágrafo não posso relinkar <a href="teste" data-hub="1">Fulano Gonçalves</a> porque já faz parte de um link</p>
<p>Aqui também <a href="teste">não porque Fulano Gonçalves está dentro</a> de um A</p>
<p>Aqui é mais complexo: <a href="teste">Não posso mexer porque <b>Fulano Gonçalves</b> está dentro dum B que está dentro dum A</a></p>
<table><tr><td><div><span><b>Esse Fulano Gonçalves tem que retornar</b></span></div></td></tr></table>
<div><b>Antes Fulano Gonçalves</b><a href="teste.html">está sozinho mas antes do A</a></div>
<pre><a href="teste.html">Com o A antes, mas no mesmo parent</a> preciso linkar esse Fulano Gonçalves</pre>
<blockquote><a href="teste.html">Com o A antes, mas no mesmo parent</a> preciso linkar esse Fulano Gonçalves</blockquote>
"""


def linkify(html_doc, texto_encontrar, link, debug=False):
    soup = BeautifulSoup(html_doc, "html.parser")
    cool_nodes = set()

    for node in soup.find_all(True):
        if debug: print '[', node.name, '|',
        print 'SIBLINGS:', [repr(child) for child in node.next_siblings],
        if node.string:
            if node.name != 'a':
                text_find_pos = unicode(node.string).find(texto_encontrar)
                if text_find_pos >= 0:
                    inside_a = 'a' in [n.name for n in node.parents]
                    if debug: print 'INSIDE A?', inside_a, '|', 
                    if not inside_a:
                        cool_nodes.add(node)
                        if debug: print node.string, text_find_pos, inside_a, 'ADDED',
                    if node.parent in cool_nodes:
                        cool_nodes.remove(node.parent)
                        if debug: print 'REMOVED', node.parent.name, '|', 
                else:
                    if debug: print 'TEXT NOT FOUND:', text_find_pos, 
            else: # It's an A element
                if debug: print 'A IGNORE', 
        else: # Node doesn't have a string
            if debug: print 'NOSTRING', 
        if debug: print ']'    

    if debug: print cool_nodes
    if debug: print 'Len Cool_nodes:', len(cool_nodes)

    if type(link) in (str, unicode):
        new_tag = soup.new_tag("a", href=link)
    elif type(link) is dict:
        new_tag = soup.new_tag("a", **link)

    new_tag.string = texto_encontrar

    if debug: print unicode(new_tag)

    for sel_node in cool_nodes:
        if debug: print '----', sel_node.contents
        node_replace = unicode(sel_node.string).replace(texto_encontrar, unicode(new_tag))
        node_replace = BeautifulSoup(node_replace, "html.parser")
        sel_node.string.replace_with(node_replace)
        if debug: print '----', node_replace

    return soup

print linkify(html_doc, u"Fulano Gonçalves", {'href':'ostra.html', 'target':'_blank', 'data-hub':1}, True)
# print linkify(html_doc, u"Bunda Verde", "/000.html")
