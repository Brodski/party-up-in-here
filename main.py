from __future__ import unicode_literals
from datetime import datetime
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.webdriver import WebDriver
from typing import List
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.firefox import GeckoDriverManager
import argparse
import os
import re
import time
import traceback

from App_Configs import App_Configs
import Creator
import Debug_helper
import Liker
import Rater
from Save_State import Save_State

def setup_browser_driver() -> WebDriver:
    options = Options()
    if App_Configs.init['SELENIUM_IS_HEADLESS'] == "True":
        options.add_argument('--headless')
        os.environ["MOZ_HEADLESS"] = "1"
        

    options.add_argument('--autoplay-policy=user-required') 
    options.add_argument("--width=1750")
    options.add_argument("--height=1080")
    options.add_argument('--disable-features=PreloadMediaEngagementData, MediaEngagementBypassAutoplayPolicies')

    BROWSER_WIDTH = 1550
    BROWSER_HEIGHT = 900
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

    extension_path = os.path.abspath('extensions/stylus.xpi')
    options.profile = firefox_profile
    # service = FirefoxService(executable_path=GeckoDriverManager().install())
    service = get_or_install_service()


    # Set up
    browser = webdriver.Firefox(service=service, options=options)
    browser.install_addon(extension_path)
    browser.set_window_size(BROWSER_WIDTH, BROWSER_HEIGHT)
    browser.set_window_position(0,0)
    configure_stylus(browser)
    browser.get("https://www.webtoons.com/member/join?loginType=EMAIL")
    browser.add_cookie(cookie_COPPA)

    return browser

def configure_stylus(browser: WebDriver):
    css = """
        body {
            overflow: auto !important;
        }
        #_dimForPopup,
        ._policyAgreePopup {
            display: none !important;
        }
    """
    browser.get("about:addons")

    extensions_btn = browser.find_element(By.CSS_SELECTOR, '[data-l10n-id="addon-category-extension"]')
    extensions_btn.click()

    enable_btn = browser.find_element(By.CSS_SELECTOR, 'button[data-l10n-id="extensions-warning-check-compatibility-button"]')
    enable_btn.click()

    stylus_ele = browser.find_element(By.CSS_SELECTOR,'[title^="Stylus"]')
    stylus_ele.click()

    more_opts = browser.find_element(By.CSS_SELECTOR,'[data-l10n-id="addon-options-button"]')
    more_opts.click()

    options_drop = browser.find_element(By.CSS_SELECTOR,'[data-l10n-id="preferences-addon-button"]')
    options_drop.click()

    # options_drop.click() opens a new tab in the background, swap to it and continue
    window_handles = browser.window_handles
    new_tab_handle = window_handles[-1]
    browser.switch_to.window(new_tab_handle)

    write_new_style_btn = browser.find_element(By.CSS_SELECTOR,'button#add-style-label')
    write_new_style_btn.click()

    css_style = browser.find_element(By.CSS_SELECTOR,'.CodeMirror textarea')
    css_style.send_keys(css)

    save_btn = browser.find_element(By.CSS_SELECTOR,'button#save-button')
    save_btn.click()

    browser.close()
    
    original_tab_handle = window_handles[0]
    browser.switch_to.window(original_tab_handle)
    
    
def get_or_install_service(retries=2, delay=3) -> FirefoxService:
    service = FirefoxService(executable_path=GeckoDriverManager().install())
    for i in range(retries):
        try:
            service = FirefoxService(executable_path=GeckoDriverManager().install())
            # service = FirefoxService(executable_path=GeckoDriverManager(cache_manager=DriverCacheManager(valid_range=0)).install())
            return service
        except Exception as e:
            if i < retries - 1:
                time.sleep(delay)
            else:
                raise e


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
    if Save_State.init['RATE_BOT_START'] != App_Configs.init['RATE_BOT_START']:
        is_diff = True
    if Save_State.init['RATE_BOT_END_BEFORE'] != App_Configs.init['RATE_BOT_END_BEFORE']:
        is_diff = True
    if Save_State.init['RATE_PAGE'] != App_Configs.init['RATE_PAGE']:
        is_diff = True
    return is_diff

def attempt_callback(action_class, fail_count=0):
    MAX_RETRY = 3
    while fail_count < MAX_RETRY:
        try:
            action_class.run()
            return
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, exiting gracefully")
            exit(1)
        except Exception as e:
            fail_count = fail_count + 1
            traceback.print_exc()
            print(f"Failed. Trying again... (Exception name: {e.__class__.__name__})")
            take_screenshot_err(action_class.driver) 
            if fail_count >= MAX_RETRY:
                print(f"Failed after {fail_count} attempts. Ending. 🙀😫😵")

def take_screenshot_err(browser: WebDriver):
    timestamp = datetime.now().strftime(r"%Y-%m-%d_%Hh%Mm%Ss") #'2024-07-16_05h12m10s'
    screenshot_path = os.path.join("screenshots", f"error_{timestamp}.png")
    browser.get_screenshot_as_file(screenshot_path)
    screenshot_path_full = os.path.join("screenshots", f"error_full_{timestamp}.png")
    browser.get_full_page_screenshot_as_file(screenshot_path_full)
    print(f"Took a screenshot @ {screenshot_path}")

if __name__ == "__main__":

    conf_file = "zConfig_local.conf" # default
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', type=str, help='file name at local directory')
    parser.add_argument('--which-action', type=str, choices=['create', 'like', 'rate', 'debug'], help='Type of operation to perform')

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

    browser: WebDriver = setup_browser_driver()
    try:
        if args.which_action == "debug":
            debug_helper = Debug_helper.Debug_helper(browser)
            attempt_callback(debug_helper)
        if args.which_action == "create":
            creator = Creator.Creator(browser)
            attempt_callback(creator)
            # creator.run()
        if args.which_action == "like":
            liker = Liker.Liker(browser)
            attempt_callback(liker)
            # liker.run()
        if args.which_action == "rate":
            rater = Rater.Rater(browser)
            attempt_callback(rater)
    except Exception as e:
        print("An error occurred :(")
        print(f"{e}")
        print(traceback.format_exc())
        take_screenshot_err(browser)

    finally:
        if browser:
            browser.quit()
    print("--- ENDING ---")



