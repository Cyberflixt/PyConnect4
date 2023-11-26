
from puissance4_Serveur import Client
import time
import os

def traiter_serveur(client):
    """Fonction appelé lorsque une information du serveur est reçu"""

    # Affichage des informations annèxes dans le titre de la fenêtre
    titre = f'{client.status[1]} id={client.id} recu={client.recu} freq={client.freq}'
    os.system('title '+titre)
    
    # Affichage des données reçu
    if client.data:
        print(client.data)

def boucle_envoie():
    # Envoie d'un texte au serveur grâce à "input"
    if client.valide:
        donnée = input('\nSend data:\n')
        client.envoyer(donnée)
    else:
        time.sleep(1)

    # Répétition
    boucle_envoie()

# Initalisation
os.system('pause')

client = Client('https://transfer.cyberflixt.repl.co', delai = 0)
client.cycle(traiter_serveur)

boucle_envoie()
