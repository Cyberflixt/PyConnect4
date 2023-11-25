
import requests
import time
import random
import threading
#import os
import json
import urllib.parse

def lerp(a,b,t):
    """Interpolation linéaire"""
    return a+(b-a)*t

class Client():
    def __init__(self, url, **kwargs):
        """Crée un nouveau client afin de communiquer au serveur"""
        
        self.delai = .5 # temps entre les requetes
        
        self.id = None
        self.url = url
        self.recu = False
        self.methode = 'POST'
        self.envois = [] # informations à envoyer
        self.timeout = 2 # temps max d'une requete
        self.freq = '...' # estimation de frequence d'envoie
        self.freqs = 2
        self.attentes = 0

        # dernier résultat
        self.json = {}
        self.valide = False # Connecté avec un autre utilisateur
        self.status = (-1, 'Non connecté') # information sur la connection
        self.data = {} # informations échangées
        self.dernierTick = None

        # Remplace les attributs par les arguments donnés
        for k in kwargs:
            #self[k] = kwargs[k]
            setattr(self, k, kwargs[k])

    def actualiser(self, envois = None):
        """Renvoie les nouvelles informations provenant du serveur"""
        if self.attentes > 0:
            return

        # On met en forme la requete
        info = {}
        if envois:
            info['data'] = envois
        if self.id:
            info['id'] = self.id
        
        # On supprime les anciennes informations
        self.envois = []
        
        # Envoie de la requête
        self.attentes += 1
        r = False
        if self.methode == 'POST':
            try:
                r = requests.post(self.url, json = info, timeout = self.timeout)
            except Exception:
                err = 'Timeout'
        else: # GET
            # Si on utilise GET, on passe les données par l'url,
            # en les encryptants en texte HTML
            enc = urllib.parse.quote_plus(json.dumps(info))
            urlGet = self.url + '?data=' + enc
            try:
                r = requests.get(urlGet)
            except Exception:
                err = 'Timeout'
        
        if r and r.status_code == 200:
            self.sauvegarde(r)
        else:
            # Erreur dans le code du serveur
            self.recu = False
            self.status = (0, "Erreur du serveur")
            print(r.status_code if r else err,'- Erreur du serveur!')

        # On enleve un de la file d'attente    
        self.attentes -= 1
        
        return self

    def sauvegarde(self, r):
        """Sauvegarde du résultat de la requete"""
        # Résultat sous format de dictionnaire
        res = r.json()
        
        if 'res' in res:
            if res['res'] == '0':
                # Erreur de resultat
                self.recu = False
                return
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

        # Calculation de la frequence
        if self.dernierTick:
            delta = (time.time() - self.dernierTick)
        else:
            delta = 1
        self.freqs = lerp(self.freqs, delta, .3)
        self.freq = f'{self.freqs//.1/10}s' # 1 decimale
        self.dernierTick = time.time()

        # Sauvegarde des resultats
        self.json = res
        self.valide = self.status[0] == 1
    
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
        r"""Répete la fonction donnée avec pour paramêtre les nouvelles informations du serveur
        /!\ Exécuté en paralèlle (pour ne pas arreter le reste du code)"""
        t = threading.Thread(
            target = self.cycleAsync,
            args = [fonction]
        )
        t.start()

    def envoyer(self, info):
        """Envoie l'information donnée au prochain cycle"""
        self.envois.append(info)
        
