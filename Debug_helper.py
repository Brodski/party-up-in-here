
import time
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException

class Debug_helper:
    
    def __init__(self, driver: WebDriver, **kwargs):
        print("###############################################################")
        print("##############        DEBUG - init()        #################")
        print("###############################################################")
        self.driver = driver

    def run(self):
        self.driver.get("http://localhost:6966/")
        time.sleep(3)
        try:
            Alert(self.driver).accept()
            self.driver.execute_script("""
                let like = document.getElementById("likeItButton")
                like.style.display = "none"
            """)
        except NoAlertPresentException:
            print("No alert found")        
        time.sleep(3)
        self.driver.get("http://localhost:6966/")
        return True