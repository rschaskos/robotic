import PyPDF2
import re
import csv
import os
from pathlib import Path
from time import sleep

downloads_path = Path.home() / "Downloads"
FILE_PATH_GAS = downloads_path / "gasolina.pdf"
FILE_PATH_DIE = downloads_path / "diesel.pdf"

def iniciar():
    print('Iniciando', end='')
    for c in range(3):
        print('.', end='')
        sleep(0.5)

def limpar():
    os.system('cls')

def pdf_gasolina():
    try:
        with open(FILE_PATH_GAS, 'rb') as pdf:
            leitor_pdf = PyPDF2.PdfReader(pdf)
            texto = ''
            for c in leitor_pdf.pages:
                texto += c.extract_text()
            with open('gasolina.txt', 'a', encoding='UTF-8') as out:
                out.write(texto)
        limpar()
        print('Conversão realizada com sucesso!')
    except FileNotFoundError:
        limpar()
        print('Arquivo "gasolina.pdf" não localizado')
        exit()

def pdf_diesel():
    try:
        with open(FILE_PATH_DIE, 'rb') as pdf:
            leitor_pdf = PyPDF2.PdfReader(pdf)
            texto = ''
            for c in leitor_pdf.pages:
                texto += c.extract_text()
            with open('diesel.txt', 'a', encoding='UTF-8') as out:
                out.write(texto)
        limpar()
        print('Conversão realizada com sucesso!')
    except FileNotFoundError:
        limpar()
        print('Arquivo "diesel.pdf" não localizado')
        exit()

def processar_relatorio_gasolina(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Expressões regulares para identificar as linhas
    cupom_pattern = re.compile(r'Cupom Fiscal Nº(\d+) Série: (\d+) Data: (\d{2}/\d{2}/\d{4}) Valor: ((?:\d{1,3}\.)*\d{1,3},\d{2})')
    gasolina_pattern = re.compile(r'(\d+) GASOLINA (\d+) (\d) (\d) (\d+,\d{4}) (\d+,\d{4}) (\d+,\d{4}) ((?:\d{1,3}\.)*\d{1,3},\d{2})')
    liquidacao_empenho_pattern = re.compile(r'(\d{5}/\d{4}) (\d{4}/\d{4})')

    # Lista para armazenar os dados combinados
    dados_combinados = []

    liquidacao = None
    empenho = None

    for i in range(len(lines)):
        liquidacao_empenho_match = liquidacao_empenho_pattern.search(lines[i])
        if liquidacao_empenho_match:
            liquidacao = liquidacao_empenho_match.group(1)
            empenho = liquidacao_empenho_match.group(2)

        cupom_match = cupom_pattern.match(lines[i])
        if cupom_match:
            for j in range(i + 1, len(lines)):
                gasolina_match = gasolina_pattern.match(lines[j])
                if gasolina_match and cupom_match.group(4) == gasolina_match.group(8):
                    dados_combinados.append([
                        liquidacao, empenho,
                        cupom_match.group(1), cupom_match.group(2), cupom_match.group(3), cupom_match.group(4),
                        gasolina_match.group(1), gasolina_match.group(2), gasolina_match.group(3), gasolina_match.group(4),
                        gasolina_match.group(5), gasolina_match.group(6), gasolina_match.group(7), gasolina_match.group(8)
                    ])
                    break

    # Verificar se há dados combinados antes de escrever no arquivo CSV
    if dados_combinados:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([
                'Liquidacao', 'Empenho', 'Cupom No', 'Serie', 'Data', 'Valor', 'Item', 'Produto', 'Lote', 'Operacao',
                'Quantidade', 'Valor unitario', 'Desconto', 'Valor total'
            ])
            csvwriter.writerows(dados_combinados)
    
        print('Sucesso na gravação do relatório!')

    else:
        print("Nenhum dado encontrado para gravar no arquivo CSV.")    

def processar_relatorio_diesel(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Expressões regulares para identificar as linhas
    cupom_pattern = re.compile(r'Cupom Fiscal Nº(\d+) Série: (\d+) Data: (\d{2}/\d{2}/\d{4}) Valor: ((?:\d{1,3}\.)*\d{1,3},\d{2})')
    diesel_pattern = re.compile(r'(\d+) (DIESEL S\d+) (\d+) (\d) (\d) ((?:\d{1,3}\.)*\d{1,3},\d{4}) (\d+,\d{4}) (\d+,\d{4}) ((?:\d{1,3}\.)*\d{1,3},\d{2})')
    liquidacao_empenho_pattern = re.compile(r'(\d{5}/\d{4}) (\d{4}/\d{4})')

    # Lista para armazenar os dados combinados
    dados_combinados = []

    liquidacao = None
    empenho = None

    for i in range(len(lines)):
        liquidacao_empenho_match = liquidacao_empenho_pattern.search(lines[i])
        if liquidacao_empenho_match:
            liquidacao = liquidacao_empenho_match.group(1)
            empenho = liquidacao_empenho_match.group(2)

        cupom_match = cupom_pattern.match(lines[i])
        if cupom_match:
            for j in range(i + 1, len(lines)):
                diesel_match = diesel_pattern.match(lines[j])
                if diesel_match and cupom_match.group(4) == diesel_match.group(9):
                    dados_combinados.append([
                        liquidacao, empenho,
                        cupom_match.group(1), cupom_match.group(2), cupom_match.group(3), cupom_match.group(4),
                        diesel_match.group(1), diesel_match.group(2), diesel_match.group(3), diesel_match.group(4),
                        diesel_match.group(5), diesel_match.group(6), diesel_match.group(7), diesel_match.group(8),
                        diesel_match.group(9)
                    ])
                    break

    # Verificar se há dados combinados antes de escrever no arquivo CSV
    if dados_combinados:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([
                'Liquidacao', 'Empenho', 'Cupom No', 'Serie', 'Data', 'Valor', 'Codigo', 'Produto', 'Operacao', 'Lote',
                'Item', 'Quantidade', 'Valor Unitario', 'Desconto', 'Valor Total'
            ])
            csvwriter.writerows(dados_combinados)

        print('Sucesso na gravação do relatório!')

    else:
        print("Nenhum dado encontrado para gravar no arquivo CSV.")
    
while True:
    print('\nEscolha qual relatório quer gerar')
    print('''
        1) Gasolina
        2) Diesel
        3) Sair''')

    user = input('\nDigite sua escolha: ')

    if user == '1':
        limpar()
        iniciar()
        pdf_gasolina()
        processar_relatorio_gasolina('gasolina.txt', 'gasolina.csv')
    elif user == '2':
        limpar()
        iniciar()
        pdf_diesel()
        processar_relatorio_diesel('diesel.txt', 'diesel.csv')
    elif user == '3':
        limpar()
        print('Até mais!')
        break
    else:
        limpar()
        print('Opção inválida! Tente novamente')
        