
"""
Alternative à selenium afin de bypass le wifi de l'école
Utilise des get requests avec les information en json
passer dans l'url demandé
"""

from selenium import webdriver
from selenium_stealth import stealth
import time
import json

class Resultat:
    def __init__(self, data):
        self.data = data
        self.status_code = 200

    def json(self):
        return json.loads(self.data)

    def __str__(self):
        return f'Resultat de requete ({self.status_code}): {self.data}'
    def __repr__(self):
        return str(self)

class Bypass:
    def __init__(self, **kwargs):
        self.driver = None
        self.starting = False
        self.headless = False

        for k in kwargs:
            setattr(self, k, kwargs[k])

        self.start()

    def start(self):
        """Initialisation du driver de recherche"""

        if self.starting or self.driver:
            return
        
        self.starting = True
        options = webdriver.ChromeOptions()

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        if self.headless:
            print('Webdriver headless')
            options.add_argument('--headless')

        print(f'Chargement du webdriver (headless = {self.headless})')

        self.driver = webdriver.Chrome(options=options)
        print('Webdriver chargé')
        
        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

    def get(self, url):
        """Obtention du texte d'une page"""
        # On fait charger la page internet
        self.start()
        self.driver.get(url)
        
        # Attendre que la page charge
        # On éxécutant du javascript afin de vérifier
        while self.driver.execute_script("return document.readyState") != "complete":
            pass

        # Extraction du texte de la page
        texte = self.driver.execute_script("return document.body.innerText")
        return Resultat(texte)

    def stop(self):
        """Arret du driver de recherche"""
        self.driver.quit()

