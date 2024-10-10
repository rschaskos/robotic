#########################################
#   DESENVOLVIDO POR RSCHASKOS EM 2024  #
#########################################

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import pyautogui as pag

TIME = 15

URL = 'https://servicos.pf.gov.br/epol-sinic-publico/'

chome_options = Options()
chome_options.add_experimental_option('detach', True)

browser = webdriver.Chrome(options=chome_options)
browser.get(URL)
current = browser.current_window_handle

with open('nomes.txt', 'rt') as file:
    for c in (file):
        b = c.split('|')
        print(b[1])
        browser.maximize_window()
        browser.find_element('xpath', '//*[@id="p-card-dados-gerais"]/div/div/div/div[2]/div[1]/pf-input-cpf/span/p-inputmask/input').click()
        browser.find_element('xpath', '//*[@id="p-card-dados-gerais"]/div/div/div/div[2]/div[1]/pf-input-cpf/span/p-inputmask/input').clear()
        browser.find_element('xpath', '//*[@id="p-card-dados-gerais"]/div/div/div/div[2]/div[1]/pf-input-cpf/span/p-inputmask/input').send_keys(b[0])

        browser.find_element('xpath', '//*[@id="p-card-dados-gerais"]/div/div/div/div[2]/div[2]/input').click()
        browser.find_element('xpath', '//*[@id="p-card-dados-gerais"]/div/div/div/div[2]/div[2]/input').clear()
        browser.find_element('xpath', '//*[@id="p-card-dados-gerais"]/div/div/div/div[2]/div[2]/input').send_keys(b[1])

        browser.find_element('xpath', '//*[@id="p-card-dados-gerais"]/div/div/div/div[3]/div[1]/pf-calendar/span/input').click()
        browser.find_element('xpath', '//*[@id="p-card-dados-gerais"]/div/div/div/div[3]/div[1]/pf-calendar/span/input').send_keys(b[2])

        browser.find_element('xpath', '//*[@id="p-card-dados-gerais"]/div/div/div/div[4]/div[2]/input').click()
        browser.find_element('xpath', '//*[@id="p-card-dados-gerais"]/div/div/div/div[4]/div[2]/input').clear()
        browser.find_element('xpath', '//*[@id="p-card-dados-gerais"]/div/div/div/div[4]/div[2]/input').send_keys(b[3])

        browser.find_element('xpath', '//*[@id="p-card-dados-gerais"]/div/div/div/div[4]/div[3]/input').click()
        browser.find_element('xpath', '//*[@id="p-card-dados-gerais"]/div/div/div/div[4]/div[3]/input').clear()
        browser.find_element('xpath', '//*[@id="p-card-dados-gerais"]/div/div/div/div[4]/div[3]/input').send_keys(b[4])

        browser.find_element('xpath', '//*[@id="btn-emitir-cac"]').click()
        sleep(3)
        pag.click(804, 560)
        input('Resolva o Captcha (caso necessário) ou pressione enter p/ continuar!')
        pag.click(1010, 682)
        input('Pressione enter após nova janela!')

        browser.switch_to.window(current)
        browser.find_element('xpath', '//*[@id="btn-limpar"]').click()
        sleep(0.5)
