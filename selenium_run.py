from __future__ import unicode_literals
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.service import Service as FirefoxService
from typing import List
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import config_run
import os
import re
import time


######################################################################################### 
######################################################################################### 
#
# Use selenium and beautiful soup 
#
######################################################################################### 
######################################################################################### 
options = Options()
if config_run.SELENIUM_IS_HEADLESS == "True":
    options.add_argument('--headless')
    os.environ["MOZ_HEADLESS"] = "1"

options.add_argument('–-autoplay-policy=user-required') 
options.add_argument('--window-size=1750,1250') # width, height
options.add_argument('--disable-features=PreloadMediaEngagementData, MediaEngagementBypassAutoplayPolicies') # width, height

browser = None

with open('send_likes.js', 'r') as file:
    # Read the entire contents of the file into a single string
    send_likes_js = file.read()

# Now file_contents contains the entire contents of the file as a string
print(send_likes_js)

def scrape4VidHref(isDebug=False): # gets returns -> {...} = [ { "displayname":"LoLGeranimo", "name_id":"lolgeranimo", "links":[ "/videos/1758483887", "/videos/1747933567",...
   
    # channelMax = int(config_run.PREP_SELENIUM_NUM_CHANNELS)
    # vodsMax = int(config_run.PREP_SELENIUM_NUM_VODS_PER)
    SLEEP_SCROLL = 2
    NUM_BOT_SCROLLS = 2
    browser = None

    # browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("media.block-play-until-visible", False)
    firefox_profile.set_preference("media.autoplay.blocking_policy", 5)
    firefox_profile.set_preference("media.autoplay.default", 1)
    firefox_profile.set_preference("media.autoplay.enabled.user-gestures-needed", False)
    firefox_profile.set_preference("media.autoplay.block-event.enabled", True)        

    try:
        browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install(), options=options, firefox_profile=firefox_profile))

        url = f'https://www.webtoons.com/en/romance/the-dragon-kings-bride/list?title_no=5517'
        browser.get(url)
        time.sleep(2)

        browser.execute_script(send_likes_js)

        for i in range(NUM_BOT_SCROLLS):
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)") # scroll to the bottom, load all the videos.
            browser.execute_script("""document.querySelector("[id='root'] main .simplebar-scroll-content").scroll(0, 10000)""")
            time.sleep(SLEEP_SCROLL)
        
        # Scrape <a href> via BeautifulSoup
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        vids = soup.select("a[href^='/videos/']:has(img)")
        allHrefs = []
        for tag in vids:
            inner_text = tag.get_text(separator="|").lower()
    except Exception as e:
        print("An error occurred :(")
        print(f"{e}")
    finally:
        # Ensure the browser is closed even if an error occurs
        if browser:
            browser.quit()
    return "yay!"
