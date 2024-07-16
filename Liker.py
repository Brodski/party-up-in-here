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
# import config_varz
import os
import re
import time
from App_Configs import App_Configs
from Save_State import Save_State

def rng_wait():
    return random.uniform(.1,3)

class Liker:

    cookie_COPPA = {
        'name': 'needCOPPA',
        'value': 'false',
        'domain': '.webtoons.com'
    }

    css = """
        body {
            overflow: auto !important;
        }
        #_dimForPopup,
        ._policyAgreePopup {
            display: none !important;
        }
    """


    def __init__(self, driver: WebDriver, **kwargs):
        print("####################################################")
        print("##########        Liker - init()         ##########")
        print("####################################################")
        self.driver = driver

        self.email                = App_Configs.init['EMAIL']
        self.pw                   = App_Configs.init['PWORD']
        self.like_start           = App_Configs.init['LIKE_BOT_START']
        self.like_end_before      = App_Configs.init['LIKE_BOT_END_BEFORE']
        self.page_urls: List[str] = App_Configs.init['LIKE_PAGES']
        if App_Configs.liking_state['email_index_finished']:
            self.like_start = App_Configs.liking_state['email_index_finished'] + 1

        print("     Liker - email           ", self.email)
        print("     Liker - pw              ", self.pw)
        print("     Liker - like_start      ", self.like_start)
        print("     Liker - like_end_before ", self.like_end_before)
        print("     Liker - page_urls     \n", "\n".join(self.page_urls))


    def run(self):
        print("##################################################")
        print("##########        Liker - run()        ###########")
        print("##################################################")
        for i in range (self.like_start, self.like_end_before):
            print(f'---------{i}--------')
            self.do_login(i)
            for page in self.page_urls:
                print("Liking: ", page)
                self.send_like(page)
                App_Configs.liking_state['email_index_finished'] = i
                Save_State.update_state_file()
            self.driver.delete_all_cookies()
        print("DONE!")


    def do_login(self, count):
        # time.sleep(rng_wait())
        login_page = "https://www.webtoons.com/member/login"
        timeout = 10
        username = self.email.split('@')[0]
        domain   = self.email.split('@')[1]

        email_w_count = f"{username}+{count}@{domain}" # supergera+12@gmail.com

        self.driver.get(login_page)
        self.driver.add_cookie(self.cookie_COPPA)

        # 1 Wait for client render -.-
        login_email_btn_wait = EC.presence_of_element_located((By.CSS_SELECTOR, "._btnLoginEmail"))
        WebDriverWait(self.driver, timeout).until(login_email_btn_wait)

        # 2 click "Email" option
        login_email_btn = self.driver.find_element(By.CSS_SELECTOR, "._btnLoginEmail")
        login_email_btn.click()

        # 3 Wait for client render again -.-
        pw_btn = EC.presence_of_element_located((By.ID, "email_address"))
        WebDriverWait(self.driver, timeout).until(pw_btn)

        # 4 Fillout login form
        self.driver.execute_script("""
            const evt2 = new Event("focus", {"view": window, "bubbles":true, "cancelable":false});
            document.getElementById("email_password").dispatchEvent(evt2)
        """)
                
        email_input_clickable   = self.driver.find_element(By.ID, "email_address")
        password_clickable      = self.driver.find_element(By.ID, "email_password")
        submit_clickable        = self.driver.find_element(By.CSS_SELECTOR, "button.login_btn.type_green._emailLoginButton")
        ActionChains(self.driver) \
            .click(email_input_clickable).send_keys(email_w_count).pause(rng_wait()) \
            .click(password_clickable).send_keys(self.pw).pause(rng_wait()) \
            .click(submit_clickable).pause(rng_wait()) \
            .perform()

        print("LIKER - LOGIN COMPLETE: ", email_w_count)
        time.sleep(0.1)

    def send_like(self, page_url):
        timeout = 3
        self.driver.get(page_url)
        # inject css
        self.driver.execute_script(f"""
            var style = document.createElement('style');
            style.type = 'text/css';
            style.innerHTML = `{self.css}`;
            document.head.appendChild(style);
        """)
        # script, scroll to button
        self.driver.execute_script("""        
            let like = document.getElementById("likeItButton")
            like.scrollIntoView({ block: "start"}); 
        """)
        # Wait for the comment section's textarea thing. B/c thats what humans do.
        try:
            ele_wait = EC.presence_of_element_located((By.CSS_SELECTOR, "#comment_module .wcc_Editor__root"))
            WebDriverWait(self.driver, timeout).until(ele_wait)
        except Exception: 
            print("Warning - couldnt find comment section css selector. Not a problem, maybe worth mentioning it to moneyman")
        
        time.sleep(.1)
        self.driver.execute_script("""     
            let like = document.getElementById("likeItButton")
            let subscribe = document.getElementById("footer_favorites")
            let isLikeOn = like.getElementsByClassName("_btnLike")[0].classList.contains("on")
            let isSubbedOn = subscribe.classList.contains("on")
            console.log("isLikeOn", isLikeOn)
            console.log("isSubbedOn", isSubbedOn)
            if (!isLikeOn) {
                like.click()
            }
            if (!isSubbedOn) {
                subscribe.click()
            }
        """)
        # time.sleep(rng_wait())
        time.sleep(0.2)