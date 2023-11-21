
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
        self.label_pions = None # label tkinter du nombre de pions
        self.btn_couleur = None # label tkinter du nombre de pions
        
        colors = ["red", "yellow"]
        self.couleur = colors[i]

    def rafraichir_pions(self):
        """Actualise le texte du nombre de pions restants"""
        self.label_pions.config(text = f"Pions restants: {self.pions_restants}")

    def enlever_pion(self):
        self.pions_restants -= 1
        self.rafraichir_pions()
        return self.pions_restants

    def choisir_couleur(self):
        if not self.jeu.debut:
            couleur = askcolor(title=f"Choisir une couleur pour {self.nom}")[1]
            if couleur:
                self.couleur = couleur
                self.afficher_couleur(True)
        else:
            self.jeu.label.config(text="La partie a déjà commencé. Impossible de changer de couleur.")

    def afficher_couleur(self, afficher):
        # Affiche ou non la couleur du joueur sur son nom
        if afficher:
            self.label.config(bg = self.couleur)
        else:
            self.label.config(bg = "SystemButtonFace")

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
        
        couleur = "#CCCCCC"
        if self.joueur:
            couleur = self.joueur.couleur
        
        pion = self.canvas.create_oval(
            px,
            py,
            px + self.taille_pion,
            py + self.taille_pion,
            outline = couleur,
            fill = couleur
        )
        return pion

    def changer_joueur(self, joueur):
        couleur = joueur.couleur
        
        self.joueur = joueur
        self.canvas.itemconfig(self.image, fill = couleur, outline = "black")

        return self.joueur.enlever_pion()

    def supprimer(self):
        self.canvas.delete(self.image)
