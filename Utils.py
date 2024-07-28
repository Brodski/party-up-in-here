
from datetime import datetime
import os
import random
import time
from S3 import S3
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Cloudwatch import Cloudwatch

def logger():
    pass
logger = Cloudwatch.log


class Utils:
    cookie_COPPA = {
        'name': 'needCOPPA',
        'value': 'false',
        'domain': '.webtoons.com'
    }
    cookie_cm_agr = {
        'name': 'cm_agr',
        'value': 'false',
        'domain': '.webtoons.com'
    }
    cookie_cm_lgr = {
        'name': 'cm_lgr',
        'value': 'false',
        'domain': '.webtoons.com'
    }

    @staticmethod
    def rng_wait():
        return random.uniform(0.1, 0.7)

    # Navigate to a url. Add cookies saying we are old. Sometimes it fails, if so fill out age-form
    @classmethod
    def go_to_page_gaurdrails_age(self, driver: WebDriver, page_url: str):
        timeout = 4
        driver.add_cookie(self.cookie_cm_lgr)
        driver.add_cookie(self.cookie_cm_agr)
        driver.get(page_url)
        try:
            WebDriverWait(driver, timeout).until(EC.url_to_be(page_url))
        except:
            logger('Unfortunate, we must fill out the age form. Cookies didnt sneak in on time 😔')
            if driver.current_url == "https://www.webtoons.com/en/age-gate?isLogin=true":
                day = driver.find_element(By.CSS_SELECTOR, "input#_day")
                day.send_keys("1")
                
                month = driver.find_element(By.CSS_SELECTOR, "a.lk_month._selectedMonth")
                month.click()
                month_dropdown = driver.find_element(By.CSS_SELECTOR, ".month ul li._month")
                month_dropdown.click()

                year = driver.find_element(By.CSS_SELECTOR, ".year input.input_text")
                year.send_keys("2000")

                submit = driver.find_element(By.CSS_SELECTOR, ".btnarea a")
                submit.click()
                
                WebDriverWait(driver, 4).until(EC.url_to_be(page_url))
                logger("Age form complete")

    @classmethod
    def do_login(self, driver: WebDriver, email: str, pw: str, count: str):
        Utils.accept_mysterious_alert(driver)

        login_page = "https://www.webtoons.com/member/login"
        timeout = 10
        username = email.split('@')[0]
        domain   = email.split('@')[1]

        email_w_count = f"{username}+{count}@{domain}" # supergera+12@gmail.com

        driver.get(login_page)
        
        cookie_sess = driver.get_cookie("NEO_SES")
        current_url = driver.current_url
        if cookie_sess or current_url == "https://www.webtoons.com/en/":
            logger(f"We are already logged in")
            return

        driver.add_cookie(self.cookie_COPPA)

        # 1 Wait for client render -.-
        login_email_btn_wait = EC.presence_of_element_located((By.CSS_SELECTOR, "._btnLoginEmail"))
        WebDriverWait(driver, timeout).until(login_email_btn_wait)

        # 2 click "Email" option
        login_email_btn = driver.find_element(By.CSS_SELECTOR, "._btnLoginEmail")
        login_email_btn.click()

        # 3 Wait for client render again -.-
        pw_btn = EC.presence_of_element_located((By.ID, "email_address"))
        WebDriverWait(driver, timeout).until(pw_btn)

        # 4 Fillout login form
        driver.execute_script("""
            const evt2 = new Event("focus", {"view": window, "bubbles":true, "cancelable":false});
            document.getElementById("email_password").dispatchEvent(evt2)
        """)
                
        email_input_clickable   = driver.find_element(By.ID, "email_address")
        password_clickable      = driver.find_element(By.ID, "email_password")
        submit_clickable        = driver.find_element(By.CSS_SELECTOR, "button.login_btn.type_green._emailLoginButton")
        login_form              = driver.find_element(By.CSS_SELECTOR, "#formLogin") # get form element before we leave the page, we'll use to confirm we have left/logged in 

        ActionChains(driver) \
            .click(email_input_clickable).send_keys(email_w_count).pause(Utils.rng_wait()) \
            .click(password_clickable).send_keys(pw).pause(Utils.rng_wait()) \
            .click(submit_clickable) \
            .perform()
            # .click(submit_clickable).pause(Utils.rng_wait()) \

        # Wait for the URL to change. The page is likely redirected 
        # alternatively we can use EC.staleness_of(element). Waits until element is gone. # WebDriverWait(driver, 10).until(EC.staleness_of(login_form))
        WebDriverWait(driver, 10).until(EC.url_changes("https://www.webtoons.com/member/login"))
        logger("LOGIN COMPLETE: ", email_w_count)

    @staticmethod
    def take_screenshot_err(browser: WebDriver):
        timestamp = datetime.now().strftime(r"%Y-%m-%d_%Hh%Mm%Ss") #'2024-07-16_05h12m10s'

        # 1st screenshot, viewport
        filename = f"error_{timestamp}.png"
        screenshot_path = os.path.join("screenshots", filename)
        browser.get_screenshot_as_file(screenshot_path)
        S3.upload_screenshot_to_s3(screenshot_path, filename)

        # 2nd screenshot, full
        filename2 = f"error_full_{timestamp}.png"
        screenshot_path_full = os.path.join("screenshots", filename2)
        browser.get_full_page_screenshot_as_file(screenshot_path_full)
        S3.upload_screenshot_to_s3(screenshot_path_full, filename2)
        logger(f"Took a screenshot @ {screenshot_path}")

    @staticmethod
    def handle_unexpected_alert(driver):
        try:
            Alert(driver).accept() # or alert.accept()
        except NoAlertPresentException:
            pass

    @staticmethod
    def accept_mysterious_alert(driver): # shows up randomly 
        try:
            Alert(driver).accept()
        except NoAlertPresentException:
            pass