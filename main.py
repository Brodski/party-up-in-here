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
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import dotenv_values
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
from Utils import Utils
from Save_State import Save_State
from Cloudwatch import Cloudwatch
from dotenv import load_dotenv

load_dotenv()
os.environ['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY')

def logger():
    pass
logger = Cloudwatch.log

def setup_browser_driver() -> WebDriver:
    options = Options()
    if App_Configs.init['SELENIUM_IS_HEADLESS'] == "True":
        options.add_argument('--headless')
        os.environ["MOZ_HEADLESS"] = "1"
    
    options.binary_location = os.path.abspath(os.getenv('FIREFOX_PATH'))
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
    timeout = 3
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

    # btn 1
    extensions_btn_x = EC.presence_of_element_located((By.CSS_SELECTOR, '[data-l10n-id="addon-category-extension"]'))
    WebDriverWait(browser, timeout).until(extensions_btn_x)    
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

    # btn 2
    write_new_style_btn_x = EC.presence_of_element_located((By.CSS_SELECTOR, 'button#add-style-label'))
    WebDriverWait(browser, timeout).until(write_new_style_btn_x)
    write_new_style_btn = browser.find_element(By.CSS_SELECTOR,'button#add-style-label')
    write_new_style_btn.click()

    css_style = browser.find_element(By.CSS_SELECTOR,'.CodeMirror textarea')
    css_style.send_keys(css)

    save_btn = browser.find_element(By.CSS_SELECTOR,'button#save-button')
    save_btn.click()

    browser.close()
    
    original_tab_handle = window_handles[0]
    browser.switch_to.window(original_tab_handle)
    
    
def get_or_install_service(retries=3, delay=3) -> FirefoxService:
    for i in range(retries):
        try:
            executable_path=GeckoDriverManager().install()
            logger("executable_path!?!?!", executable_path)
            logger("os.path.exists(executable_path)???" , os.path.exists(executable_path))
            
            service = FirefoxService(executable_path=executable_path)
            # service = FirefoxService(executable_path=GeckoDriverManager().install())
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

# this can be better. I need to do a yield trick inside of run() i think?
def attempt_callback(action_class, fail_count=0):
    MAX_RETRY = 6
    while fail_count < MAX_RETRY:
        try:
            action_class.run()
            return
        except UnexpectedAlertPresentException as e:
            logger(f"Unexpected alert detected: {e}")
            Utils.handle_unexpected_alert(action_class.driver)
            continue
        except KeyboardInterrupt:
            logger("Caught KeyboardInterrupt, exiting gracefully")
            exit(1)
        except Exception as e:
            fail_count = fail_count + 1
            traceback.print_exc()
            logger(f"Failed. Trying again... (Exception name: {e.__class__.__name__})")
            Utils.take_screenshot_err(action_class.driver) 
            if fail_count >= MAX_RETRY:
                logger(f"Failed after {fail_count} attempts. Ending. 🙀😫😵")

if __name__ == "__main__":
    conf_file = "zConfig_local.conf" # default
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', type=str, help='file name at local directory')
    parser.add_argument('--which-action', type=str, choices=['create', 'like', 'rate', 'debug'], help='Type of operation to perform')

    args = parser.parse_args()

    if args.files == None:
        logger('\nNo file present in args. You need the flag: --file myfile.conf')
        exit(1)
    conf_file = str(args.files)
    App_Configs(conf_file)
    state_filename = App_Configs.prep_state_filename(conf_file)
    Save_State.init_state_file(state_filename)
    if is_current_configs_diff_from_previous_configs():
        logger("\n main() - Config file changed from last time. \n")
        App_Configs.create_new_file(Save_State.save_state_file)
    else:
        logger("\n main() - Config file is the SAME from last time \n")
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
        if args.which_action == "rate":
            rater = Rater.Rater(browser)
            attempt_callback(rater)
    except Exception as e:
        logger("An error occurred :(")
        logger(f"{e}")
        logger(traceback.format_exc())
        Utils.take_screenshot_err(browser)

    finally:
        if browser:
            browser.quit()
    logger("--- ENDING ---")



