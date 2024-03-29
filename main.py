from __future__ import unicode_literals
import traceback
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from typing import List
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.webdriver import WebDriver
import argparse
import os
import re
import time

from App_Configs import App_Configs
import Creator
import Liker
from Save_State import Save_State

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

    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("media.block-play-until-visible", False)
    firefox_profile.set_preference("media.autoplay.blocking_policy", 5)
    firefox_profile.set_preference("media.autoplay.default", 1)
    firefox_profile.set_preference("media.autoplay.enabled.user-gestures-needed", False)
    firefox_profile.set_preference("media.autoplay.block-event.enabled", True)
    options.profile = firefox_profile
    service = FirefoxService(executable_path=GeckoDriverManager().install())
    # Set up
    browser = webdriver.Firefox(service=service, options=options)
    browser.set_window_size(BROWSER_WIDTH, BROWSER_HEIGHT)
    browser.get("https://www.webtoons.com/member/join?loginType=EMAIL")
    browser.add_cookie(cookie_COPPA)
    browser.set_window_position(0,0)
    # browser.install_addon(extension_path)
    # options.add_extension(extension_path)

    return browser


def is_current_configs_diff_from_previous_configs(): # returns True for 1st run
    is_diff = False
    if Save_State.init['SELENIUM_IS_HEADLESS'] != App_Configs.init['SELENIUM_IS_HEADLESS']:
        is_diff = True
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

def attempt_callback(callback, fail_count=0):
        MAX_RETRY = 3
        try:
            callback()

        except Exception as e:
            print(f"Failed. Trying again... (Exception name: {e.__class__.__name__})")
            if fail_count < MAX_RETRY:
                time.sleep(1)
                return attempt_callback(callback, fail_count + 1)
            print(f"Failed after {fail_count} attempts. Ending. 🙀😫😵")
            traceback.print_exc()
            raise # Re-raise the last exception to preserve the original traceback




if __name__ == "__main__":

    conf_file = "zConfig_local.conf" # default
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', type=str, help='file name at local directory')
    parser.add_argument('--which-action', type=str, choices=['create', 'like'], help='Type of operation to perform')

    args = parser.parse_args()

    if args.files == None:
        print('\nNo file present in args. You need the flag: --file myfile.conf')
        exit(1)
    conf_file = str(args.files)
    App_Configs(conf_file)
    state_filename = App_Configs.prep_state_filename(conf_file)
    Save_State.init_state_file(state_filename)
    if is_current_configs_diff_from_previous_configs():
        print("\n main() - Config file changed from last time. \n")
        App_Configs.create_new_file(Save_State.save_state_file)
    else:
        print("\n main() - Config file is the SAME from last time \n")
        Save_State.state_into_app_configs()

    try:
        browser: WebDriver = setup_browser_driver()
        if args.which_action == "create":
            creator = Creator.Creator(browser)
            attempt_callback(creator.run())
            # creator.run()
        if args.which_action == "like":
            liker = Liker.Liker(browser)
            attempt_callback(liker.run())
            # liker.run()
    except Exception as e:
        print("An error occurred :(")
        print(f"{e}")
    finally:
        if browser:
            browser.quit()
    print("--- ENDING ---")
