# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from bs4.element import NavigableString

def linkify(html_doc, texto_encontrar, link, debug=False):
    soup = BeautifulSoup(html_doc, "html.parser")
    cool_nodes = set()
    texto_encontrar = re.sub(r'\s+',' ',texto_encontrar.strip())
    re_texto_encontrar = re.sub(r'\s+','\\s+',texto_encontrar)
    re_texto_encontrar = re.compile(u'\\b%s\\b' % re_texto_encontrar)


    for node in soup.find_all(text=re_texto_encontrar):
        inside_a = 'a' in [n.name for n in node.parents] # Testar com if/break depois
        print type(node), type(node.parent), node.parent.name, repr(node), inside_a
        if not inside_a:
            cool_nodes.add(node.parent)

    if type(link) in (str, unicode):
        new_tag = soup.new_tag("a", href=link)
    elif type(link) is dict:
        new_tag = soup.new_tag("a", **link)

    new_tag.string = texto_encontrar
    if debug: print unicode(new_tag)

    for sel_node in cool_nodes:
        for sel_child in sel_node.contents:
            if debug: print '----', type(sel_child), isinstance(sel_child, NavigableString)
            if isinstance(sel_child, NavigableString):
                node_replace = re.sub(re_texto_encontrar, unicode(new_tag), sel_child.string)
                node_replace = BeautifulSoup(node_replace, "html.parser")
                sel_child.string.replace_with(node_replace)
                if debug: print '----', sel_child.string, '--->', node_replace

    return soup


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

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
    <article>FFFulano Gonçalves Fulano Gonçalves Fulano Gonçalvessss Fulano    &nbsp; Gonçalves Fulano    Gonçalves</article>
    """

    print linkify(html_doc, "Fulano Gonçalves", "/fulano-goncalves.html", True)
    # print linkify(html_doc, "link", "/link.html", True)
    # print linkify(html_doc, u"Fulano Gonçalves", {'href':'ostra.html', 'target':'_blank', 'data-hub':1}, True)
    # print linkify(html_doc, u"Bunda Verde", "/000.html")
