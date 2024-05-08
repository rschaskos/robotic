#########################################
#   DESENVOLVIDO POR RSCHASKOS EM 2024  #
#########################################

import pyautogui as pag
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime
from pygetwindow import PyGetWindowException
from selenium.common.exceptions import NoSuchElementException
import customtkinter as ctk

url = ['https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf',
       'http://www.cdw.fazenda.pr.gov.br/cdw/emissao/certidaoAutomatica',
       'https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PJ/Consultar',
       'https://www.tst.jus.br/certidao1',
       'https://www8.receita.fazenda.gov.br/simplesnacional/aplicacoes.aspx?id=21']

version = 2.0

# Essa função permite que o Chrome fique aberto mesmo após encerrar o código
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)


# def leia_cnpj():
#     global cnpj
#     cabecalho('DEFINA O CNPJ DA BUSCA')
#     while True:
#         try:
#             cnpj = str(input('Digite o CNPJ desejado p/ consulta: '))
#             if len(cnpj) < 14 or len(cnpj) > 14:
#                 print('Possível CNPJ errado')
#             else:
#                 break
#         except KeyboardInterrupt:
#             print()
#             print('Usuario encerrou')
#             exit()

def leia_cnpj():
    global app
    app = ctk.CTk()
    app.title('Desenvolvido em Python')
    app.geometry('400x100')

    # Criação do campo de entrada para a opção
    global option_entry
    option_entry = ctk.CTkEntry(app, placeholder_text='Digite o CNPJ')
    option_entry.pack(pady=30)

    # Configuração para chamar a função quando a tecla "Enter" for pressionada
    option_entry.bind('<Return>', handle_option_entry)

    # Execução da aplicação
    app.mainloop()


def handle_option_entry(event=None):
    global cnpj
    cnpj = option_entry.get()
    while True:
        try:
            if len(cnpj) < 14:
                print(f'CNPJ inválido: {cnpj}')
                app.destroy()
                leia_cnpj()
            else:
                print(f'A opção inserida foi: {cnpj}')
                app.destroy()
                break
        except KeyboardInterrupt:
            print()
            print('Usuario encerrou')
            exit()


def leia_int(info):
    while True:
        try:
            n = int(input(info))
        except (ValueError, TypeError):
            print('Dado inválido')
        except KeyboardInterrupt:
            print()
            print('Usuário encerrou.')
            exit()
        else:
            return n
        

def linha(tam=30):
    return '-' * tam


def cabecalho(msg):
    print(linha())
    print(msg.center(30))
    print(linha())


def menu(lista):
    c = 1
    cabecalho('M E N U')
    for item in lista:
        print(f'{c} - {item}')
        c += 1
    print(linha())
    p = leia_int('Escolha: ')
    print(linha())
    return p


def captcha():
    global cap
    cap = str(input('Digite o Captcha: ')).strip()


def fgts():
    global browser
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()
    browser.get(url[0])
    sleep(3)
    browser.find_element('xpath', '//*[@id="mainForm:txtInscricao1"]').click()
    browser.find_element('xpath', '//*[@id="mainForm:txtInscricao1"]').send_keys(cnpj)
    captcha()
    browser.find_element('xpath', '//*[@id="mainForm:txtCaptcha"]').click()
    sleep(1)
    browser.find_element('xpath', '//*[@id="mainForm:txtCaptcha"]').send_keys(cap)
    sleep(1)
    browser.find_element('xpath', '//*[@id="mainForm:btnConsultar"]').click()
    sleep(2)
    while True:
        try:
            browser.find_element('xpath', '//*[@id="mainForm"]/div[1]/span')
            print('CAPTCHA INVÁLIDO')
            sleep(1)
            browser.get(url[0])
            sleep(3)
            browser.find_element('xpath', '//*[@id="mainForm:txtInscricao1"]').click()
            browser.find_element('xpath', '//*[@id="mainForm:txtInscricao1"]').send_keys(cnpj)
            captcha()
            browser.find_element('xpath', '//*[@id="mainForm:txtCaptcha"]').click()
            sleep(1)
            browser.find_element('xpath', '//*[@id="mainForm:txtCaptcha"]').send_keys(cap)
            sleep(1)
            browser.find_element('xpath', '//*[@id="mainForm:btnConsultar"]').click()
            sleep(2)
        except NoSuchElementException:
            razao = browser.find_element('xpath', '//*[@id="mainForm"]/div[3]/p/span[2]').text
            sleep(1)
            browser.find_element('xpath', '//*[@id="mainForm:j_id51"]').click()
            sleep(1)
            browser.find_element('xpath', '//*[@id="mainForm:btnVisualizar"]').click()
            sleep(2)
            while True:
                try:
                    pag.getWindowsWithTitle('Consulta Regularidade do Empregador')[0].activate()
                    break
                except PyGetWindowException:
                    print('Clique na Janela do FGTS')
                    sleep(1)
            sleep(1)
            pag.keyDown('ctrl')
            pag.press('p')
            pag.keyUp('ctrl')
            sleep(1)
            pag.press('enter')
            sleep(2)
            pag.write('FGTS ' + razao)
            sleep(1)
            pag.press('enter')
            break


def estadual():
    global browser
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()
    browser.get(url[1])
    browser.find_element('xpath', '//*[@id="EmissaoCnpj"]').click()
    browser.find_element('xpath', '//*[@id="EmissaoCnpj"]').send_keys(cnpj)
    browser.find_element('xpath', '//*[@id="submitBtn"]').click()
    sleep(4)
    while True:
        try:
            pag.getWindowsWithTitle('Secretaria da Fazenda')[0].activate()
            break
        except PyGetWindowException:
            print('Clique na Janela do Certidão')
            sleep(1)
    try:
        browser.find_element('xpath', '//*[@id="msg"]/table/tbody/tr/td[2]/div')
        print('ALGUM PROBLEMA COM O CNPJ. VERIFICAR COM O FORNECEDOR')
        sleep(3)
    except NoSuchElementException:
        sleep(4)
        browser.find_element('xpath', '//*[@id="pdf"]/table/tbody/tr/td[2]/div/b/a').click()


def federal():
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(url[2])
    sleep(4)
    while True:
        try:
            pag.getWindowsWithTitle('Certidão de Débitos')[0].activate()
            break
        except PyGetWindowException:
            print('Clique na Janela da Certidão')
            sleep(1)
    pag.press('tab')
    sleep(0.5)
    pag.write(cnpj)
    sleep(1)
    hoje = datetime.today()
    hoje_brasil = hoje.strftime('%d%m%Y')
    pag.write('01012024')
    sleep(0.5)
    pag.write(hoje_brasil)
    sleep(0.5)
    pag.press('enter')
    sleep(2)
    for c in range(32):
        pag.press('tab')
    sleep(0.5)
    pag.press('enter')


def trabalhista():
    global browser
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()
    browser.get(url[3])
    browser.find_element('xpath',
                         '//*[@id="portlet_com_liferay_journal_content_web_portlet_JournalContentPortlet_INSTANCE_Wu3q"]/div/div[2]/div/div/div/p/div/p/a').click()
    sleep(1)
    browser.get(url[3])
    sleep(1)
    browser.get(url[3])
    sleep(1)
    while True:
        try:
            pag.getWindowsWithTitle('Certidão Negativa de Débitos')[0].activate()
            break
        except PyGetWindowException:
            print('Clique na Janela do Certidão')
            sleep(1)
    sleep(1)
    browser.get('https://cndt-certidao.tst.jus.br/gerarCertidao.faces')
    sleep(2)
    browser.find_element('xpath', '//*[@id="gerarCertidaoForm:cpfCnpj"]').click()
    browser.find_element('xpath', '//*[@id="gerarCertidaoForm:cpfCnpj"]').send_keys(cnpj)
    captcha()
    browser.find_element('xpath', '//*[@id="idCampoResposta"]').click()
    browser.find_element('xpath', '//*[@id="idCampoResposta"]').send_keys(cap)
    sleep(2)
    browser.find_element('xpath', '//*[@id="gerarCertidaoForm:btnEmitirCertidao"]').click()
    sleep(1)
    while True:
        try:
            browser.find_element('xpath', '//*[@id="mensagens"]/ul/li')
            print('CAPTCHA INVÁLIDO')
            sleep(1)
            browser.get('https://cndt-certidao.tst.jus.br/gerarCertidao.faces')
            sleep(2)
            browser.find_element('xpath', '//*[@id="gerarCertidaoForm:cpfCnpj"]').click()
            browser.find_element('xpath', '//*[@id="gerarCertidaoForm:cpfCnpj"]').send_keys(cnpj)
            captcha()
            browser.find_element('xpath', '//*[@id="idCampoResposta"]').click()
            browser.find_element('xpath', '//*[@id="idCampoResposta"]').send_keys(cap)
            sleep(2)
            browser.find_element('xpath', '//*[@id="gerarCertidaoForm:btnEmitirCertidao"]').click()
            sleep(1)
        except NoSuchElementException:
            sleep(2)
            print('Certidão geradada com sucesso!')
            break


def simples():
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(url[4])
    sleep(4)
    while True:
        try:
            pag.getWindowsWithTitle('Simples Nacional')[0].activate()
            break
        except PyGetWindowException:
            print('Clique na Janela do Certidão')
            sleep(1)
    sleep(1)
    for c in range(7):
        pag.press('tab')
        sleep(0.3)
    pag.write(cnpj)
    pag.press('enter')
    sleep(1)
    sleep(1)
    for c in range(3):
        pag.press('tab')
        sleep(0.3)
    pag.press('enter')

if __name__ == '__main__':
    leia_cnpj()
while True:
    user = menu(['FGTS', 'ESTADUAL', 'RECEITA FEDERAL', 'TRABALHISTA', 'SIMPLES NACIONAL', 'TROCAR CNPJ', 'GERAR TODAS', 'ENCERRAR'])
    if user == 1:
        fgts()
    elif user == 2:
        estadual()
    elif user == 3:
        federal()
    elif user == 4:
        trabalhista()
    elif user == 5:
        simples()
    elif user == 6:
        leia_cnpj()
    elif user == 7:
        fgts()
        sleep(3)
        estadual()
        sleep(3)
        federal()
        sleep(3)
        trabalhista()
        sleep(3)
        simples()
    elif user == 8:
        print('Até logo!')
        exit()
    else:
        print('Não existe essa opção.')
