from __future__ import unicode_literals
from App_Configs import App_Configs
from bs4 import BeautifulSoup
from Save_State import Save_State
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import List
from Utils import Utils
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import os
import random
import re
import time


class Liker:

    def __init__(self, driver: WebDriver, **kwargs):
        print("####################################################")
        print("##########        Liker - init()         ##########")
        print("####################################################")
        self.driver               = driver
        self.email                = App_Configs.init['EMAIL']
        self.pw                   = App_Configs.init['PWORD']
        self.like_start           = App_Configs.init['LIKE_BOT_START']
        self.like_end_before      = App_Configs.init['LIKE_BOT_END_BEFORE']
        self.page_urls: List[str] = App_Configs.init['LIKE_PAGES']

        print("     Liker - email           ", self.email)
        print("     Liker - pw              ", self.pw)
        print("     Liker - like_start      ", self.like_start)
        print("     Liker - like_end_before ", self.like_end_before)
        print("     Liker - page_urls     \n", "\n".join(self.page_urls))

    def run(self):
        print("##################################################")
        print("##########        Liker - run()        ###########")
        print("##################################################")
        start = App_Configs.liking_state['email_index_finished'] if App_Configs.liking_state['email_index_finished'] else self.like_start
        for i in range (start, self.like_end_before):  # Since we have the 'retry' code in attempt_callback(), we have to get from App_Configs
            print(f'---------{i}--------')
            Utils.do_login(self.driver, self.email, self.pw, i)
            for page in self.page_urls:
                print("Liking: ", page)
                self.send_like(page)
                App_Configs.liking_state['email_index_finished'] = i
                Save_State.update_state_file()
            self.driver.delete_all_cookies()
        print("DONE!")

    def send_like(self, page_url):
        timeout = 3
        Utils.go_to_page_gaurdrails_age(self.driver, page_url)

        # Wait for the comment section's textarea thing. B/c thats what humans do.
        try:
            ele_wait = EC.presence_of_element_located((By.CSS_SELECTOR, "#comment_module .wcc_Editor__root"))
            WebDriverWait(self.driver, timeout).until(ele_wait)
        except Exception: 
            print("Warning - couldnt find comment section css selector. Not a problem, maybe worth mentioning it to moneyman")

        # script, scroll to button
        self.driver.execute_script("""        
            let like = document.getElementById("likeItButton")
            like?.scrollIntoView({ block: "start"}); 
        """)
        ele_wait_2 = EC.presence_of_element_located((By.CSS_SELECTOR, "#likeItButton"))
        WebDriverWait(self.driver, timeout).until(ele_wait_2)
        time.sleep(.05)
        
        # No purpose, just log
        is_liked = len(self.driver.find_elements(By.CSS_SELECTOR, "#likeItButton .ico_like2._btnLike.on")) > 0
        if is_liked:
            print("💩 We already liked this page")
            return

        self.driver.execute_script("""     
            let like = document.getElementById("likeItButton");
            let subscribe = document.getElementById("footer_favorites");
            let isLikeOn = like.getElementsByClassName("_btnLike")[0].classList.contains("on");
            let isSubbedOn = subscribe.classList.contains("on");
            if (!isLikeOn) {
                like.click();
            }
            if (!isSubbedOn) {
                subscribe.click();
            }
        """)
        # time.sleep(Utils.rng_wait())
        time.sleep(0.2)

        # except UnexpectedAlertPresentException as e:
        #     print(f"Unexpected alert detected: {e}")
        #     self.handle_unexpected_alert()
        #     pass

    # def handle_unexpected_alert(self):
    #     try:
    #         Alert(self.driver).accept() # or alert.accept()
    #     except NoAlertPresentException:
    #         pass
    
    # def accept_mysterious_alert(self): # shows up randomly 
    #     try:
    #         Alert(self.driver).accept()
    #     except NoAlertPresentException:
    #         pass