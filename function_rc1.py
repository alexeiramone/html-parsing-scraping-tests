# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from bs4.element import NavigableString

def linkify(html_doc, texto_encontrar, link, is_aggressive=False, debug=False):
    if type(html_doc) in [str, unicode]:
        soup = BeautifulSoup(html_doc, "html.parser")
    else:
        soup = html_doc

    cool_nodes = set()

    # Don't link if inside these direct parents. The difference between these and the A element
    # is that these must be only direct, if there's a B inside a H1, I shall link, bro.
    forbidden_direct_parents = ['h2', 'h3', 'h4', 'h5', 'h6']
    forbidden_deep_parents = ['a',]

    texto_encontrar = re.sub(r'\s+',' ',texto_encontrar.strip())
    re_texto_encontrar = re.sub(r'([\\\.\+\^\$\*\?\[\]\(\)\{\}\|])',r'\\\1',texto_encontrar)
    re_texto_encontrar = re.sub(r'\s+','\\s+', re_texto_encontrar) # Precisa ser o último
    re_texto_encontrar = re.compile(u'\\b%s\\b' % re_texto_encontrar, flags=re.UNICODE)
    if debug: print 'texto_encontrar:', repr(texto_encontrar), '|', texto_encontrar

    matching_nodes = soup.find_all(text=re_texto_encontrar)

    if matching_nodes == []:
        return html_doc

    for node in matching_nodes:
        inside_a = 'a' in [n.name for n in node.parents] # Testar com if/break depois
        if debug: print type(node), type(node.parent), node.parent.name, repr(node), inside_a
        if not inside_a:
            if node.parent.name not in forbidden_direct_parents:
                cool_nodes.add(node.parent)


    # for node in matching_nodes:
    #     if debug: print type(node), type(node.parent), node.parent.name, repr(node)
    #     if node.parent.name in forbidden_direct_parents:
    #         continue
    #     for n in node.parents:
    #         if n.name in forbidden_deep_parents:
    #             continue
    #     cool_nodes.add(node.parent)


    # NEW_TAG
    if type(link) in (str, unicode):
        new_tag = soup.new_tag("a", href=link)
    elif type(link) is dict:
        new_tag = soup.new_tag("a", **link)
    elif link is None:
        new_tag = soup.new_tag("a")
        new_tag['data-hub-void'] = 'true'
    else:
        raise Exception('Link cannot be type %s. Must be str, unicode or dict with attributes.' % type(link))

    new_tag.string = texto_encontrar

    if debug: print 'TAG:', unicode(new_tag)

    # UPDATE: find links with the same data-hub and update them
    # TOTHINK: Do I need to find the text aswell? What if the text changes?
    for node in soup.find_all(**{'name':'a','data-hub':True, 'text':texto_encontrar}):
        for k,v in new_tag.attrs.items():
            node[k] = v
        if debug: print 'Update', unicode(node), '--->', unicode(new_tag)

    # Agressive Replace - replace links inside As with same term AND update current ones
    if is_aggressive:
        for node in soup.find_all('a', text=texto_encontrar):
            for k,v in new_tag.attrs.items():
                node[k] = v
            if debug: print 'Aggressive', unicode(node), '--->', unicode(new_tag)


    # Replace

    for sel_node in cool_nodes:
        for sel_child in sel_node.contents:
            if debug: print '----', type(sel_child), isinstance(sel_child, NavigableString)
            if isinstance(sel_child, NavigableString):
                node_replace = re.sub(re_texto_encontrar, unicode(new_tag), sel_child.string)
                node_replace = BeautifulSoup(node_replace, "html.parser")
                sel_child.string.replace_with(node_replace)
                if debug: print '----', sel_child.string, '--->', node_replace

    return unicode(soup)



if __name__ == '__main__':
    teste = "<p>salame salame salame bunda <b>salame</b></p><p>bunda <b><a>salame</a></b></p>"
    print linkify(teste, 'salame', '/salame.html', debug=True)