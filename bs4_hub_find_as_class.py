# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from bs4.element import NavigableString

class NoodleText(object):
    """docstring for NoodleText"""
    def __init__(self, html_doc, parser="html.parser", debug=False):
        super(NoodleText, self).__init__()
        self.soup = BeautifulSoup(html_doc, parser)
        self.debug = debug
        self.parser = parser

    def render(self):
        return unicode(self.soup)

    def print_debug(self, *args):
        if self.debug:
            for arg in args:
                print arg,
            print
        
    def linkify(self, texto_encontrar, link):
        cool_nodes = set()
        texto_encontrar = re.sub(r'\s+',' ',texto_encontrar.strip())
        re_texto_encontrar = re.sub(r'([\\\.\+\^\$\*\?\[\]\(\)\{\}\|])',r'\\\1',texto_encontrar)
        re_texto_encontrar = re.sub(r'\s+','\\s+', re_texto_encontrar) # Precisa ser o último
        re_texto_encontrar = re.compile(u'\\b%s\\b' % re_texto_encontrar, flags=re.UNICODE)
        self.print_debug('texto_encontrar:', repr(texto_encontrar), '|', texto_encontrar)

        self.print_debug('Elements', self.soup.find_all(True))
        self.print_debug('Total elements', len(self.soup.find_all(True)))

        soup_find = self.soup.find_all(text=re_texto_encontrar)

        for node in soup_find:
            inside_a = 'a' in [n.name for n in node.parents] # Testar com if/break depois
            self.print_debug(type(node), type(node.parent), node.parent.name, repr(node), inside_a)
            if not inside_a:
                cool_nodes.add(node.parent)
        self.print_debug('Find_all:', len(soup_find))

        if type(link) in (str, unicode):
            new_tag = self.soup.new_tag("a", href=link)
        elif type(link) is dict:
            new_tag = self.soup.new_tag("a", **link)

        new_tag.string = texto_encontrar
        self.print_debug('TAG:', unicode(new_tag))

        for sel_node in cool_nodes:
            for sel_child in sel_node.contents:
                self.print_debug('--', type(sel_child), isinstance(sel_child, NavigableString))
                if isinstance(sel_child, NavigableString):
                    node_replace = re.sub(re_texto_encontrar, unicode(new_tag), sel_child.string)
                    node_replace = BeautifulSoup(node_replace, self.parser)
                    # sel_child.replace_with(node_replace)
                    # sel_child.string = node_replace
                    sel_child.replace_with(node_replace)
                    self.print_debug('----', sel_child.string, '--->', node_replace)


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

    noodle = NoodleText(html_doc, debug=True)
    noodle.linkify("Blelaelalel", "/buuu.js")
    noodle.linkify("link", "/link")
    noodle.linkify("Fulano Gonçalves", "/fulano-goncalves.html")

    print noodle.render()