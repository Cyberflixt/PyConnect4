
"""
Alternative à selenium afin de bypass le wifi de l'école
Utilise des get requests avec les information en json
passer dans l'url demandé
"""

from selenium import webdriver
from selenium_stealth import stealth
#from selenium.webdriver.chrome.service import Service
import time

chrome_path = r'.\chromedriver_win32\chromedriver.exe'

class Bypass():
    def __init__(self):
        pass

    def start(self):
        #service = Service(executable_path=chrome_path)
        
        options = webdriver.ChromeOptions()
        #options.add_argument("start-maximized")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        #options.add_argument('--headless')

        print('Chargement du webdriver')
        #driver = webdriver.Chrome(service=service, options=options)

        driver = webdriver.Chrome(options=options)
        print('Webdriver chargé')
        
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        r = self.get("https://transfer.cyberflixt.repl.co/")
        print(r)

    def get(self, url):
        driver.get(url)
        # Wait for page to load
        while driver.execute_script("return document.readyState") != "complete":
            pass
        r = driver.execute_script("return document.body.innerText")
        return r

    def stop(self):
        driver.quit()

a = Bypass()
print(a.start())
