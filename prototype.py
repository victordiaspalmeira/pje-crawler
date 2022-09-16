import unittest 
from random import uniform, randint
from time import sleep
import scipy.interpolate as si
from datetime import datetime

import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from webdriver_manager.firefox import GeckoDriverManager

from proxy_list import PROXY

import os
from dotenv import load_dotenv

index = int(uniform(0, len(PROXY)))
PROXY = PROXY[index]["host"]+":"+str(PROXY[index]["port"])

# RANDOMIZATION RELATED
MIN_RAND        = 0.64
MAX_RAND        = 1.27
LONG_MIN_RAND   = 4.78
LONG_MAX_RAND = 11.1

class PjeCrawler(unittest.TestCase):
    headless = False
    options = None
    profile = None
    capabilities = None 
    proccess_number = None 

    def setup_options(self):
        self.options = webdriver.FirefoxOptions()
        self.options.headless = self.headless

    def setup_profile(self):
        self.profile = webdriver.FirefoxProfile("C:/Users/victo/AppData/Roaming/Mozilla/Firefox/Profiles/pbzeh28s.selenium")
        self.profile._install_extension("{e58d3966-3d76-4cd9-8552-1582fbc800c1}.xpi", unpack=False)
        self.profile.set_preference("security.fileuri.strict_origin_policy", False)
        self.profile.update_preferences()

    def setup_capabilities(self):
        self.capabilities = webdriver.DesiredCapabilities.FIREFOX
        self.capabilities['marionette'] = True

    def setup_proxy(self):
        self.log(PROXY)
        self.capabilities['proxy'] = {
            "proxyType": "MANUAL",
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY
        }

    def setUp(self):
        self.setup_profile()
        self.setup_options()
        self.setup_capabilities()
        self.setup_proxy() # comment this line for ignore proxy

        self.driver = webdriver.Firefox(
            options=self.options,
            capabilities=self.capabilities, 
            firefox_profile=self.profile, 
            executable_path=GeckoDriverManager().install()
        )

    # Simple logging method
    def log(s,t=None):
            now = datetime.now()
            if t == None :
                    t = "Main"
            print ("%s :: %s -> %s " % (str(now), t, s))

    # Use time.sleep for waiting and uniform for randomizing
    def wait_between(self, a, b):
        rand=uniform(a, b)
        sleep(rand)

    def human_like_mouse_move(self, action, start_element):
        points = [[6, 2], [3, 2],[0, 0], [0, 2]];
        points = np.array(points)
        x = points[:,0]
        y = points[:,1]

        t = range(len(points))
        ipl_t = np.linspace(0.0, len(points) - 1, 100)

        x_tup = si.splrep(t, x, k=1)
        y_tup = si.splrep(t, y, k=1)

        x_list = list(x_tup)
        xl = x.tolist()
        x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

        y_list = list(y_tup)
        yl = y.tolist()
        y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

        x_i = si.splev(ipl_t, x_list)
        y_i = si.splev(ipl_t, y_list)

        startElement = start_element

        action.move_to_element(startElement);
        action.perform();

        c = 5 # change it for more move
        i = 0
        for mouse_x, mouse_y in zip(x_i, y_i):
            action.move_by_offset(mouse_x,mouse_y);
            action.perform();
            self.log("Move mouse to, %s ,%s" % (mouse_x, mouse_y))
            i += 1
            if i == c:
                break

    def do_captcha(self,driver):
        driver.switch_to.default_content()
        self.log("Switch to new frame")
        #iframes = driver.find_elements('tag name', "iframe")
        #self.log(f'iframes found:{iframes}')
        #driver.switch_to.frame(iframes[0])

        self.log("Wait for recaptcha-anchor")
        check_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(('xpath' ,'/html/body/app-root/div/app-public/mat-sidenav-container/mat-sidenav-content/div/app-resultado/mat-card/mat-card-content/re-captcha/div/div/iframe')))

        self.log("Wait")
        self.wait_between(MIN_RAND, MAX_RAND)

        action =  ActionChains(driver);
        self.human_like_mouse_move(action, check_box)

        self.log("Click")
        check_box.click()

        self.log("Wait")
        self.wait_between(MIN_RAND, MAX_RAND)

        self.log("Mouse movements")
        action =  ActionChains(driver);
        self.human_like_mouse_move(action, check_box)

        self.log("Switch Frame")
        driver.switch_to.default_content()
        iframes = driver.find_elements('tag name', "iframe")
        driver.switch_to.frame(iframes[2])

        self.log("Wait")
        self.wait_between(MIN_RAND, MAX_RAND)
        
        self.log("Find solver button")
        btn_holder = driver.find_element('css selector', 'div.button-holder:nth-child(4)')
        print(btn_holder)
        outer = driver.execute_script(
            'return arguments[0].shadowRoot',
            btn_holder
        )
        capt_btn = outer.find_element('xpath', '//*[@id="solver-button"]')

        self.log("Wait")
        self.wait_between(MIN_RAND, MAX_RAND)

        self.log("Click")
        capt_btn.click()

        self.log("Wait")
        self.wait_between(LONG_MIN_RAND, LONG_MAX_RAND)

        try:
            self.log("Alert exists")
            alert_handler = WebDriverWait(driver, 20).until(
                    EC.alert_is_present()
                    )
            alert = driver.switch_to.alert
            self.log("Wait before accept alert")
            self.wait_between(MIN_RAND, MAX_RAND)

            alert.accept()

            self.wait_between(MIN_RAND, MAX_RAND)
            self.log("Alert accepted, retry captcha solver")

            self.do_captcha(driver)
        except:
            self.log("No alert")


        self.log("Wait")
        driver.implicitly_wait(5)
        self.log("Switch")
        driver.switch_to.frame(driver.find_elements('tag name', "iframe")[0])

    def test_run(self):
        load_dotenv()
        driver = self.driver
        proccess_number = self.proccess_number

        self.log(f'Starting crawler in {os.environ.get("BASE_URL")}')
        driver.get(os.environ.get("BASE_URL"))

        self.log(f"Starting data crawling for {proccess_number}...")
        self.log(f'Inserting input...')
        
        proccess_input = self.driver.find_element('xpath', os.environ.get('PROCCESS_NUMBER_FIELD'))
        proccess_input.send_keys(proccess_number)

        self.log("Finding search button...")
        self.wait_between(MIN_RAND, MAX_RAND)

        search_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(('xpath', os.environ.get('QUERY_BUTTON')))
        )

        self.wait_between(MIN_RAND, MAX_RAND)
        search_button.click()

        self.log("Trying to solve captcha...")

        self.do_captcha(driver)

        self.log("Done")

    def tearDown(self):
        self.wait_between(25.13, 39.05)
        self.driver.quit()

if __name__ == "__main__":
    PjeCrawler.proccess_number = '0602691-22.2022.6.05.0000'
    unittest.main()

    