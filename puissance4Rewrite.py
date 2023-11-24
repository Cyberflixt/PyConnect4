
import tkinter as tk
from tkinter.colorchooser import askcolor
import random
import math
#from puissance4Connection import Connection

#connection = Connection()

class Accueil:
    def __init__(self, fen = None):
        """Menu d'accueil afin de choisir le mode de jeu"""
        
        # Création ou réutilisation de la fenêtre tkinter
        if fen is None:
            self.fen = tk.Tk()
            self.fen.attributes('-fullscreen', True)
        else:
            self.fen = fen
        self.fen.title("Accueil")
        
        self.create_gui()
    
    def create_gui(self):
        """Création de l'apparence du menu principale"""
        
        for elem in self.fen.winfo_children():
            elem.destroy()
        
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
        jeu = AffichageJeu(self.fen) # Démarrer le jeu Puissance 4
    
    def demarrer_internet(self):
        jeu = AffichageJeu(self.fen, True) # Démarrer le jeu Puissance 4

class Jeu:
    def __init__(self, fen, internet = False):
        """Classe Jeu contenant les attributs et méthodes nécéssaires au fonctionnent basique du jeu"""
        
        self.internet = internet

        # Taille de la grille de jeu
        self.taille = [7,6]

        # Tableau de tableaux, remplit quand la partie commence
        self.pions = []
        
        self.joueur_actuel = 0
        self.pions_joueurs = [21, 21] # pions maximum des joueurs
        
        self.initialiser()
    
    def initialiser(self):
        """Initialise le tableau des pions"""

        # Remplissage de la liste pions par des -1
        self.pions = []
        for x in range(self.taille[0]):
            col = []
            for y in range(self.taille[1]):
                col.append(-1)
            self.pions.append(col)

        # Joueur aléatoire entre 0 et 1
        self.joueur_actuel = random.randint(0,1)
        self.pions_joueurs = [21, 21]

    def position_colonne(self, x):
        if 0 <= x < self.taille[0]:
            # On cherche la position y libre en partant du bas
            y = self.taille[1]-1
            while y>=0 and self.pions[x][y] != -1:
                y -= 1

            # Si le y trouvé n'est pas en dehors de la grille, on le renvoie
            if y>=0:
                return y
        
    def placer_pion(self, x):
        """Place un pion dans la colonne X, renvoie l'ordonné où le pion a été posé"""

        y = self.position_colonne(x)

        # on vérifie que la position est jouable
        if y is not None:
            
            # Alors on place le pion
            self.pions[x][y] = self.joueur_actuel
            # On enleve un pion au joueur
            self.pions_joueurs[self.joueur_actuel] -= 1
            
            return y

    def tour_suivant(self):
        """Passe le tour au joueur suivant"""
        
        # Si le mode est en ligne, on attends le tour de l'autre joueur
        #if self.internet:
            #connection.attendre_tour(self, self.joueur_actuel.i)
        
        # Passage au joueur suivant
        self.joueur_actuel = 1-self.joueur_actuel
    
    def verifier_match_nul(self):
        """Verification si le match est nul (aucun pions restants)"""
        
        # Un joueur a-t'il encore des pions?
        for pions in self.pions_joueurs:
            if pions > 0:
                return False # pas match nul
        
        return True # match nul

    def verifier_gagnant(self, x, y):
        """Vérification si le pion placé en (X;Y) à fait gagné un joueur"""
        directions = [(1, 0), (1,1), (0, 1), (-1, 1)]
        #on regarde toutes les directions possible
        for dir_x, dir_y in directions:
            # On crée un compteur points_aligne initialement à 0
            pions_aligne = 0
            # On regarde 4 pions qui sont dans la même direction (dir_x, dir_y)
            for i in range(-3,4):

                # On vérifie l'alignement avec les coordonnés plus loin dans la même direction
                pos_x = x + dir_x*i
                pos_y = y + dir_y*i
                
                if 0 <= pos_x < self.taille[0] and 0 <= pos_y < self.taille[1]: # Si ils ne sont pas en dehors de la grille
                    if self.pions[pos_x][pos_y] == self.joueur_actuel: # & Si ils sont du meme joueur
                        pions_aligne += 1 # On ajoute 1 au compteur points aligné

                    # Sinon, on remet les pions alignés à 0
                    else:
                        pions_aligne = 0
                else:
                    pions_aligne = 0

                # Si 4 pions sont alignés, le joueur a gagné
                if pions_aligne==4:
                    return self.joueur_actuel # On renvoie le joueur ayant gagné

        # Sinon, vérifier si c'est match nul
        if self.verifier_match_nul():
            return -1 # On renvoie -1 pour un match nul
        

######################################################################


class ControleJeu:
    def __init__(self, affichage_jeu):
        self.affichage = affichage_jeu

        # Quand la sourie bouge, on prévisualise la position où l'on peut poser un pion
        affichage_jeu.fen.bind(
            '<Motion>',
            lambda event: self.mouvement_sourie(event.x)
        )
        
        # Quand on clique, on pose un pion
        affichage_jeu.fen.bind(
            '<Button-1>',
            lambda event: self.clique_sourie(event.x)
        )

    def colonne_grille(self, px):
        """position de la sourie dans la grille"""
        return math.floor((px-self.affichage.grille_x)/self.affichage.taille_pion)
        
    def mouvement_sourie(self, px):
        """Fonction appelé lors d'un mouvement de sourie,
        --> Prévisualisation de la position où placer"""

        x = self.colonne_grille(px)

        self.affichage.previsualisation_colonne(x)

    def clique_sourie(self, px):
        """Fonction appelé lors d'un clique de sourie
        --> Placement d'un pion sur la colonne cliquée"""

        x = self.colonne_grille(px)

        self.affichage.placer_colonne(x)


######################################################################


class AffichageJeu:
    def __init__(self, fen, internet = False):
        """Controle le jeu par une gui tkinter"""

        self.fen = fen # réutilisation de la fenetre tkinter
        self.internet = internet
        
        # Utilisation de l'objet jeu
        self.jeu = Jeu(internet)
        self.controle = ControleJeu(self)
        
        
        # Changement du titre "local" ou "en ligne"
        self.internet = internet # mode en ligne
        if internet:
            self.fen.title("Puissance 4 Local")
        else:
            self.fen.title("Puissance 4 En ligne")

        # Images de pions
        self.taille_pion = 60 # pixels
        self.pions_img = []
        self.pion_visualisation = None
        self.pion_img_visual = tk.PhotoImage(file = "iconPionVis.png")
        
        # Centre de la grille
        self.grille_x = 145
        self.grille_y = 60

        # Labels des joueurs
        self.labels_pions = []
        self.labels_nom = []
        self.couleurs = ["#E00000", "#EECC00"] # couleurs des joueurs par défaut
        self.joueurs_nom = ["Joueur 1", "Joueur 2"]
        
        self.en_jeu = False

        # Initialiser
        self.create_gui()

    def position_grille(self, x,y):
        """Donne la position en pixel des coordonnés dans la grille"""
        
        # Position en pixels
        px = x * self.taille_pion + self.grille_x
        py = y * self.taille_pion + self.grille_y

        return px,py

    def previsualisation_colonne(self, x):
        """Prévisualisation de la position où placer dans une colonne"""
        
        if self.en_jeu:
            # supprimer la visualisation précédante
            if self.pion_visualisation:
                self.canvas.delete(self.pion_visualisation)
            
            # visualiser la position où le pion sera placé
            y = self.jeu.position_colonne(x)
            if y is not None:
                couleur = self.couleurs[self.jeu.joueur_actuel]
                
                # Position en pixels
                px, py = self.position_grille(x,y)

                # Affichage de l'image de visualisation de la position
                pion = self.canvas.create_image(px, py, image = self.pion_img_visual, anchor = "nw")
                self.pion_visualisation = pion

    def placer_colonne(self, x):
        """Place un pion dans la colonne X de la grille de jeu"""

        # La position est-elle jouable ? (non-bloqué)
        y = self.jeu.placer_pion(x)
        if self.en_jeu and not(y is None):
            
            # ajout du pion dans la liste d'image du joueur
            couleur = self.couleurs[self.jeu.joueur_actuel]
            pion = self.creer_image_pion(x, y, couleur)
            self.pions_img[self.jeu.joueur_actuel].append(pion)

            gagnant = self.jeu.verifier_gagnant(x, y)
            if gagnant is None:
                # Pas de fin, passer au tour suivant
                self.tour_suivant()
                
            elif gagnant == -1:
                # Match nul
                self.afficher_match_nul()
                
            else:
                # Victoire du joueur: gagnant
                self.afficher_gagnant(True)
            
            # actualiser la prévisualisation de la colonne
            self.previsualisation_colonne(x)
    

    def create_gui(self):
        """Crée l'interface utilisateur"""

        for elem in self.fen.winfo_children():
            elem.destroy()
        
        # Espace pour l'image en haut
        espace = tk.Frame(self.fen, height=50)
        espace.pack(fill=tk.BOTH, expand=True)
        
        # Bouton "Démarrer" pour commencer la partie
        btn_demarrer = tk.Button(espace, text="Démarrer", command=self.commencer_partie)
        btn_demarrer.pack(pady = 10)
        
        # Grille centrale
        self.canvas = tk.Canvas(self.fen, width=700, height=600)
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Création des élements symmétriques pour chaque joueur
        for i in range(2):

            # Coté de l'interface du joueur
            tk_side = tk.LEFT
            if i==1:
                tk_side = tk.RIGHT

            # Encadrage des elements
            cadre = tk.Frame(self.fen, width=50)
            cadre.pack(side=tk_side, fill=tk.BOTH, expand=True)

            # Texte avec le nom du joueur
            label_nom = tk.Label(cadre, text = self.joueurs_nom[i], font=("Arial", 14))
            label_nom.pack()

            # Texte avec le nombre de pions restants du joueur
            label_pions = tk.Label(cadre, text="", font=("Arial", 12))
            label_pions.pack()

            # Bouton pour changer la couleur du joueur
            fonction = lambda joueur=i: self.choisir_couleur(joueur)
            btn_couleur = tk.Button(cadre, text="Choisir Couleur", command = fonction)
            btn_couleur.pack()

            # Ajouter les labels à leurs liste
            self.labels_nom.append(label_nom)
            self.labels_pions.append(label_pions)
            
            # Afficher la couleur du joueur
            self.afficher_couleur_joueur(i, True)
            
        self.rafraichir_label_pions()

        # Texte affichant l'aide
        self.label = tk.Label(self.fen, text="Cliquez sur 'Démarrer' pour commencer la partie")
        self.label.pack()

        # Message centré (affiché uniquement pour annoncer le gagnant)
        self.message_centre = tk.Label(self.fen, text="", font=("Arial", 20), bg="white", relief=tk.SOLID, borderwidth=2)

        # Bouton Retour
        img_btn_retour = tk.PhotoImage(file = "btnRetour.png")
        btn_retour = tk.Button(self.fen, image = img_btn_retour, command = self.fermer, bd=0)
        btn_retour.image = img_btn_retour
        btn_retour.place(relx=0, rely=0)

        # Crée une grille de pions
        self.creer_grille()

    def afficher_couleur_joueur(self, joueur, afficher):
        """Affiche ou chache la couleur d'un joueur"""
        
        label = self.labels_nom[joueur]
        if afficher:
            # couleur du joueur
            label.config(bg = self.couleurs[joueur])
        else:
            # couleur par défaut d'un bouton
            label.config(bg = "SystemButtonFace")

    def rafraichir_label_pions(self):
        """Rafraichi les labels du nombre de pions"""
        
        for i in range(2):
            # pions restants
            restants = self.jeu.pions_joueurs[i]
            
            label = self.labels_pions[i]
            label.config(text = f"Pions restants: {restants}")

    def choisir_couleur(self, joueur):
        """Permet à un joueur de choisir la couleur de ses pions"""
        
        couleur = askcolor(title = f"Choisir une couleur pour {self.joueurs_nom[joueur]}")[1]
        if couleur:
            self.couleurs[joueur] = couleur
            self.afficher_couleur_joueur(joueur, True)

    def fermer(self):
        """Ferme le jeu et retourne au menu principale"""
        Accueil(self.fen)

    def vider_grille(self):
        """Supprime les pions placés"""
        self.canvas.delete("all")

        # Initialiser le tableau d'images de pions
        self.pions_img = [[],[]]
        
    def creer_grille(self):
        """Remplie la grille d'emplacement libre"""

        self.vider_grille()
        
        for x in range(self.jeu.taille[0]):
            for y in range(self.jeu.taille[1]):
                self.creer_image_pion(x,y)

    def creer_image_pion(self, x,y, couleur = None):
        """Crée l'image d'un pion dans la grille en position (X;Y) de couleur choisi"""

        bordure = "#404040"
        if couleur is None:
            couleur = "#CCCCCC"
            bordure = couleur

        # Position en pixels
        px, py = self.position_grille(x,y)

        # Crée un cercle au coordonnées calculées
        pion = self.canvas.create_oval(
            px,
            py,
            px + self.taille_pion,
            py + self.taille_pion,
            outline = bordure,
            fill = couleur
        )
        return pion

    def commencer_partie(self):
        if not self.en_jeu:
            self.en_jeu = True           # débute la partie
            self.creer_grille()          # enleve les pions précédants
            self.afficher_gagnant(False) # cache le gagnant précédant

            # Initialistion du jeu
            self.jeu.initialiser()

            # Passage au tour du premier joueur
            self.tour_suivant()
        else:
            self.label.config(text="La partie a déjà commencé.")
    
    def tour_suivant(self):
        self.jeu.tour_suivant()

        # afficher le nom du joueur qui doit joueur
        joueur = self.jeu.joueur_actuel
        self.label.config(text = f"Tour de {self.joueurs_nom[joueur]}")
        
        # afficher la couleur du joueur qui doit jouer
        for i in range(2):
            self.afficher_couleur_joueur(i, i == joueur)

        # rafraichit les labels du nombre de pions
        self.rafraichir_label_pions()
        
        
    def afficher_message(self, texte, couleur = 'black'):
        """Affichage du message au centre de l'écran avec le texte et couleur donnée"""
        
        self.message_centre.config(text=texte, fg = couleur)
        # On place le message au centre de l'écran
        self.message_centre.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def afficher_gagnant(self, afficher):
        """Affiche ou cache le message du gagnant"""
        self.label.config(text = "") # enlever le texte d'informations
        if afficher:
            # afficher le nom du gagnant
            gagnant = self.jeu.joueur_actuel
            self.afficher_message(f"{self.joueurs_nom[gagnant]} a gagné!", self.couleurs[gagnant])
            
            self.partie_finie()
            
        else:
            # cacher le nom du gagnant
            self.message_centre.place_forget()

    def afficher_match_nul(self):
        self.label.config(text = "Match nul!")
        self.afficher_message("Match nul!")
        self.partie_finie()
    
    def partie_finie(self):
        self.en_jeu = False
        


if __name__ == "__main__":
    accueil = Accueil()


