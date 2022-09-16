from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from datetime import datetime

BASE_URL = "https://consultaunificadapje.tse.jus.br/#/public/inicial/index"

def get_data_from_proccess_number(proccess_number):
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(BASE_URL)
    driver.implicitly_wait(0.5)
    driver.maximize_window()

    #chave de pesquisa
    proccess_code = '0602454-85.2022.6.05.0000'
    css_elem = driver.find_element('xpath','//*[@id="mat-input-1"]');
    button = driver.find_element('xpath', '/html/body/app-root/div/app-public/mat-sidenav-container/mat-sidenav-content/div/app-inicial/section/article/div/div/mat-card/mat-card-content/form/span/button[1]/span')

    css_elem.send_keys(proccess_code)
    button.click()

    #captcha básico
    time.sleep(5)
    driver.switch_to.frame(driver.find_element('tag name', "iframe"))
    element = driver.find_element('xpath', '/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]')
    ed = ActionChains(driver)
    ed.move_to_element(element).move_by_offset(1, 1).click().perform()

    driver.switch_to.default_content()
    time.sleep(5)
    #numero do processo
    proccess_number = driver.find_element('xpath', '/html/body/app-root/div/app-public/mat-sidenav-container/mat-sidenav-content/div/app-resultado/mat-tab-group/div/mat-tab-body/div/mat-card[1]/mat-card-content/div[1]/div[1]/p')
    fase_atual = driver.find_element('xpath', '/html/body/app-root/div/app-public/mat-sidenav-container/mat-sidenav-content/div/app-resultado/mat-tab-group/div/mat-tab-body/div/mat-card[1]/mat-card-content/div[1]/div[2]/p')
    orgao_justica = driver.find_element('xpath', '/html/body/app-root/div/app-public/mat-sidenav-container/mat-sidenav-content/div/app-resultado/mat-tab-group/div/mat-tab-body/div/mat-card[1]/mat-card-content/div[1]/div[3]/p')
    origem = driver.find_element('xpath', '/html/body/app-root/div/app-public/mat-sidenav-container/mat-sidenav-content/div/app-resultado/mat-tab-group/div/mat-tab-body/div/mat-card[1]/mat-card-content/div[1]/div[4]/p')
    relator = driver.find_element('xpath', '/html/body/app-root/div/app-public/mat-sidenav-container/mat-sidenav-content/div/app-resultado/mat-tab-group/div/mat-tab-body/div/mat-card[1]/mat-card-content/div[1]/div[5]/p')
    data_autuacao = driver.find_element('xpath', '/html/body/app-root/div/app-public/mat-sidenav-container/mat-sidenav-content/div/app-resultado/mat-tab-group/div/mat-tab-body/div/mat-card[1]/mat-card-content/div[2]/div[1]/p')
    data_ultimo_movimento = driver.find_element('xpath', '/html/body/app-root/div/app-public/mat-sidenav-container/mat-sidenav-content/div/app-resultado/mat-tab-group/div/mat-tab-body/div/mat-card[1]/mat-card-content/div[2]/div[2]/p')
    classe_judicial = driver.find_element('xpath', '/html/body/app-root/div/app-public/mat-sidenav-container/mat-sidenav-content/div/app-resultado/mat-tab-group/div/mat-tab-body/div/mat-card[1]/mat-card-content/div[2]/div[3]/p')
    assunto_principal = driver.find_element('xpath', '/html/body/app-root/div/app-public/mat-sidenav-container/mat-sidenav-content/div/app-resultado/mat-tab-group/div/mat-tab-body/div/mat-card[1]/mat-card-content/div[2]/div[4]/p')
    ano_eleicao = driver.find_element('xpath', '/html/body/app-root/div/app-public/mat-sidenav-container/mat-sidenav-content/div/app-resultado/mat-tab-group/div/mat-tab-body/div/mat-card[1]/mat-card-content/div[2]/div[4]/p')

    output_dict = [
        proccess_number.text,
        fase_atual.text,
        orgao_justica.text,
        origem.text,
        relator.text,
        data_autuacao.text,
        data_ultimo_movimento.text,
        classe_judicial.text,
        assunto_principal.text,
        ano_eleicao.text,
        datetime.now()
    ]
    driver.close()

