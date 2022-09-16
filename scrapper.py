from re import S, T
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, pickle 
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from datetime import datetime
from dotenv import load_dotenv
import os, re
from pprint import pprint
from tinydb import TinyDB, Query
import random
from pickle_gen import init_query_list
pattern = r'[^A-Za-z0-9]+'


class PjeScrapper():
    def get_data_from_proccess_number(self, proccess_number):
        load_dotenv()
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        self.driver.implicitly_wait(600)
        #  entra no url base
        self.driver.get(os.environ.get('BASE_URL'))
        #self.driver.maximize_window()

        # ETAPA 1 - INSERÇÃO DE NUMERO PROCESSO

        #  insere chave de busca no campo de n processo
        key_input_elem = self.driver.find_element('xpath', os.environ.get('PROCCESS_NUMBER_FIELD'))
        key_input_elem.send_keys(proccess_number)

        #  clica no botão
        query_button = self.driver.find_element('xpath', os.environ.get('QUERY_BUTTON'))
        query_button.click()

        # ETAPA 3 - EXTRAÇÃO DE DADOS

        fetched_data = {
            "proccess_number": self.driver.find_element('xpath', os.environ.get('PROCCESS_NUMBER')).get_attribute('textContent'),
            "fase_atual": self.driver.find_element('xpath', os.environ.get('FASE_ATUAL')).get_attribute('textContent'),
            "orgao_justica": self.driver.find_element('xpath', os.environ.get('ORGAO_JUSTICA')).get_attribute('textContent'),
            "origem": self.driver.find_element('xpath', os.environ.get('ORIGEM')).get_attribute('textContent'),
            "relator": self.driver.find_element('xpath', os.environ.get('RELATOR')).get_attribute('textContent'),
            "data_autuacao": self.driver.find_element('xpath', os.environ.get('DATA_AUTUACAO')).get_attribute('textContent'),
            "data_ultimo_movimento": self.driver.find_element('xpath', os.environ.get('DATA_ULTIMO_MOVIMENTO')).get_attribute('textContent'),
            "classe_judicial": self.driver.find_element('xpath', os.environ.get('CLASSE_JUDICIAL')).get_attribute('textContent'),
            "assunto_principal": self.driver.find_element('xpath', os.environ.get('ASSUNTO_PRINCIPAL')).get_attribute('textContent'),
            "ano_eleicao":  self.driver.find_element('xpath', os.environ.get('ANO_ELEICAO')).get_attribute('textContent'),
        }

        self.driver.close()
        return fetched_data

if __name__ == "__main__":
    init_query_list()
    scrapper = PjeScrapper()
    db = TinyDB('processos.db')
    #carrega todas as chaves de busca
    file = open('keys_list.p', 'rb')
    keys = pickle.load(file)
    random.shuffle(keys)
    file.close()
    print("faltam", len(keys))
    for key in keys:
        try:
            #filtered_key = re.sub(pattern, '', key)
            output = scrapper.get_data_from_proccess_number(key)
            if output['proccess_number'] == '':
                print("algo ocorreu.")
                continue
            db.insert(output)
            print(f'Success! {output["proccess_number"]}')
        except Exception as e:
            raise e 

            #time.sleep(225)
            continue 
        #time.sleep(225)

    
