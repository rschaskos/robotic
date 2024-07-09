#########################################
#   DESENVOLVIDO POR RSCHASKOS EM 2024  #
#########################################

import requests
import json
from time import sleep

cont = 0

def existeArquivo(nome):
    try:
        a = open(nome, 'rt')
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True

existe = False
while existe != True:
    nome = str(input('NOME DO ARQUIVO COM EXTENSAO (ex.: cnpj.txt): ')).strip()
    if not existeArquivo(nome):
        print('Arquivo não encontrado')
    else:
        existe = True
sep = str(input('SEPARADOR DO ARQUIVO (ex.: , | ;): ')).strip()

# Função criada para saber tamamho aproximado do relatório
def calcula_tempo():
    with open(nome, 'r') as arquivo:
        size = len(arquivo.readlines())
        print(f'Tempo aproximado para o relatório: {size / 3:.0f}min.')
        input('Pressione ENTER para continuar')
calcula_tempo()
lista = ['nome', 'fantasia', 'cnpj', 'logradouro',
         'numero', 'municipio', 'bairro', 'uf',
         'cep', 'email', 'situacao']

# leitura do arquivo e gravação do .csv
with open('excel.csv', 'a', newline='', encoding='utf-8') as txt:
    with open('cnpjs.txt', 'r') as arquivo:
        # cabeçalho
        for c in lista:
            txt.write(c + ';')
        txt.write('\n')
        for linha in arquivo:
            cnpj = linha.split(sep)[0]
            cont += 1
            url = (f'https://www.receitaws.com.br/v1/cnpj/{cnpj}/')
            req = requests.get(url)
            resp = json.loads(req.text)
            lista = (resp['nome'], resp['fantasia'], resp['cnpj'], resp['logradouro'],
                     resp['numero'], resp['municipio'], resp['bairro'], resp['uf'],
                     resp['cep'], resp['email'], resp['situacao'])
            for c in lista:
                txt.write(c + ';')
            txt.write('\n')
            print(resp['nome'])
            if cont == 3:
                for c in range(60, 0, -1):
                    print(f'Aguarde...{c}s')
                    sleep(1)
                cont = 0

