
from server import Client
import time
import os

def traiter_serveur(client):
    os.system('title '+client.status[1])
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
