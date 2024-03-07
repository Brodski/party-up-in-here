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
import argparse
import os
import re
import time

# must appear here b/c python is a awful programming language
from App_Configs import App_Configs
import Creator
import Liker
from Save_State import Save_State

# email = "biggerpenisthanyoulol@outlook.com" # "Base" email used for eveything. ---- It's a "base" email b/c all bots will look like "biggerpenisthanyoulol+0@gmail.com" , 0=some number

def setup_browser_driver() -> WebDriver:

    extension_path = os.path.abspath('extensions/ublock_origin-1.55.0.xpi')

    options = Options()
    if App_Configs.init['SELENIUM_IS_HEADLESS'] == "True":
        options.add_argument('--headless')
        os.environ["MOZ_HEADLESS"] = "1"
        
    options.add_argument('--autoplay-policy=user-required') 
    options.add_argument("--width=1750")
    options.add_argument("--height=1080")
    options.add_argument('--disable-features=PreloadMediaEngagementData, MediaEngagementBypassAutoplayPolicies')

    BROWSER_WIDTH = 1550
    BROWSER_HEIGHT = 1000
    browser = None
    cookie_COPPA = {
        'name': 'needCOPPA',
        'value': 'false',
        'domain': '.webtoons.com'
    }

    # browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("media.block-play-until-visible", False)
    firefox_profile.set_preference("media.autoplay.blocking_policy", 5)
    firefox_profile.set_preference("media.autoplay.default", 1)
    firefox_profile.set_preference("media.autoplay.enabled.user-gestures-needed", False)
    firefox_profile.set_preference("media.autoplay.block-event.enabled", True)
    
    # Set up
    browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install(), options=options, firefox_profile=firefox_profile))
    # browser.install_addon(extension_path)
    browser.set_window_size(BROWSER_WIDTH, BROWSER_HEIGHT)
    browser.get("https://www.webtoons.com/member/join?loginType=EMAIL")
    browser.add_cookie(cookie_COPPA)
    # options.add_extension(extension_path)

    return browser


def is_current_configs_diff_from_previous_configs(): # returns True for 1st run
    is_diff = False
    if Save_State.init['EMAIL'] != App_Configs.init['EMAIL']:
        is_diff = True
    if Save_State.init['PWORD'] != App_Configs.init['PWORD']:
        is_diff = True
    if Save_State.init['CREATE_BOT_START'] != App_Configs.init['CREATE_BOT_START']:
        is_diff = True
    if Save_State.init['CREATE_BOT_END_BEFORE'] != App_Configs.init['CREATE_BOT_END_BEFORE']:
        is_diff = True
    if Save_State.init['LIKE_BOT_START'] != App_Configs.init['LIKE_BOT_START']:
        is_diff = True
    if Save_State.init['LIKE_BOT_END_BEFORE'] != App_Configs.init['LIKE_BOT_END_BEFORE']:
        is_diff = True
    if Save_State.init['LIKE_PAGES'] != App_Configs.init['LIKE_PAGES']:
        is_diff = True
    return is_diff

if __name__ == "__main__":

    default_conf_file = "zConfig_local.conf"
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', type=str, help='file name at local directory')
    parser.add_argument('--which-action', type=str, choices=['create', 'like', 'read'], help='Type of operation to perform')

    args = parser.parse_args()

    App_Configs(default_conf_file)
    state_filename = App_Configs.prep_state_filename(default_conf_file)
    Save_State.init_state_file(state_filename)
    if is_current_configs_diff_from_previous_configs():
        print("\n main() - TRUE - is_current_configs_diff_from_previous_configs \n")
        App_Configs.create_new_file(Save_State.save_state_file)
    else:
        print("\n main() - FALSE - is_current_configs_diff_from_previous_configs \n")
        Save_State.state_into_app_configs()
    print("args:", args)

    try:
        browser: WebDriver = setup_browser_driver()
        if args.files == None:
            print('expected a file')
            # exit(0)
        if args.which_action == "create":
            creator = Creator.Creator(browser)
            creator.run()
        if args.which_action == "like":
            liker = Liker.Liker(browser)
            liker.run()            
    except Exception as e:
        print("An error occurred :(")
        print(f"{e}")
    finally:
        if browser:
            browser.quit()
    print("--- ENDING ---")
