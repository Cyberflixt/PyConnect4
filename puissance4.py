
import tkinter as tk
from tkinter.colorchooser import askcolor
from puissance4Classes import *
from puissance4Connection import Connection

connection = Connection()

class Accueil:
    def __init__(self):
        # Création de la fenêtre tkinter
        self.fen = tk.Tk()
        self.fen.attributes('-fullscreen', True)
        self.fen.title("Accueil")
        
        self.create_gui()
    
    def create_gui(self):
        # Création de l'apparence du menu principale
        # Image du titre du jeu au centre
        image = tk.PhotoImage(file="menu.png") 
        image_menu = tk.Label(self.fen, image=image)
        image_menu.image = image
        image_menu.pack()
        
        # Bouton "Jouer Local"
        img_btn_local = tk.PhotoImage(file = "btnLocal.png")
        btn_local = tk.Button(self.fen, image = img_btn_local, command=self.demarrer_local, bd=0)
        btn_local.image = img_btn_local
        btn_local.pack()
        
        # Bouton "Jouer En Ligne"
        img_btn_internet = tk.PhotoImage(file = "btnOnline.png")
        btn_internet = tk.Button(self.fen, image = img_btn_internet, command=self.demarrer_internet, bd=0)
        btn_internet.image = img_btn_internet
        btn_internet.pack(pady=10)

        
        # Bouton Fermer
        img_btn_close = tk.PhotoImage(file = "btnClose.png")
        btn_local = tk.Button(self.fen, image = img_btn_close, command=self.fermer, bd=0)
        btn_local.image = img_btn_close
        btn_local.place(relx=0, rely=0)

    def fermer(self):
        self.fen.destroy()
    
    def demarrer_local(self):
        self.fermer()  # Fermer la fenêtre d'accueil
        jeu = Jeu()  # Démarrer le jeu Puissance 4
    
    def demarrer_internet(self):
        self.fermer()  # Fermer la fenêtre d'accueil
        jeu = Jeu(True)  # Démarrer le jeu Puissance 4

class Jeu:
    def __init__(self, internet = False):
        # création de la fenetre tkinter
        self.fen = tk.Tk()
        self.fen.attributes('-fullscreen', True)

        # changement du titre "local" ou "en ligne"
        self.internet = internet # mode en ligne
        if internet:
            self.fen.title("Puissance 4 Local")
        else:
            self.fen.title("Puissance 4 En ligne")

        # Attributs constants de Jeu 
        self.taille = [7,6]
        self.taille_pion = 60 # pixels

        # Tableau de tableau, remplit quand la partie commence
        self.pions = []
        
        # Crée le joueur 1 et le joueur 2
        self.joueurs = [Joueur(self, i) for i in range(2)]
        self.joueur_actuel = None
        
        self.debut = False  # Variable pour suivre l'état de démarrage        
        
        self.create_gui()
    
    def create_gui(self):
        # Espace pour l'image en haut
        espace = tk.Frame(self.fen, height=50)
        espace.pack(fill=tk.BOTH, expand=True)
        
        # Bouton "Démarrer" pour commencer la partie
        btn_demarrer = tk.Button(espace, text="Démarrer", command=self.commencer_partie)
        btn_demarrer.pack()
        
        # Grille centrale
        self.canvas = tk.Canvas(self.fen, width=700, height=600)
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Création des élements symmétriques pour chaque joueur
        for i in range(2):
            joueur = self.joueurs[i]

            # Coté de l'interface du joueur
            tk_side = tk.LEFT
            if i==1:
                tk_side = tk.RIGHT

            # Encadrage des elements
            cadre = tk.Frame(self.fen, width=50)
            cadre.pack(side=tk_side, fill=tk.BOTH, expand=True)

            # Texte avec le nom du joueur
            label_nom = tk.Label(cadre, text=joueur.nom, font=("Arial", 14))
            label_nom.pack()

            # Texte avec le nombre de pions restants du joueur
            label_pions = tk.Label(cadre, text="", font=("Arial", 12))
            label_pions.pack()

            # Bouton pour changer la couleur du joueur
            btn_couleur = tk.Button(cadre, text="Choisir Couleur", command = joueur.choisir_couleur)
            btn_couleur.pack()
            
            joueur.label = label_nom
            joueur.label_pions = label_pions
            joueur.btn_couleur = btn_couleur

            joueur.rafraichir_pions()
            joueur.afficher_couleur(True)

        # Texte affichant l'aide
        self.label = tk.Label(self.fen, text="Cliquez sur 'Démarrer' pour commencer la partie")
        self.label.pack()

        # Message centré (affiché uniquement pour annoncer le gagnant)
        self.message_centre = tk.Label(self.fen, text="", font=("Arial", 20), bg="white", relief=tk.SOLID, borderwidth=2)

        # Bouton Retour
        img_btn_retour = tk.PhotoImage(file = "btnRetour.png")
        btn_retour = tk.Button(self.fen, image = img_btn_retour, command=self.fermer, bd=0)
        btn_retour.image = img_btn_retour
        btn_retour.place(relx=0, rely=0)
        
        # Remplit le canvas d'emplacements vides
        self.vider_pions()

        #self.fen.geometry("800x700") # Taille initiale de la fenêtre
        self.fen.mainloop()

    def fermer(self):
        self.fen.destroy()
        Accueil()

    def supprimer_pions(self):
        for col in self.pions:
            if col:
                for pion in col:
                    pion.supprimer()
        self.pions = []
        
    def vider_pions(self):
        self.supprimer_pions()
        
        # Création des emplacements libres
        for x in range(self.taille[0]):
            col = []
            for y in range(self.taille[1]):
                pion = Pion(self.canvas, x,y)
                col.append(pion)

                self.canvas.tag_bind(
                    pion.image,
                    "<Button-1>",
                    lambda event, i=x: self.placer_pion(i)
                )
            self.pions.append(col)
    
    def commencer_partie(self):
        if not self.debut:
            self.debut = True            # débute la partie
            self.vider_pions()           # enleve les pions précédants
            self.afficher_gagnant(False) # cache le gagnant précédant
            
            # Désactiver le changement de couleur
            for joueur in self.joueurs:
                joueur.btn_couleur.config(state=tk.DISABLED)
                # on redonne les pions à chaque joueurs
                joueur.redonner_pion()
                joueur.rafraichir_pions()

            # Passage au tour du premier joueur
            self.joueur_actuel = self.joueurs[1]
            self.tour_suivant()
        else:
            self.label.config(text="La partie a déjà commencé.")
    
    def placer_pion(self, x):
        if not self.debut:
            self.label.config(text="Cliquez sur 'Démarrer' pour commencer la partie")
            return

        # on cherche la position y libre en partant du bas
        y = self.taille[1]-1
        while y>=0 and self.pions[x][y].joueur != None:
            y -= 1

        # si le y trouvé n'est pas en dehors de la grille
        if y >= 0:
            # alors on place le pion
            pion = self.pions[x][y]
            pions_restants = pion.changer_joueur(self.joueur_actuel)
            
            # le pion placé a-t'il permit de gagner?
            if self.verifier_gagnant(x,y):
                self.afficher_gagnant(self.joueur_actuel) # joueur à gagné
            else:
                # vérifier match nul si tout les joueurs n'ont plus de pions en reserve
                nul = True
                for joueur in self.joueurs:
                    if joueur.pions_restants > 0:
                        nul = False
                
                if nul:
                    self.afficher_match_nul()
                else:
                    # tour suivant
                    self.tour_suivant()

    def tour_suivant(self):
        # Si le mode est en ligne, on attends le tour de l'autre joueur
        if self.internet:
            connection.attendre_tour(self, self.joueur_actuel.i)
        
        # Passage au joueur suivant
        i = 1 - self.joueur_actuel.i
        self.joueur_actuel = self.joueurs[i]

        # Actualise l'interface
        self.label.config(text = f"Tour de {self.joueur_actuel.nom}")
        self.surligner_joueur(self.joueur_actuel)

    def verifier_gagnant(self, x, y):
        directions = [(1, 0), (1,1), (0, 1), (-1, 1), (-1,0), (-1, -1), (0,-1), (1,-1)]
        #on regarde toutes les directions possible
        for dir_x, dir_y in directions:
            # On crée un compteur points_aligne initialement à 0
            pions_aligne = 0
            # On regarde 4 pions qui sont dans la même direction (dir_x, dir_y)
            for i in range(4):
                pos_x = x + dir_x*i
                pos_y = y + dir_y*i
                if 0 <= pos_x < self.taille[0] and 0 <= pos_y < self.taille[1]: # Si ils ne sont pas en dehors de la grille
                    if self.pions[pos_x][pos_y].joueur == self.joueur_actuel: # & Si ils sont du meme joueur
                        pions_aligne += 1 # On ajoute 1 au compteur points aligné

            # Si 4 pions sont alignés, le joueur a gagné
            if pions_aligne==4:
                return True
    
    def surligner_joueur(self, actuel):
        for joueur in self.joueurs:
            if actuel == joueur:
                # Met le label joueur qui doit jouer surligné en sa couleur lorsque c'est sont tour
                joueur.afficher_couleur(True)
            else:
                # Met le label joueur a qui ce n'est pas le tour de la couleur de base
                joueur.afficher_couleur(False)

    def partie_finie(self):
        self.debut = False
        
        # réactivation des boutons de couleurs
        for player in self.joueurs:
            player.btn_couleur.config(state='normal')

    def afficher_message(self, texte, couleur = 'black'):
        self.message_centre.config(text=texte, fg = couleur)
        #le message est placé au centre de l'écran
        self.message_centre.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def afficher_gagnant(self, joueur):
        self.label.config(text="") # enlever le texte d'informations
        if joueur:
            # afficher le nom du gagnant
            gagnant = self.joueur_actuel
            self.afficher_message(f"{gagnant.nom} a gagné!", gagnant.couleur)
            
            self.partie_finie()
        else:
            # cacher message du gagnant
            self.message_centre.place_forget()

    def afficher_match_nul(self):
        self.label.config(text="Match nul!")
        self.afficher_message("Match nul!")
        self.partie_finie()
        

        

        
    

if __name__ == "__main__":
    accueil = Accueil()


