import csv
import os
from xml.dom import minidom

head = ['Empresa', 'N da NF', 'Data Emissao',
        'Codigo do Produto', 'Nome do Produto', 'Qtde do Produto',
        'Valor Unitario do Produto', 'Valor do Produto',
        'Valor de Desconto']

LOCAL = r'C:\Users\seu_usuario\Downloads\XML'
CSV_PATH = os.path.join(LOCAL, 'excel.csv')

with open(CSV_PATH, 'w', newline='', encoding='utf-8') as output:
    writer = csv.writer(output, delimiter=';')
    writer.writerow(head)

for filename in os.listdir(LOCAL):
    if filename.endswith('.xml'):
        filepath = os.path.join(LOCAL, filename)
        with open(filepath) as nfe:
            nfe = minidom.parse(nfe)

            cnpj_emit = nfe.getElementsByTagName('emit')[0].getElementsByTagName('xNome')[0].firstChild.data
            num_nfe = nfe.getElementsByTagName('nNF')[0].firstChild.data
            data_nfe = nfe.getElementsByTagName('ide')[0].getElementsByTagName('dhEmi')[0].firstChild.data[:10]

            det_elements = nfe.getElementsByTagName('det')

            with open(CSV_PATH, 'a', newline='', encoding='utf-8') as output:
                writer = csv.writer(output, delimiter=';')

                for det in det_elements:
                    prod = det.getElementsByTagName('prod')[0]
                    cProd = prod.getElementsByTagName('cProd')[0].firstChild.data
                    xProd = prod.getElementsByTagName('xProd')[0].firstChild.data
                    qProd = prod.getElementsByTagName('qCom')[0].firstChild.data
                    qProd_split = qProd.split('.')[0]
                    vUnProd = prod.getElementsByTagName('vUnCom')[0].firstChild.data
                    vUnProd_split = vUnProd.split('.')[0]
                    vProd = prod.getElementsByTagName('vProd')[0].firstChild.data
                    vProd_split = vProd.split('.')[0]
                    vDesc_elements = prod.getElementsByTagName('vDesc')
                    vDesc = vDesc_elements[0].firstChild.data if vDesc_elements else '0.00'

                    # Escrever os dados no CSV
                    writer.writerow([cnpj_emit, num_nfe, data_nfe, cProd, xProd, qProd_split, vUnProd_split, vProd_split, vDesc])
                    print(cnpj_emit, num_nfe, data_nfe, cProd, xProd, qProd, vUnProd, vProd)
print(f'\nSALVO NO LOCAL: {CSV_PATH}')
print('SEU RELATÓRIO FOI CONCLUÍDO COM SUCESSO')
print()
