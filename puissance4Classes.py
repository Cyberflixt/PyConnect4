
import tkinter as tk
from tkinter.colorchooser import askcolor

references = [] # tkinter supprime les images, si elles ne sont pas stockés, ez

class Joueur:
    def __init__(self, jeu, i):
        self.i = i
        self.jeu = jeu
        self.pions_restants = 21
        self.nom = f'Joueur {i+1}'

        self.label = None # label tkinter du nom du joueur
        self.label_pion = None # label tkinter du nombre de pions
        
        colors = ["red", "yellow"]
        self.couleur = colors[i]

    def enlever_pion(self):
        self.pions_restants -= 1
        self.label_pion.config(text = f"Pions restants: {self.pions_restants}")
        return self.pions_restants

class Pion:
    def __init__(self, canvas, x,y):
        self.canvas = canvas
        self.x = x
        self.y = y

        self.taille_pion = 60 # pixels
        self.joueur = None

        self.image = self.afficher_pion()

    def afficher_pion(self):
        px = self.x * self.taille_pion + 145
        py = self.y * self.taille_pion + 60
        
        couleur = "white"
        if self.joueur:
            couleur = self.joueur.couleur
        
        pion = self.canvas.create_oval(
            px,
            py,
            px + self.taille_pion,
            py + self.taille_pion,
            outline = "black",
            fill = couleur
        )
        return pion

    def changer_joueur(self, joueur):
        couleur = joueur.couleur
        
        self.joueur = joueur
        self.canvas.itemconfig(self.image, fill = couleur)

        return self.joueur.enlever_pion()

    def supprimer(self):
        self.canvas.delete(self.image)
