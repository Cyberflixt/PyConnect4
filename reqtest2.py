
"""
Alternative à selenium afin de bypass le wifi de l'école
Utilise des get requests avec les information en json
passer dans l'url demandé
"""

from selenium import webdriver
from selenium_stealth import stealth

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

url = "https://transfer.cyberflixt.repl.co/"
def getRequest():
    driver.get(url)
    # Wait for page to load
    while driver.execute_script("return document.readyState") != "complete":
        pass

    r = driver.execute_script("return document.body.innerText")
    return r

for i in range(10):
    getRequest()
    time.sleep(1)

driver.quit()
