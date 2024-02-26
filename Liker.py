from __future__ import unicode_literals
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
import app_config

class Liker:

    config_varz = app_config.AppConfigSingleton(".env_config_local")

    def __init__(self, driver: WebDriver, **kwargs):
        # Set default values
        self.driver = driver
        self.name = kwargs.get('name', 'Anonymous')
        self.age = kwargs.get('age', None)
        self.country = kwargs.get('country', 'Unknown')

        self.email = self.config_varz.EMAIL
        self.pw = self.config_varz.PWORD
        self.like_start = self.config_varz.LIKE_BOT_START
        self.like_end_before = self.config_varz.LIKE_BOT_END_BEFORE

        self.page_urls: List[str] = self.config_varz.LIKE_PAGES

        # You can also dynamically set attributes based on kwargs
        # for key, value in kwargs.items():
        #     setattr(self, key, value)

    
    # https://www.webtoons.com/en/romance/the-dragon-kings-bride/episode-35/viewer?title_no=5517&episode_no=35,
    # https://www.webtoons.com/en/romance/the-dragon-kings-bride/episode-36/viewer?title_no=5517&episode_no=36,
    def run(self):
        for i in range (self.like_start, self.like_end_before):
            print(f'---------{i}--------')
            self.do_login(i)
            for page in self.page_urls:
                print(page)
                self.send_like(page)
            self.pre_login()
        # self.driver.get("https://www.webtoons.com/member/login")
        print("DOOOOOOOOOOOOOOONE")
        print("DOOOOOOOOOOOOOOONE")

    def pre_login(self):
        self.driver.delete_all_cookies()
        cookie_COPPA = {
            'name': 'needCOPPA',
            'value': 'false',
            'domain': '.webtoons.com'
        }
        self.driver.add_cookie(cookie_COPPA)

    def do_login(self, count):
        # login_page = "https://www.webtoons.com/member/login?returnUrl=/"
        login_page = "https://www.webtoons.com/member/login"
        timeout = 10
        username = self.email.split('@')[0]
        domain   = self.email.split('@')[1]

        email_w_count = f"{username}+fsxx{count}@{domain}" # supergera+12@gmail.com


        print('going to login page')
        self.driver.get(login_page)
        print('AT login page')

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
            .click(email_input_clickable).send_keys(email_w_count) \
            .click(password_clickable).send_keys(self.pw) \
            .click(submit_clickable) \
            .perform()
        time.sleep(1)

    def send_like(self, page_url):
        print('about to send likes!!! to:', page_url)
        time.sleep(10)
        cookiez: List[dict] = self.driver.get_cookies()
        print("COOKIEz send likes !!!!!")
        for cook in cookiez:
            print(cook)
            # if cook['name'] != 'needCOPPA':
            #     print('deleting', cook['name'])
            #     self.driver.delete_cookie(cook['name'])
            print()


        timeout = 10
        self.driver.get(page_url)
        print('WE ARRIVED AT??:', page_url)
        self.driver.execute_script("""        
            let like = document.getElementById("likeItButton")
            like.scrollIntoView({ block: "center"}); 
        """)

        # Wait -.-
        ele_wait = EC.presence_of_element_located((By.CSS_SELECTOR, "#cbox_module__write_textarea"))
        WebDriverWait(self.driver, timeout).until(ele_wait)
        
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
        time.sleep(1)