
import requests
import time
import random
import threading
import os
import json
import urllib.parse

class Client():
    def __init__(self, url):
        """Crée un nouveau client afin de communiquer au serveur"""
        
        self.id = None
        self.url = url
        self.envois = []
        self.delai = 1

        # dernier résultat
        self.json = {}
        self.valide = False
        self.status = (-1, 'Non connecté')
        self.data = {}
    
    def actualiser(self, envois = None):
        """Renvoie les nouvelles informations provenant du serveur"""

        # On met en forme la requete
        info = {}
        if envois:
            info['data'] = envois
        if self.id:
            info['id'] = self.id
        
        # On supprime les anciennes informations
        self.envois = []
        
        # Envoie de la requête
        enc = urllib.parse.quote_plus(json.dumps(info))
        url = self.url + '?data=' + enc
        print(url)
        r = requests.get(url)
        print(r)
        if r.status_code == 200:
            res = r.json()
            # Résultat sous format de dictionnaire

            # Garder l'indentifiant donné par le serveur
            if 'id' in res:
                self.id = res['id']

            # Mise à jour des information sur le Client
            # Valeur des resultats par défaut pour une utilisation plus simple
            self.data = {}
            if 'res' in res:
                self.data = res['res']
            
            self.status = (0, "Statue non-reçu")
            if 'status' in res:
                self.status = res['status']
            
            self.json = res
            self.valide = self.status[0] == 1
        else:
            # Erreur dans le code du serveur
            print(r.status_code,'Erreur du serveur!')
            
        return self
    
    def stop(self):
        """Arrête la boucle de la fonction cycle"""
        self.marche = False
    
    def cycleAsync(self, fonction):
        """Répete la fonction donnée avec pour paramêtre les nouvelles informations du serveur"""

        self.marche = True
        while self.marche:
            self.actualiser(self.envois)
            fonction(self)

            time.sleep(self.delai)

    def cycle(self, fonction):
        """Répete la fonction donnée avec pour paramêtre les nouvelles informations du serveur
        /!\\ Exécuté en paralèlle (pour ne pas arreter le reste du code)"""
        t = threading.Thread(
            target = self.cycleAsync,
            args = [fonction]
        )
        t.start()

    def envoyer(self, info):
        """Envoie l'information donnée au prochain cycle"""
        self.envois.append(info)



"""
def traiter_serveur(a):
    res = a['res']
    if res:
        print('\nres:', res)

input('CLIENT')

client = Client()
client.cycle(traiter_serveur)

print('Connection...')

while True:
    if client.valide:
        r = input('\nsend data:')
        client.envoyer(r)
    
    time.sleep(1)

os.system('pause')
"""

