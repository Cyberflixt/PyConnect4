
import requests
import time
import random
import threading
import os
import json
import urllib.parse

modeBypass = False

"""
from get_bypass import Bypass

bypass = Bypass()

if modeBypass:
    print('Starting bypass')
    bypass.start()
    print('Loaded bypass')
"""

class Client():
    def __init__(self, url):
        """Crée un nouveau client afin de communiquer au serveur"""
        
        self.id = None
        self.url = url
        self.envois = []
        self.delai = 1
        self.recu = False

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

        # Get Request en bypassant le wifi de l'école ou non
        if modeBypass:
            r = bypass.get(url)
        else:
            r = requests.get(url)
            
        if r.status_code == 200:
            # Résultat sous format de dictionnaire
            res = r.json()

            if 'res' in res:
                if res['res'] == '0':
                    # Erreur de resultat
                    self.recu = False
                    return self
            self.recu = True

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

    def test():
        def traiter_serveur(client):
            os.system(f'title {client.status[1]} id={client.id}')
            if client.data:
                print(client.data)

        def boucle_envoie():
            if client.valide:
                donnée = input('\nSend data:')
                client.envoyer(donnée)
            
            time.sleep(1)
            boucle_envoie()

        input('CLIENT')

        client = Client('https://transfer.cyberflixt.repl.co')
        client.cycle(traiter_serveur)

        boucle_envoie()


Client.test()
