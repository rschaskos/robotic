#########################################
#   DESENVOLVIDO POR RSCHASKOS EM 2024  #
#########################################

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import pyautogui as pag

noauth = 'http://serverwebapp.sysmar.com.br:8138/frota/servlet/hnotauthorized'
main = 'http://serverwebapp.sysmar.com.br:8138/frota/servlet/hfro_rman'
login = input('Digite seu usuário: ')
login_str = str(login)
senha = input('Digite sua senha: ')
senha_str = str(senha)
of = [6908, 6964, 6961, 5129, 4755]

# Essa função permite que o Chrome fique aberto mesmo após encerrar o código
chome_options = Options()
chome_options.add_experimental_option('detach', True)


# Abre o navegador
def acessar():
    global browser
    global current
    browser = webdriver.Chrome(options=chome_options)

    # login
    browser.get(noauth)
    current = browser.current_window_handle # usada para obter o identificador (ID) da janela atual
    browser.find_element('xpath', '//*[@id="TABLE1"]/tbody/tr[3]/td/span/span/span/span/input').click()
    browser.maximize_window()
    sleep(1)
    browser.find_element('xpath',
                         '//*[@id="vUSULOGIN"]').send_keys(login_str)
    sleep(1)
    browser.find_element('xpath',
                         '//*[@id="vUSUSENHA"]').send_keys(senha_str)
    sleep(1)
    browser.find_element('xpath',
                         '//*[@id="TABLE"]/tbody/tr[3]/td/input').click()
    sleep(1)

    # acessa relatório
    browser.get(main)
    sleep(1)

acessar()


def relatorio():
    dataini = str(input('Digite a data inicial: ')).strip().replace('/', '')
    datafin = str(input('Digite a data final: ')).strip().replace('/', '')

    # acessa relatório
    browser.get(main)
    sleep(1)

    for c in range(5):
        # insere oficina
        browser.find_element('xpath', '//*[@id="vOFCPESCODINI"]').click()
        browser.find_element('xpath', '//*[@id="vOFCPESCODINI"]').send_keys(of[c])
        browser.find_element('xpath', '//*[@id="vOFCPESCODFIN"]').click()
        browser.find_element('xpath', '//*[@id="vOFCPESCODFIN"]').send_keys(of[c])

        # insere data
        browser.find_element('xpath', '//*[@id="vDATAMANINI"]').click()
        browser.find_element('xpath', '//*[@id="vDATAMANINI"]').send_keys(dataini)
        browser.find_element('xpath', '//*[@id="vDATAMANFIN"]').click()
        browser.find_element('xpath', '//*[@id="vDATAMANFIN"]').send_keys(datafin)
        sleep(0.5)
        browser.find_element('xpath', '//*[@id="TABLE1"]/tbody/tr[4]/td/span/span/span/span/input').click()
        sleep(1)

        # volta aba inicial
        browser.switch_to.window(current)

relatorio()
