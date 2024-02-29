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
import os
import re
import time
from App_Configs import App_Configs
from Save_State import Save_State


class Creator:

    # config_varz = AppConfigSingleton.AppConfigSingleton(".env_config_local")
    # config_varz = AppConfigSingleton.AppConfigSingleton()
    # App_Configs.
    
    cookie_COPPA = {
        'name': 'needCOPPA',
        'value': 'false',
        'domain': '.webtoons.com'
    }
    
    def __init__(self, driver: WebDriver, **kwargs):
        self.driver             = driver
        self.email              = App_Configs.EMAIL
        self.pw                 = App_Configs.PWORD
        self.create_start       = App_Configs.CREATE_BOT_START
        self.create_end_before  = App_Configs.CREATE_BOT_END_BEFORE

    def load_state(self):
        self.email              = Save_State.EMAIL
        self.pw                 = Save_State.PWORD
        self.create_start       = Save_State.CREATE_BOT_START
        self.create_end_before  = Save_State.CREATE_BOT_END_BEFORE


    def run(self):
        for i in range (self.create_start, self.create_end_before):
            print(i)
            self.create_accounts(i)

    def create_accounts(self, count):
        login_url = f'https://www.webtoons.com/member/join?loginType=EMAIL'
        limit = 2
        username = self.email.split('@')[0]
        domain   = self.email.split('@')[1]
        print("EMAIL!!!!!!!!!")
        print("EMAIL!!!!!!!!!")
        print(self.email)

        email_w_count = f"{username}+fsxx{count}@{domain}" # supergera_12@gmail.com

        self.driver.get(login_url)
        self.driver.add_cookie(self.cookie_COPPA)
        time.sleep(2)

        email_clickable         = self.driver.find_element(By.ID, "email")
        pw1Input_clickable      = self.driver.find_element(By.ID, "pw")
        pw1Input2_clickable     = self.driver.find_element(By.ID, "retype_pw")
        nicknameInput_clickable = self.driver.find_element(By.ID, "nickname")
        submit_clickable        = self.driver.find_element(By.CLASS_NAME, "NPI\=a\:signup")
        
        ActionChains(self.driver) \
            .click(email_clickable).send_keys(email_w_count) \
            .click(pw1Input_clickable).send_keys(self.pw) \
            .click(pw1Input2_clickable).send_keys(self.pw) \
            .click(nicknameInput_clickable).send_keys("im_writing_a_ticket_enjoy_ban") \
            .click(submit_clickable) \
            .perform()
        
        element = self.driver.find_element(By.CLASS_NAME, "_joinSuccessLayer")
        print("llllllllllllllllllll")
        wait_elapsed = 0
        is_display_none = True
        while is_display_none:
            is_display_none = "display: none" in element.get_attribute('style')
            wait_elapsed = wait_elapsed + 0.2
            print("creating account... ", wait_elapsed)
            time.sleep(wait_elapsed)
            if wait_elapsed >= limit:
                break
        print("END!")