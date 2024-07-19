
import random
import time
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton

from typing import List

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
            print('Unfortunate, we must fill out the age form. Cookies didnt sneak in on time 😔')
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
                print("Age form complete")

    @classmethod
    def do_login(self, driver: WebDriver, email: str, pw: str, count: str):
        login_page = "https://www.webtoons.com/member/login"
        timeout = 10
        username = email.split('@')[0]
        domain   = email.split('@')[1]

        email_w_count = f"{username}+{count}@{domain}" # supergera+12@gmail.com

        driver.get(login_page)
        
        cookie_sess = driver.get_cookie("NEO_SES")
        current_url = driver.current_url
        if cookie_sess or current_url == "https://www.webtoons.com/en/":
            print(f"We are already logged in")
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
        ActionChains(driver) \
            .click(email_input_clickable).send_keys(email_w_count).pause(Utils.rng_wait()) \
            .click(password_clickable).send_keys(pw).pause(Utils.rng_wait()) \
            .click(submit_clickable).pause(Utils.rng_wait()) \
            .perform()

        print("LOGIN COMPLETE: ", email_w_count)
        time.sleep(0.1)