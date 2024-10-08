import csv
import os
from xml.dom import minidom

head = ['Empresa', 'N da NF', 'Data Emissao',
        'Codigo do Produto', 'Nome do Produto', 'Qtde do Produto',
        'Valor Unitario do Produto', 'Valor do Produto',
        'Valor de Desconto']

with open('excel.csv', 'w', newline='', encoding='utf-8') as output:
    writer = csv.writer(output, delimiter=';')
    writer.writerow(head)

local = r'C:\Users\roney.schaskos\iCloudDrive\Cursos\Python\robotic\automatic\6-NFe_XML'

for filename in os.listdir(local):
    if filename.endswith('.xml'):
        filepath = os.path.join(local, filename)
        with open(filepath) as nfe:
            nfe = minidom.parse(nfe)

            cnpj_emit = nfe.getElementsByTagName('emit')[0].getElementsByTagName('xNome')[0].firstChild.data
            num_nfe = nfe.getElementsByTagName('nNF')[0].firstChild.data
            data_nfe = nfe.getElementsByTagName('ide')[0].getElementsByTagName('dhEmi')[0].firstChild.data[:10]

            det_elements = nfe.getElementsByTagName('det')

            with open('excel.csv', 'a', newline='', encoding='utf-8') as output:
                writer = csv.writer(output, delimiter=';')

                for det in det_elements:
                    prod = det.getElementsByTagName('prod')[0]
                    cProd = prod.getElementsByTagName('cProd')[0].firstChild.data
                    xProd = prod.getElementsByTagName('xProd')[0].firstChild.data
                    qProd = prod.getElementsByTagName('qCom')[0].firstChild.data
                    vUnProd = prod.getElementsByTagName('vUnCom')[0].firstChild.data
                    vProd = prod.getElementsByTagName('vProd')[0].firstChild.data
                    vDesc_elements = prod.getElementsByTagName('vDesc')
                    vDesc = vDesc_elements[0].firstChild.data if vDesc_elements else '0.00'

                    # Escrever os dados no CSV
                    writer.writerow([cnpj_emit, num_nfe, data_nfe, cProd, xProd, qProd, vUnProd, vProd, vDesc])

