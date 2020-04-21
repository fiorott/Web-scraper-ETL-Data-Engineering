# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 21:58:17 2019

@author: fioro
"""
#! python3 # busca_zap_estavel.py - Launches a map in the browser using an address from the # command line or clipboard.
import pprint, csv
import re
from lxml import html
import requests, bs4
import pandas as pd
import numpy as np
from pandas import DataFrame

from bs4 import BeautifulSoup
url = 'http://www.zapimoveis.com.br/venda/imoveis/pr+curitiba/?pagina=4&__zt=nrp:b'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
page = requests.get(url, headers=headers)
tree = html.fromstring(page.content)
#This will create a list of buyers:
#preco = tree.xpath('//*[@id="app"]/section/div/div/section/div[*]/div/div[2]/div[1]/p/text()')
#metragem = tree.xpath('//*[@id="app"]/section/div/div/section/div[*]/div/div[2]/div[3]/ul/li[1]/span/text()')
#localizacao = tree.xpath('//*[@id="app"]/section/div/div/section/div[*]/div/div[2]/div[3]/p/a/text()')
#descricao = tree.xpath('//*[@id="app"]/section/div/div/section/div[*]/div/div[2]/div[2]/div/span/text()[1]')
link = tree.xpath('//*[@id="app"]/section/div/div/section/div[*]/div/div[2]/div[3]/p/a/@href')

convert_ids = []

def Convert_Link(lista):

    for l in range(len(lista)):
        
        link_texto = [str(lista[l])]
        Id_Regex = re.compile(r'\d\d\d\d\d\d\d\d\d\d')
        found_id = Id_Regex.search(str(lista[l])) 
        convert_ids.insert(l,found_id.group())
        
Convert_Link(link)     
#print(convert_ids)

#quebra a informação da localização em duas variaveis: rua e bairro

bairror = []
ruar = []
def obtem_bairro_rua(lista_loc):

    for t in range(len(lista_loc)):

        loc_Regex = re.compile(r'(.*)(,)(.*)')
        found_loc = loc_Regex.search(str(lista_loc[t]))
        ruar.append(found_loc.group(1))
        bairror.append(found_loc.group(3))

import datetime
agora = datetime.datetime.now()

        
# Esta função verifica se todas as variáveis de informação têm os mesmos elementos:
def verifica_elementos (lista_de_var):
    count_err = 0
    for i in lista_de_var:
        if len(i) != len(lista_de_var[0]):
            print('deu problema')
            count_err = count_err + 1
        else:
            print('tudo ok')
    return count_err     
                   
#Ideia -> fazer o scrapping usando REGEX do tetxi gerado pelo comando   print(page.text)          
print(page.text)

soup = BeautifulSoup(url, 'html.parser')
soup.select('input[name]')
Extrat_Soup = bs4.BeautifulSoup(page.text)
#N = len(Extrat_Soup.select('div[class="card-container"]'))
#LI = Extrat_Soup.select('li[class="feature__item text-small js-bedrooms"]')
#    
## A consulta abaixo traz os quartos vários spans, incluindo o que contém dormitórios, etc
#LI_quartos = Extrat_Soup.select('li[class="feature__item text-small js-bedrooms"]')
#
## A consulta abaixo traz os quartos vários spans, incluindo o que contém garagens e banheiros e area, etc
#LI_garagem = Extrat_Soup.select('li[class="feature__item text-small"]')

for link in Extrat_Soup.select('li[class="feature__item text-small"]'):
    
    print(link.get_text('href'))
    
#Tentativa de obter todas as informações que preciso:
link_preco = []
link_localizacao= []
link_quarto= []
contador = 0
CCP = []
CC = []
# acha cada elemento dos cards, chamndo de link"
for link in Extrat_Soup.select('div[class="card-container"]'):
    contador= contador + 1
   # print('link    :' , contador)
    print(link.prettify())
    # acha o elemento p da classe preço  
  #  for p in link.find_all('p'):
        #print(p['class'])
        
        #print(p.get_text())
    # Armazena Preço
    for p in link.select('p[class="simple-card__price js-price heading-regular heading-regular__bolder align-left"]'):
        pr = p.get_text()
        print(pr)
        link_preco.append(pr)
    # Armazena localização 
    for p in link.select('p[class="color-dark text-regular simple-card__address"]'):
        loc = p.get_text()
        print(loc)
        link_localizacao.append(loc)
        
    for li in link.select('li[class="feature__item text-small js-bedrooms"]'):
        qua = li.get_text()
        print(qua)
        link_quarto.append(qua)

   # t_p_cl_preco = Extrat_Soup.find("p", class="simple-card__price js-price heading-regular heading-regular__bolder align-left")
    #print(t_p_cl_preco.get_text())
    CCP.append(link)
    CC.append(link.get_text(" - "))
    
    print('___________________')

CL = []
count = 0
for link in Extrat_Soup.select('div[class="card-listing simple-card js-listing-card"]'):
    count= count + 1
    print('link    :' , count)
    print(link.get_text(" - "))
#    print(link.findNextSibling())
    print('___________________')
    CL.append(link.get_text(" - ")) 


def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

  #MEGA REGEX - Extrai todad as informações a partir o get text feito no div card container

situacaor = []  
precor = []
descricaor = []
bairro_ruar = []
metragemr = []
quartosr = []
garagensr =[]
banheirosr=[]
condominior=[]
linkr =[]
linkr2 =[]
dia_horar =[]
#situacao_texto =[]
def mega_regex(get_text_div):
    #extrai dia hora da captura
    for m in range(len(get_text_div)):
        
        
        
        dia_horar.append(datetime.datetime.now())
    #extrai situação
    for m in range(len(get_text_div)):
        situacao_Regex = re.compile(r'(white text-small">)(\w+)')
        found_situacao = situacao_Regex.search(str(get_text_div[m]))
        situacaor.append(found_situacao.group(2))
     #extrai preço   
    for m in range(len(get_text_div)):
        preco_Regex = re.compile(r'(ft">)(\s+)(\S+)(\s)((\d+).(\d+).(\d+))')
        if preco_Regex.search(str(get_text_div[m])) is None:
            found_preco = 'None'
            precor.append(found_preco)
        else:
            found_preco = preco_Regex.search(str(get_text_div[m]))
            precor.append(found_preco.group(5))              
    #extrai descrição
    for m in range(len(get_text_div)):
        descricao_Regex = re.compile(r'(__text">)(.*)(</span>)')
        if descricao_Regex.search(str(get_text_div[m])) is None:
            found_descricao = 'None'
            descricaor.append(found_descricao)
        else:
            found_descricao = descricao_Regex.search(str(get_text_div[m]))
            descricaor.append(found_descricao.group(2))
    #extrai bairro_rua
    for m in range(len(get_text_div)):
        bairro_rua_Regex = re.compile(r'(-lines="1">)(.*)(</p><ul)')
        if bairro_rua_Regex.search(str(get_text_div[m])) is None:
            found_bairro_rua = 'None'
            bairro_ruar.append(found_bairro_rua)
        else:
            found_bairro_rua = bairro_rua_Regex.search(str(get_text_div[m]))
            bairro_ruar.append(found_bairro_rua.group(2))  
        #EXTRA NESTE: chama a funçao que quebra a string em bairro e rua            
    obtem_bairro_rua(bairro_ruar)
    #extrai metragem
    for m in range(len(get_text_div)):

        metragem_Regex = re.compile(r'(rea"></use></svg><span>)(\n)(        )(.*)')
        if metragem_Regex.search(str(get_text_div[m])) is None:
            found_metragem = 'None'
            metragemr.append(found_metragem)
        else:
            found_metragem = metragem_Regex.search(str(get_text_div[m]))
            metragemr.append(found_metragem.group(4))   
    #extrai quartos
    for m in range(len(get_text_div)):

        quartos_Regex = re.compile(r'(#bedroom"></use></svg><span>)(\n)(        )(.*)')
        if quartos_Regex.search(str(get_text_div[m])) is None:
            found_quartos = 'None'
            quartosr.append(found_quartos)
        else:
            found_quartos = quartos_Regex.search(str(get_text_div[m]))
            quartosr.append(found_quartos.group(4))  
    #extrai garagens
    for m in range(len(get_text_div)):

        garagens_Regex = re.compile(r'(#parking"></use></svg><span>)(\n)(        )(.*)')
        if garagens_Regex.search(str(get_text_div[m])) is None:
            found_garagens = 'None'
            garagensr.append(found_garagens)
        else:
            found_garagens = garagens_Regex.search(str(get_text_div[m]))
            garagensr.append(found_garagens.group(4))  
    #extrai banheiros
    for m in range(len(get_text_div)):

        banheiros_Regex = re.compile(r'(#bathroom"></use></svg><span>)(\n)(        )(.*)')
        if banheiros_Regex.search(str(get_text_div[m])) is None:
            found_banheiros = 'None'
            banheirosr.append(found_banheiros)
        else:
            found_banheiros = banheiros_Regex.search(str(get_text_div[m]))
            banheirosr.append(found_banheiros.group(4))  
    #extrai condominio
    for m in range(len(get_text_div)):

        condominio_Regex = re.compile(r'(card-price__value">)(.*)(</span></li>)')
        
        if condominio_Regex.search(str(get_text_div[m])) is None:
            found_condominio = 'None'
            condominior.append(found_condominio)
        else:
            found_condominio = condominio_Regex.search(str(get_text_div[m]))
            condominio_corte = str(found_condominio.group(2))
              #Não consegui pegar o valor perfeitamente, então farei abaixo uma gambiarra para arrumar a string final antes de armazenar    
            condominior.append(condominio_corte[3:])  
    #extrai link
    for m in range(len(get_text_div)):

        link_Regex = re.compile(r'(<a class="simple-card__link")(.*)(nrp%3Ab">)')
  
        if link_Regex.search(str(get_text_div[m])) is None:
            found_link = 'None'
            linkr.append(found_link)
        else:
            found_link = link_Regex.search(str(get_text_div[m]))
            link_corte = str(found_link.group(2))
              #Não consegui pegar o link perfeitamente, então farei abaixo uma gambiarra para arrumar a string final antes de armazenar    
            linkr.append(str('zapimoveis.com.br'+ link_corte[7:]+ 'nrp%3Ab'))  

    #extrai link novo
    for m in range(len(get_text_div)):

        link2_Regex = re.compile(r'([content_ids]=)(.*)(&amp;)')
  
        if link2_Regex.search(str(get_text_div[m])) is None:
            found_link = 'None'
            linkr2.append(found_link)
        else:
            found_link2 = link2_Regex.search(str(get_text_div[m]))
            link2_corte = str(found_link2.group(2))
              #Não consegui pegar o link perfeitamente, então farei abaixo uma gambiarra para arrumar a string final antes de armazenar    
            linkr2.append(str('zapimoveis.com.br'+ link_corte[7:]+ 'nrp%3Ab'))


            
mega_regex(CCP)     
#removi o campo descriçãor da informação que é compilada. 
list_of_lists = [convert_ids, situacaor, bairror, ruar, metragemr, precor, condominior,  quartosr, garagensr, banheirosr, linkr, dia_horar]
fieldnames = ['id', 'situacao', 'bairro', 'rua', 'metragem', 'preco', 'condominio',  'quartos', 'garagens', 'banheiros', 'link', 'dia_hora']
l= zip(*list_of_lists)
zap = {z[0]:list(z[1:]) for z in zip(*list_of_lists)}  

t = pd.DataFrame.from_dict(zap,orient='index')
t.to_csv('teste.csv')


def build_data_dict(convert_ids, situacaor, bairror):
    inputs = zip(convert_ids, situacaor, bairror)
    d = {}
    for convert_ids, situacaor, bairror in inputs:
        d.update({convert_ids : {"Situacao" : situacaor, "Bairro" : bairror}})
    return d




#pprint.pprint((zap))

if verifica_elementos (list_of_lists) != 0:
    #salva o log da roddada de erro   
    FileName = str('Erros '+ url[-19:-10])             
    ErrosFile = open(FileName, 'w', newline='')
    ErrosWriter = csv.writer(ErrosFile)
    for item in linkr:
        ErrosWriter.writerow(zip(convert_ids, dia_horar, linkr))
else:
    #abre o banco de dados de key
    print('Abrindo Banco de Keys: ')
    
    banco_principal_retrieve = pd.read_csv('banco_principal.csv', index_col=0)
    #pd.DataFrame(KeysData, names=fieldnames, header=0)
#    KeysFile = open('banco_principal.csv')
#    KeysReader = csv.reader(KeysFile)    
    Keys_to_list = banco_principal_retrieve["id"].tolist()
    #Keys_to_list = []
    #Keys = Keys_to_list.values
#   # with paginasFile as csv_file:
#    for row in KeysReader:
#      #  print(str(row))
#        KeysData.append(row[0])
# verifica chaves levantadas na rodadas contra keys já existentes
for key in convert_ids:
    #se a chave for nova faz duas coisas 1) salva no banco principal 2) novidades da rodada
    if str(key) not in str(Keys_to_list):
       #Savando no banco principal 
        #banco_principal_retrieve.append(key)
        df = pd.DataFrame(list_of_lists)
        df_transposed = df.T
        df_transposed.columns = fieldnames
     #   df_transposed.to_csv('banco_principal.csv')
        df_transposed.to_csv('novidades.csv')
        
 
#        with open('banco_principal.csv', 'w', newline="") as file:  
#           writer = csv.writer(file)
#           for list in list_of_lists:
#               writer.writerow([list])
     
               

        
        
        
        
        
#        df = pandas.read_csv('banco_principal.csv', 
#            index_col='Id', 
#            parse_dates=['Data'],
#            header=0, 
#            names=['Id', 'Data', 'Salary', 'Sick Days'])
#        df.to_csv('banco_principal.csv_modified.csv')           

#zap2 = build_data_dict(convert_ids, situacaor, bairror)
#pprint.pprint(zap2)
#
#for key in convert_ids:
#    if key not in KeysData:
#        KeysData.append(key)
#        with open('dict.csv', 'w', newline="") as csv_file:  
#            writer = csv.writer(csv_file, delimiter='§')
#            for key, values in zap2.items():
#                  #  writer.writerow(zap.keys())
#                 #   writer.writerow(zap.values())
#               #  writer.writerow(zap.items())
#                writer.writerow(zip(key, values)



