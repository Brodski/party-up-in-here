from __future__ import unicode_literals
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.by import By
from typing import List
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from Utils import Utils
import os
import re
import time
from App_Configs import App_Configs
from Save_State import Save_State
from Cloudwatch import Cloudwatch

def logger():
    pass
logger = Cloudwatch.log

def rng_wait():
    return random.uniform(0.1, 0.7)

class Rater:

    def __init__(self, driver: WebDriver, **kwargs):
        logger("####################################################")
        logger("##########        Rater - init()         ##########")
        logger("####################################################")
        self.driver               = driver
        self.email                = App_Configs.init['EMAIL']
        self.pw                   = App_Configs.init['PWORD']
        self.rate_start           = App_Configs.init['RATE_BOT_START']
        self.rate_end_before      = App_Configs.init['RATE_BOT_END_BEFORE']
        self.rate_page            = App_Configs.init['RATE_PAGE']

        logger("     Rater - email           ", self.email)
        logger("     Rater - pw              ", self.pw)
        logger("     Rater - rate_start      ", self.rate_start)
        logger("     Rater - rate_end_before ", self.rate_end_before)
        logger("     Rater - rate_page       ", self.rate_page)

    def run(self):
        logger("##################################################")
        logger("##########        Rater - run()        ###########")
        logger("##################################################")
        start = App_Configs.rating_state['email_index_finished'] if App_Configs.rating_state['email_index_finished'] else self.rate_start

        for i in range (start, self.rate_end_before):  # Since we have the 'retry' code in attempt_callback(), we have to get from App_Configs
            logger(f'---------{i}--------')
            Utils.do_login(self.driver, self.email, self.pw, i)
            self.send_rate()
            App_Configs.rating_state['email_index_finished'] = i
            Save_State.update_state_file()
            self.driver.delete_all_cookies()
        logger("DONE!")

    def send_rate(self):
        Utils.go_to_page_gaurdrails_age(self.driver, self.rate_page)
        time.sleep(0.55) # they send whethere  you rated or not back to you later

        # 1 Click "Rate"
        rate_btn = self.driver.find_element(By.CSS_SELECTOR, "#_rateButton")
        rate_btn.click()
        time.sleep(0.15) # they send whethere  you rated or not back to you later
        
        # 2.A Leave if already rated
        rated_already_msg = self.driver.find_element(By.CSS_SELECTOR, ".ly_grade.retry")
        if rated_already_msg.value_of_css_property('display') == "block":
            logger("🧐 We already rated it apparently")
            yes_btn = self.driver.find_element(By.CSS_SELECTOR, ".lnk_cncl[title='No']")
            yes_btn.click()
            return
        # 2.B Rate it.
        else:
            send_btn = self.driver.find_element(By.CSS_SELECTOR, ".grade_btn a[title='Send']")
            send_btn.click()
        logger("✅ Rated probably succesfully")
        time.sleep(0.1)
        pass
