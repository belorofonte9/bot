'''
import unittest
from pyunitreport import HTMLTestRunner
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromiumService
#from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.core.os_manager import ChromeType


class HelloWorld(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
        #self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        driver = self.driver
        driver.implicitly_wait(20)

    
    def test_hello_world(self):
        driver = self.driver
        driver.get('https://www.google.com/')
        web_element = driver.find_element(By.NAME, 'q')
        web_element.send_keys("Selenium webdriver" + Keys.ENTER)

    
    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity = 2, testRunner = HTMLTestRunner(output = 'reportes', report_name = 'hello-world-report'))

'''
'''  
from webdriver_manager.chrome import ChromeDriverManager 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.core.os_manager import ChromeType
import time
'''

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
urls = [

    'https://www.google.com/' 
        
        ]
s = FirefoxService(r"./geckodriver")

for url in urls:
    #driver = webdriver.Chrome(service=s)
    #driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    #driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver = webdriver.Firefox(service=s)
    driver.get(url)
    web_element = driver.find_element(By.NAME, 'q')
    web_element.send_keys("Selenium webdriver" + Keys.ENTER)
    time.sleep(30)
    driver.quit()