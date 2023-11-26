
import requests
import time, threading
import json, urllib.parse

from libs.puissance4_Bypass import Bypass


def lerp(a,b,t):
    """Interpolation linéaire"""
    return a+(b-a)*t

class Client():
    def __init__(self, url, **kwargs):
        """Crée un nouveau client afin de communiquer au serveur"""

        # Paramêtres
        self.delai = .5 # temps entre les requetes
        self.methode = 'POST'

        # Attributs par défaut
        self.id = None
        self.url = url
        self.recu = False
        self.envois = {} # informations à envoyer
        self.timeout = 2 # temps max d'une requete
        self.freq = '...' # estimation de frequence d'envoie
        self.freqs = 2
        self.attentes = 0
        self.cycle_token = 0
        self.bypass = False

        # Attributs du dernier résultat reçu
        self.json = {}
        self.valide = False # Connecté avec un autre utilisateur
        self.status = (-1, 'Non connecté') # information sur la connection
        self.data = {} # informations échangées
        self.dernierTick = None

        # Remplace les attributs par les arguments donnés
        for k in kwargs:
            setattr(self, k, kwargs[k])

        if self.bypass:
            self.bypass = Bypass()

    def get(self, info):
        """Obtention des informations du serveur avec la méthode choisie"""
        r = False
        err = None
        
        if self.methode == 'POST' and not self.bypass:
            # POST, on passe les données en JSON
            print('Getting post')
            try:
                r = requests.post(self.url, json = info, timeout = self.timeout)
            except Exception:
                err = 'Timeout'
            
        elif self.methode == 'GET':
            # GET, on passe les données par l'url,
            # en les encryptants en texte HTML
            
            enc = urllib.parse.quote_plus(json.dumps(info))
            urlGet = self.url + '?data=' + enc

            if self.bypass:
                print('Getting bypass')
                try:
                    r = self.bypass.get(urlGet)
                except Exception:
                    # Recommencer sans le bypass
                    self.bypass = False
            else:
                print('Getting get')
                try:
                    r = requests.get(urlGet)
                except Exception:
                    err = 'Timeout'
        return r,err

    def actualiser(self):
        """Renvoie les nouvelles informations provenant du serveur"""
        if self.attentes > 0:
            return

        # On met en forme la requete
        info = {'data': self.envois}
        if self.id:
            info['id'] = self.id
        
        # On supprime les anciennes informations
        self.envois = {}
        
        # Envoie de la requête
        self.attentes += 1
        r, err = self.get(info)
        
        # Valeur des resultats par défaut pour une utilisation plus simple
        self.data = {}
        
        if r and r.status_code == 200:
            # Résultat correct
            self.sauvegarde(r)
        else:
            # Erreur dans la requete au serveur
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
        self.cycle_token += 1
    
    def cycleAsync(self, fonction, *args):
        """Répete la fonction donnée en passant les nouvelles informations du serveur"""

        token = self.cycle_token
        while token == self.cycle_token:
            # Si la boucle n'a pas été arrêtée
            # On prends les nouvelles informations
            self.actualiser()
            # Puis on les envoient dans la fonction souhaitée
            fonction(self, *args)

            time.sleep(self.delai)

    def cycle(self, fonction, *args):
        r"""Répete la fonction donnée avec pour paramêtre les nouvelles informations du serveur
        /!\ Exécuté en paralèlle (pour ne pas arreter le reste du code)"""
        t = threading.Thread(
            target = self.cycleAsync,
            args = [fonction, *args]
        )
        t.start()

    def envoyer(self, dico):
        """Envoie des informations d'un dictionaire donné au prochain cycle"""
        for k in dico:
            self.envois[k] = dico[k]
        
