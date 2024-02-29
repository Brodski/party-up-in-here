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
    config_varz = App_Configs(".env_config_local")

    options = Options()
    if config_varz.SELENIUM_IS_HEADLESS == "True":
        options.add_argument('--headless')
        os.environ["MOZ_HEADLESS"] = "1"
        
    options.add_argument('--autoplay-policy=user-required') 
    options.add_argument("--width=1750")
    options.add_argument("--height=1080")
    options.add_argument('--disable-features=PreloadMediaEngagementData, MediaEngagementBypassAutoplayPolicies')

    SLEEP_SCROLL = 2
    NUM_BOT_SCROLLS = 2
    BROWSER_WIDTH = 1550
    BROWSER_HEIGHT = 1000
    END_MAKE_ACCOUNT = 3
    browser = None
    # cookie_COPPA = {
    #     'name': 'needCOPPA',
    #     'value': 'false',
    #     'domain': '.webtoons.com'
    # }

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
    # browser.get("https://www.webtoons.com/member/join?loginType=EMAIL")
    # browser.add_cookie(cookie_COPPA)
    # options.add_extension(extension_path)

    return browser


def gogogo(isDebug=False):
    try:
        browser: WebDriver = setup_browser_driver()

        # Make account
        # for cnt in range(0, END_MAKE_ACCOUNT):
        #     create_accounts.create_accounts(browser, cnt)
        # time.sleep(10)
        
        # Send Likes
        # send_likes.send_likes(None, 0)



        # Scrape <a href> via BeautifulSoup
        # soup = BeautifulSoup(browser.page_source, 'html.parser')
        # vids = soup.select("a[href^='/videos/']:has(img)")
        # allHrefs = []
        # for tag in vids:
        #     inner_text = tag.get_text(separator="|").lower()
    except Exception as e:
        print("An error occurred :(")
        print(f"{e}")
    finally:
        # Ensure the browser is closed even if an error occurs
        if browser:
            browser.quit()
    return "yay!"

def is_configs_diff_from_previous_configs():
    is_diff = False
    if Save_State.EMAIL != App_Configs.EMAIL:
        is_diff = True
    if Save_State.PWORD != App_Configs.PWORD:
        is_diff = True
    if Save_State.CREATE_BOT_START != App_Configs.CREATE_BOT_START:
        is_diff = True
    if Save_State.CREATE_BOT_END_BEFORE != App_Configs.CREATE_BOT_END_BEFORE:
        is_diff = True
    if Save_State.LIKE_BOT_START != App_Configs.LIKE_BOT_START:
        is_diff = True
    if Save_State.LIKE_BOT_END_BEFORE != App_Configs.LIKE_BOT_END_BEFORE:
        is_diff = True
    if Save_State.LIKE_PAGES != App_Configs.LIKE_PAGES:
        is_diff = True
    return is_diff

if __name__ == "__main__":
    # gogogo()
    my_conf_file = ".env_config_local"
    App_Configs(my_conf_file)

    parser = argparse.ArgumentParser()
    parser.add_argument('--files', type=str, help='file name at local directory')
    parser.add_argument('--which-action', type=str, choices=['create', 'vote', 'read'], help='Type of operation to perform')

    args = parser.parse_args()

    statez = Save_State(my_conf_file)

    exit(0)

    print("args:", args)

    browser: WebDriver = setup_browser_driver()
    if args.files == None:
        print('expected a file')
        # exit(0)
    if args.which_action == "create":
        creator = Creator.Creator(browser)
        creator.load_state()
        creator.run()
    if args.which_action == "vote":
        liker = Liker.Liker(browser)
        liker.run()

        # try:
        #     with open(args.files, 'r') as file:
        #         print("READING")
        #         content = file.read()
        #         print("File content:")
        #         print(content)
        # except FileNotFoundError:
        #     print("File not found. Proceeding with the argument as a simple string.")