# -*- coding: utf-8 -*-
import codecs
from lxml import etree, html

def nonefy(value):
    if value in (u'\xa0', '', None, '-'):
        return None
    return value

def parse_tennis_table(plain):
    dom = html.fromstring(plain)
    for table in dom.xpath("//table[@class='tennis']"):
        torneio = table.xpath('thead/tr[1]/td[2][starts-with(@class,"head_ab")]//span[@class="country_part"]/text()')[0]
        localidade = table.xpath('thead/tr[1]/td[2][starts-with(@class,"head_ab")]//span[@class="tournament_part"]/text()')[0]
        dia = dom.xpath('//li[@id="ifmenu-calendar"][1]/span[2]/span[@class="h2"]/a/text()')[0]
        print torneio, localidade, dia
        for tr in table.xpath("tbody/tr"):
            children = tr.getchildren()
            tr_len = len(children)
            #print tr_len
            if tr_len == 14: # primeira linha, player 1
                dados = dict(id=tr.get('id')) # começa um novo jogo
                _, hora, status, servico1, player1, score1, p1set1, p1set2, p1set3, p1set4, p1set5, p1set6, _, _ = children
                dados['hora'] = hora.text
                dados['status'] = status.find('span').text
                dados['player1'] = player1.find('span').text
                dados['score1'] = nonefy(score1.text)
                dados['p1set1'] = nonefy(p1set1.text)
                dados['p1set2'] = nonefy(p1set2.text)
                dados['p1set3'] = nonefy(p1set3.text)
                dados['p1set4'] = nonefy(p1set4.text)
                dados['p1set5'] = nonefy(p1set5.text)
                dados['p1set6'] = nonefy(p1set6.text)
            elif tr_len == 9: # segunda linha, player 2
                servico2, player2, score2, p2set1, p2set2, p2set3, p2set4, p2set5, p2set6 = children
                dados['player2'] = player2.find('span').text
                dados['score2'] = nonefy(score2.text)
                dados['p2set1'] = nonefy(p2set1.text)
                dados['p2set2'] = nonefy(p2set2.text)
                dados['p2set3'] = nonefy(p2set3.text)
                dados['p2set4'] = nonefy(p2set4.text)
                dados['p2set5'] = nonefy(p2set5.text)
                dados['p2set6'] = nonefy(p2set6.text)
            else: # done
                print dados

if __name__ == '__main__':
    with codecs.open('splinter_tennis.html','r', 'utf-8') as file:
        parse_tennis_table(file.read())
    file.close()
