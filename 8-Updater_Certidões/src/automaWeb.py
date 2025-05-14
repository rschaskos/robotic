from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime


from time import sleep
from src.readerPDF import ReaderPDF
from src.utils import constructedFilePath

URL = 'https://sit.tce.pr.gov.br/sitListarTransferencias.aspx'


XPATH_TIPO = '//*[@id="ContentPlaceHolder1_ddlTipoCertidao"]'
XPATH_CERTI_BOX = '//*[@id="ContentPlaceHolder1_tbNumeroCertidao"]'
XPATH_EMIT_BOX = '//*[@id="ContentPlaceHolder1_ucdtEmissao_textBoxData"]'
XPATH_VALID_BOX = '//*[@id="ContentPlaceHolder1_ucdtValidade_textBoxData"]'
XPATH_SAVE = '//*[@id="ContentPlaceHolder1_btnNovo"]'
XPATH_INIT = '//*[@id="btlInicioPrincipal"]'

MESES = {'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4, 'maio': 5,
'junho': 6, 'julho': 7, 'agosto': 8, 'setembro': 9,
'outubro': 10, 'novembro': 11, 'dezembro': 12}

t1 = 1.5
t2 = 2
t3 = 3

class TCEPRBot:
    def __init__(self, user, passwd, sitNumber, selectedFiles, url=URL, detach=True):
        self.url = url
        self.user = user
        self.passwd = passwd
        self.sitNumber = sitNumber
        self.selectedFiles = selectedFiles
        self.detach = detach
        self.browser = None
        self._setupChromeOptions()

    def _setupChromeOptions(self):
        self.chromeOptions = Options()
        if self.detach:
            self.chromeOptions.add_experimental_option('detach', True)

    def launchBrowser(self):

        if self.browser is None:
            try:
                serv = Service(ChromeDriverManager().install())
                self.browser = webdriver.Chrome(service=serv, options=self.chromeOptions)
                self.browser.get(self.url)
                self.browser.maximize_window()
                sleep(t1)
                self._login()
            except Exception as e:
                print(f"Erro ao iniciar o navegador: {e}")
                if self.browser:
                    self.browser.quit()
        else:
            print('Navegador já aberto...')

    def _login(self):        
        try:
            self.browser.find_element(By.XPATH, '//*[@id="Login"]').send_keys(self.user)
            sleep(t1)
            self.browser.find_element(By.XPATH, '//*[@id="Senha"]').send_keys(self.passwd)
            sleep(t1)
            self.browser.find_element(By.XPATH, '//*[@id="btnLogin"]').click()
            sleep(t3)
            self._navegate()
        except Exception as e:
            print(f"Erro ao fazer login: {e}")
            self.quit_browser()

    def _navegate(self):
        try:
            self.browser.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_tbidTransferencia"]').send_keys(self.sitNumber)
            sleep(t1)
            self.browser.find_element(By.XPATH, '//*[@id="btPesquisar"]').click()
            sleep(t1)
            self.browser.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_gvListaTransferencias_btnDetalhes_0"]').click()
            sleep(t2)
            self.browser.find_element(By.XPATH, '//*[@id="my_menu"]/div[4]/span').click()
            sleep(t2)
            self.browser.find_element(By.XPATH, '//*[@id="lsTomador_hlItem_1"]').click()
            sleep(t1)
            self.certificateSelection(self.selectedFiles)
            
        except Exception as e:
            print(f'Elemento não encontrado: {e}')
            self.quit_browser()


    def certificateSelection(self, selectedFiles):
        numSelected = len(selectedFiles)
        processedCount = 0

        if 'fgts.pdf' in selectedFiles:
            pdfPathFgts = constructedFilePath('fgts.pdf')
            readerFGTS = ReaderPDF(pdfPathFgts)
            self.browser.find_element(By.XPATH, XPATH_TIPO + '/option[8]').click()
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).send_keys(readerFGTS.certiNumberFGTS)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).send_keys(readerFGTS.emitDateFGTS)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_VALID_BOX).send_keys(readerFGTS.finalValidFGTS)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_SAVE).click()
            sleep(t2)
            alert = self.browser.switch_to.alert
            alert.accept()
            sleep(t2)
            processedCount += 1
            if processedCount == numSelected:
                self.browser.find_element(By.XPATH, XPATH_INIT).click()
                sleep(t2)

        if 'estadual.pdf' in selectedFiles:
            pdfPathEstadual = constructedFilePath('estadual.pdf')
            readerESTADUAL = ReaderPDF(pdfPathEstadual)
            self.browser.find_element(By.XPATH, XPATH_TIPO + '/option[3]').click()
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).send_keys(readerESTADUAL.certiNumberESTADUAL)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).send_keys(readerESTADUAL.emitDateESTADUAL)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_VALID_BOX).send_keys(readerESTADUAL.finalValidESTADUAL)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_SAVE).click()
            sleep(t3)
            alert = self.browser.switch_to.alert
            alert.accept()
            sleep(t2)
            processedCount += 1
            if processedCount == numSelected:
                self.browser.find_element(By.XPATH, XPATH_INIT).click()
                sleep(t2)

        
        if 'tce.pdf' in selectedFiles:
            pdfPathTce = constructedFilePath('tce.pdf')
            readerTCE = ReaderPDF(pdfPathTce)
            self.browser.find_element(By.XPATH, XPATH_TIPO + '/option[5]').click()
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).send_keys(readerTCE.certiNumberTCE)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).send_keys(readerTCE.emitDateTCE)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_VALID_BOX).send_keys(readerTCE.finalValidTCE)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_SAVE).click()
            sleep(t3)
            alert = self.browser.switch_to.alert
            alert.accept()
            sleep(t2)
            processedCount += 1
            if processedCount == numSelected:
                self.browser.find_element(By.XPATH, XPATH_INIT).click()
                sleep(t2)

        if 'trabalhista.pdf' in selectedFiles:
            pdfPathTrabalhista = constructedFilePath('trabalhista.pdf')
            readerTRABALHISTA = ReaderPDF(pdfPathTrabalhista)
            self.browser.find_element(By.XPATH, XPATH_TIPO + '/option[6]').click()
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).send_keys(readerTRABALHISTA.certiNumberTRABALHISTA)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).send_keys(readerTRABALHISTA.emitDateTRABALHISTA)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_VALID_BOX).send_keys(readerTRABALHISTA.finalValidTRABALHISTA)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_SAVE).click()
            sleep(t3)
            alert = self.browser.switch_to.alert
            alert.accept()
            sleep(t2)
            processedCount += 1
            if processedCount == numSelected:
                self.browser.find_element(By.XPATH, XPATH_INIT).click()
                sleep(t2)

        
        if 'federal.pdf' in selectedFiles:
            pdfPathFederal = constructedFilePath('federal.pdf')
            readerFEDERAL = ReaderPDF(pdfPathFederal)
            self.browser.find_element(By.XPATH, XPATH_TIPO + '/option[9]').click()
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).send_keys(readerFEDERAL.certiNumberFEDERAL)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).send_keys(readerFEDERAL.emitDateFEDERAL)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_VALID_BOX).send_keys(readerFEDERAL.finalValidFEDERAL)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_SAVE).click()
            sleep(t3)
            alert = self.browser.switch_to.alert
            alert.accept()
            sleep(t2)
            processedCount += 1
            if processedCount == numSelected:
                self.browser.find_element(By.XPATH, XPATH_INIT).click()
                sleep(t2)

        if 'municipal.pdf' in selectedFiles:
            pdfPathMunicipal = constructedFilePath('municipal.pdf')
            readerMUNICIPAL = ReaderPDF(pdfPathMunicipal)
            self.browser.find_element(By.XPATH, XPATH_TIPO + '/option[2]').click()
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).send_keys(readerMUNICIPAL.certiNumberMUNICIPAL)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).send_keys(readerMUNICIPAL.emitDateMUNICIPAL)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_VALID_BOX).send_keys(readerMUNICIPAL.finalValidMUNICIPAL)
            sleep(t1)
            self.browser.find_element(By.XPATH, XPATH_SAVE).click()
            sleep(t3)
            alert = self.browser.switch_to.alert
            alert.accept()
            sleep(t2)
            processedCount += 1
            if processedCount == numSelected:
                self.browser.find_element(By.XPATH, XPATH_INIT).click()
                sleep(t2)


    def quit_browser(self):
        if self.browser:
            self.browser.quit()

def getSitNumber():
    return input('Nº SIT: ')

# def dateConverter(data_str):
#     dia, mes_nome, ano = data_str.lower().split(' de ')
#     mes = MESES[mes_nome]
#     data = datetime(int(ano), mes, int(dia))
#     return data.strftime("%d/%m/%Y")