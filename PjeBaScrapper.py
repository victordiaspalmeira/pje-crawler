from selenium import webdriver
import os
from dotenv import load_dotenv
import logging 
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from utils import init_query_list, human_like_mouse_move
import time 
from tinydb import TinyDB

import urllib
from pydub import AudioSegment
from pydub.playback import play

import audio_transcript

import chime
chime.theme('zelda')

class PjeProccessScrapper():
    """Scrapper desenvolvido para extração automática de processos no PJe BA.

    Class to navigate and collect data from CONSULTA PÚBLICA PJe.


    Note:
        *** ALWAYS CHECK FOR XPATH ELEMENT UPDATES ***
        Can find PUBLIC PROCESSES ONLY.
        Implemented explicitly for PJe BA.
        Tested only for Firefox Webdriver.

    """
    def __init__(self):
        """Initializes driver and xpath element dict
        
        Parameters:
            driver (WebDriver): Selenium Webdriver 
            xpath_dict (dict): Dict containing all xpath element identifiers.
            wait_secs (int, optional): Time in seconds for drive implicitly_wait 

        Returns:
            None
        """

        # Load .env to environment variables
        load_dotenv()

        # Init driver
        self.base_url = os.environ.get('BASE_URL')

        # Init identifiers for input related elements
        self.xpath_input_ids = {
            'PROCCESS_NUMBER_FIELD': os.environ.get('PROCCESS_NUMBER_FIELD'),
            'SEARCH_BUTTON': os.environ.get('SEARCH_BUTTON'),
            'RECAPTCHA_BOX': os.environ.get('RECAPTCHA_BOX'),
            'CAPTCHA_IMAGE_BOX': os.environ.get('CAPTCHA_IMAGE_BOX'),
            'CAPTCHA_AUDIO_ICON': os.environ.get('CAPTCHA_AUDIO_ICON'),
            'DOWNLOAD_ICON': os.environ.get('DOWNLOAD_ICON'),
            'CAPTCHA_AUDIO_TEXT': os.environ.get('CAPTCHA_AUDIO_TEXT'),
            'CAPTCHA_AUDIO_BUTTON': os.environ.get('CAPTCHA_AUDIO_BUTTON')
        }

        # Init identifiers for data related elements
        self.xpath_data_ids = {
            'PROCCESS_NUMBER': os.environ.get('PROCCESS_NUMBER'),
            'LAST_ACTION': os.environ.get('LAST_ACTION'),
        }

    def _check_for_captcha(self, driver, index):
        time.sleep(2)
        iframes = driver.find_elements('tag name', "iframe")
        logging.info("Checking for presearch catpcha...")
        logging.info("iframes: "+ str(len(iframes)))
        detected = False
        try:
            driver.switch_to.frame(iframes[index])
            captcha_box = driver.find_element('xpath', self.xpath_input_ids['CAPTCHA_IMAGE_BOX'])
            detected = True
        except Exception as e:
            logging.info("Captcha not detected.")

        driver.switch_to.default_content()
        
        return detected

    def _do_audio_captcha(self, driver, iframe):
        logging.info("AUDIO CAPTCHA!!!!")
        driver.switch_to.frame(iframe)
        audio_input = driver.find_element('xpath', self.xpath_input_ids['CAPTCHA_AUDIO_ICON'])
        audio_input.click()
        download_input = driver.find_element('xpath', self.xpath_input_ids['DOWNLOAD_ICON'])

        mp3file = urllib.request.urlopen(download_input.get_attribute('href'))
        with open('captcha.mp3', 'wb') as audio_mp3:
            audio_mp3.write(mp3file.read())
        transcription = audio_transcript.transcript('captcha.mp3')

        text_input = driver.find_element('xpath', self.xpath_input_ids['CAPTCHA_AUDIO_TEXT'])
        text_input.send_keys(transcription)

        button = driver.find_element('xpath', self.xpath_input_ids['CAPTCHA_AUDIO_BUTTON'])
        button.click()
        driver.switch_to.default_content()

    def _do_captcha_box(self, driver):
        logging.info("Checking for captcha box...")
        check_box = WebDriverWait(driver, 600).until(
            EC.element_to_be_clickable(
                ('xpath', self.xpath_input_ids['RECAPTCHA_BOX'])
            )
        )

        action = ActionChains(driver)
        human_like_mouse_move(action, check_box)
        check_box.click()

    def _do_proccess_search(self, driver, proccess_id):
        proccess_input = driver.find_element('xpath', self.xpath_input_ids['PROCCESS_NUMBER_FIELD'])
        proccess_input.send_keys(proccess_id)

        search_button = driver.find_element('xpath', self.xpath_input_ids['SEARCH_BUTTON'])
        search_button.click()
    
    def _do_data_extraction(self, driver):
        return {
            'PROCCESS_NUMBER': driver.find_element('xpath', self.xpath_data_ids['PROCCESS_NUMBER']).get_attribute('textContent').strip(),
            'LAST_ACTION': driver.find_element('xpath', self.xpath_data_ids['LAST_ACTION']).get_attribute('textContent').strip()
        }

    def run(self, driver, db, proccess_id: str):
        logging.info(f'Driver getting {self.base_url}')
        wait_time = 3
        driver.implicitly_wait(wait_time)
        driver.get(self.base_url)
        logging.info(f"===== {proccess_id} =====")

        # STEP 1 - INSERT SEARCH INPUT
        logging.info('Inserting input.')
        self._do_proccess_search(driver, proccess_id)

        if self._check_for_captcha(driver, 2):
            logging.info('Presearch captcha found.')
            #chime.error(True)
            self._do_audio_captcha(driver, 2)
            #chime.success(True)
        else:
            logging.info('Presearch captcha not found. Carrying on.')

        # STEP 2 - CHECK FOR CAPTCHA BOX
        self._do_captcha_box(driver)

        if self._check_for_captcha(driver, 2):
            logging.info('Postsearch captcha found.')
            #chime.error(True)
            self._do_audio_captcha(driver, 2)
            #chime.success(True)
        else:
            pass

        # STEP 3 - COLETAR DADOS
        data = self._do_data_extraction(driver)
        if data['PROCCESS_NUMBER'] != proccess_id:
            logging.warning(data['PROCCESS_NUMBER']+":"+str(proccess_id))
            logging.warning('Proccess number collected does not match informed proccess ID!')
        else:
            db.insert(data)
            logging.info(f'Success! {proccess_id} collected successfully.')
            logging.info(f"{data['LAST_ACTION']}")
        time.sleep(0.2)
        driver.refresh()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    db = TinyDB('processos.db')
    keylist = init_query_list(db)
    logging.info('=========================================')
    logging.info('\tPJE SCRAPPER V0.0.1')
    logging.info(f'\tProcessos na fila: {len(keylist)}')
    logging.info(f'\tEu amo muito a minha noiva!!!')
    logging.info('=========================================\n\n')
    logging.basicConfig(level=logging.WARNING)
    service = Service(GeckoDriverManager().install())
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, service=service)

    scrapper = PjeProccessScrapper()

    for proccess_id in keylist:
        if proccess_id == '':
            continue
        try:
            scrapper.run(driver, db, proccess_id.strip())
        except Exception as e:
            print(e)
            driver.refresh()
            chime.warning(True)
            time.sleep(0.3)
            chime.warning(True)
            time.sleep(0.3)
            continue
    chime.success(True)
    
    driver.quit()