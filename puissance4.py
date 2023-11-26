
import math
import time
import random
import platform
import tkinter as tk
from tkinter.colorchooser import askcolor

from libs.puissance4_Jeu import Jeu
from libs.puissance4_Accueil import Menu_Accueil
from libs.puissance4_Serveur import Client


######################################################################


### CONTROLES DU JEU


class Controles_Jeu:
    def __init__(self, affichage_jeu):
        self.affichage = affichage_jeu

        # Quand la sourie bouge, on prévisualise la position où l'on peut poser un pion
        self.bind_sourie = affichage_jeu.fen.bind(
            '<Motion>',
            lambda event: self.mouvement_sourie(event.x)
        )
        
        # Quand on clique, on pose un pion
        self.bind_clique = affichage_jeu.fen.bind(
            '<Button-1>',
            lambda event: self.clique_sourie(event.x)
        )
        
    def fermer(self):
        """Déconnection les evenements"""
        fen = self.affichage.fen
        fen.unbind('<Motion>', self.bind_sourie)
        fen.unbind('<Button-1>', self.bind_clique)
        
    def colonne_grille(self, px):
        """Colonne de la sourie dans la grille"""
        # (position x dans la grille divisé par la taille d'un pion)
        return math.floor(
            (px-self.affichage.grille_x)/self.affichage.taille_pion
        )
        
    def mouvement_sourie(self, px):
        """Fonction appelé lors d'un mouvement de sourie,
        --> Prévisualisation de la position où placer"""

        x = self.colonne_grille(px)

        self.affichage.previsualisation_colonne(x)

    def clique_sourie(self, px):
        """Fonction appelé lors d'un clique de sourie
        --> Placement d'un pion sur la colonne cliquée"""

        x = self.colonne_grille(px)

        self.affichage.tester_colonne(x)


######################################################################


### AFFICHAGE DU JEU


class Affichage_Jeu:
    def __init__(self, fen, menu_precedent, internet):
        """Controle le jeu par une gui tkinter"""

        self.fen = fen # réutilisation de la fenetre tkinter
        self.menu_precedent = menu_precedent
        self.internet = internet
        
        # Utilisation de l'objet jeu
        self.jeu = Jeu(internet)
        self.controles = Controles_Jeu(self)
        
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
        self.pion_img_visual = tk.PhotoImage(file = "assets/iconPionVis.png")
        
        # Centre de la grille
        self.grille_x = 145
        self.grille_y = 60

        # Labels des joueurs
        self.labels_pions = []
        self.labels_nom = []
        self.couleurs = ["#E00000", "#EECC00"] # couleurs des joueurs par défaut
        self.joueurs_nom = ["Joueur 1", "Joueur 2"]
        
        self.en_jeu = False

        if internet:
            # On commence le traitement des informations pour le jeu
            self.internet_timeout = 3
            self.internet_timeout_tick = False
            self.internet_joueur_determine = False
            self.internet_commencer_autre = False
            self.internet_commencer_self = False

            # Nom de l'utilisateur du pc
            self.joueurs_nom[0] = platform.node()
            self.couleurs[0] = self.couleur_aleatoire()

            # Utilisation du serveur
            client.stop()
            client.cycle(traiter_serveur_jeu, self)
            client.envoyer({
                'couleur': self.couleurs[0],
                'name': self.joueurs_nom[0]
            })

        # Initialiser
        self.creer_gui()

    def couleur_aleatoire(self):
        """Renvoie un code couleur HTML aléatoire"""
        
        l = "456789ABCDEF"
        s = "#"
        for i in range(6):
            s += random.choice(l)
        return s
        
    
    def position_grille(self, x,y):
        """Donne la position en pixel des coordonnés dans la grille"""
        
        # Position en pixels
        px = x * self.taille_pion + self.grille_x
        py = y * self.taille_pion + self.grille_y

        return px,py
        
    def previsualisation_colonne(self, x):
        """Prévisualisation de la position où placer dans une colonne"""
        
        # supprimer la visualisation précédante si elle existe
        self.previsualisation_supprimer()
        
        if self.en_jeu:
            # visualiser la position où le pion sera placé
            y = self.jeu.position_colonne(x)
            if y is not None:
                couleur = self.couleurs[self.jeu.joueur_actuel]
                
                # Position en pixels
                px, py = self.position_grille(x,y)

                # Affichage de l'image de visualisation de la position
                pion = self.canvas.create_image(px, py, image = self.pion_img_visual, anchor = "nw")
                self.pion_visualisation = pion

    def previsualisation_supprimer(self):
        """Supprime la visualisation si elle existe"""
        if self.pion_visualisation:
            #if self.pion_visualisation in self.canvas.find_all():
            self.canvas.delete(self.pion_visualisation)
    
    def tester_colonne(self, x):
        """Place un pion dans la colonne X de la grille de jeu"""

        if self.en_jeu:
            # La position est-elle jouable ? (non-bloqué)
            
            y = self.jeu.position_colonne(x)
            if y is not None:

                # On envoie l'action si internet est activé
                if self.internet:
                    client.envoyer({
                        'placer': x,
                    })

                self.placer_colonne(x)
    
    def placer_colonne(self, x):
        """Place un pion"""
        y = self.jeu.placer_pion(x)
        
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
        if not self.internet or self.jeu.joueur_actuel==0:
            self.previsualisation_colonne(x)
                

                
    

    def creer_gui(self):
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
            label_nom = tk.Label(cadre, text="", font=("Arial", 14))
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

            if self.internet and i==1:
                btn_couleur['state'] = 'disabled'
            
        self.rafraichir_label_pions()
        self.rafraichir_noms()

        # Texte affichant l'aide
        self.label = tk.Label(self.fen, text="Cliquez sur 'Démarrer' pour commencer la partie")
        self.label.pack()

        # Message centré (affiché uniquement pour annoncer le gagnant)
        self.message_centre = tk.Label(self.fen, text="", font=("Arial", 20), bg="white", relief=tk.SOLID, borderwidth=2)

        # Bouton Retour
        img_btn_retour = tk.PhotoImage(file = "assets/btnRetour.png")
        btn_retour = tk.Button(self.fen, image = img_btn_retour, command = self.fermer, bd=0)
        btn_retour.image = img_btn_retour
        btn_retour.place(relx=0, rely=0)

        # Crée une grille de pions
        self.creer_grille()

    def rafraichir_noms(self):
        """Rafraichit les labels du nom des joueurs"""
        
        for i in range(2):
            label = self.labels_nom[i]
            nom = self.joueurs_nom[i]

            label.config(text = nom)
    
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
            self.rafraichir_couleur(joueur)

            if self.internet and joueur==0:
                client.envoyer({
                    'couleur': couleur,
                })
    
    def rafraichir_couleur(self, joueur):
        """Rafraichit la couleur des pions et les labels du joueur donnée"""
        
        self.afficher_couleur_joueur(joueur, True)
        for pion in self.pions_img[joueur]:
            self.canvas.itemconfig(pion, fill = self.couleurs[joueur])

    def fermer(self):
        """Ferme le jeu et retourne au menu principale"""
        
        self.partie_finie() # Arreter la partie
        client.stop() # Arreter l'accès au serveur
        if self.controles:
            self.controles.fermer() # Arreter les controles

        # Lancer le menu principal
        self.menu_precedent(self.fen, menu_suivant)

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
        """Initialise la partie, détermine quel joueur joue en premier"""
        
        if not self.en_jeu:
            if self.internet and not self.internet_joueur_determine:
                # Avec internet, on attends et on envoie un nombre aléatoire pour déterminer qui joue en premier
                if not self.internet_commencer_self:
                    x = random.randint(1,999999999)
                    self.internet_commencer_self = x

                # On regarde si le deuxième joueur est prêt
                if self.internet_commencer_autre:
                    # Deuxième joueur à confirmer
                    if self.internet_commencer_autre != self.internet_commencer_self:
                        # On compare notre nombre aléatoire et celui de l'autre joueur pour voir qui commence
                        commencer = self.internet_commencer_self > self.internet_commencer_autre
                        self.internet_commencer_tour = 0 if commencer else 1
                        self.internet_joueur_determine = True

                        # On envoie notre nombre pour que l'autre joueur fasse de même
                        client.envoyer({'commencer': self.internet_commencer_self})

                    # On réitère la fonction
                    self.commencer_partie()
                else:
                    # Premier joueur à confirmer
                    client.envoyer({'commencer': self.internet_commencer_self})
                    self.label.config(text="Attente du deuxième joueur...")
                
            else:
                # En local
                self.en_jeu = True           # débute la partie
                self.creer_grille()          # enleve les pions précédants
                self.afficher_gagnant(False) # cache le gagnant précédant

                # Initialistion du jeu
                self.jeu.initialiser()
                
                if self.internet:
                    # Joueur débutant la partie
                    self.jeu.joueur_actuel = self.internet_commencer_tour

                # Passage au tour du premier joueur
                self.tour_suivant()
        else:
            # Déjà en jeu
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

        # bloquer les controles ou non si internet est activé
        if self.internet:
            if self.jeu.joueur_actuel==0:
                if not self.controles:
                    self.controles = Controles_Jeu(self)
            else:
                if self.controles:
                    self.previsualisation_supprimer()
                    self.controles.fermer()
                    self.controles = False
        
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

        # Remise de valeurs par défaut pour internet
        self.internet_joueur_determine = False
        self.internet_commencer_autre = False
        self.internet_commencer_self = False


### Requete internet


def traiter_serveur_jeu(client, affichage):
    """Fonction appelée lorsque une information du serveur est reçu en jeu"""

    # Si la connection est valide
    if client.valide:
        affichage.internet_timeout_tick = False

        for data in client.data:
            # Nouvelles informations reçues

            # Changement de la couleur
            if 'couleur' in data:
                affichage.couleurs[1] = data['couleur']
                affichage.rafraichir_couleur(1)

            # Joueur prêt à commencer
            if 'commencer' in data:
                affichage.internet_commencer_autre = data['commencer']

                # Si le joueur est déjà prêt, on réappuit
                if not affichage.internet_joueur_determine:
                    if affichage.internet_commencer_self:
                        affichage.commencer_partie()
                    else:
                        affichage.label.config(text="Deuxième joueur prêt.")

            # Joueur a placé un pion
            if 'placer' in data:
                x = data['placer']
                affichage.jeu.joueur_actuel = 1
                affichage.placer_colonne(x)

            # Nom du joueur
            if 'name' in data:
                nom = data['name']
                affichage.joueurs_nom[1] = nom
                affichage.rafraichir_noms()
            
    else:
        # Connection interrompue
        if not affichage.internet_timeout_tick:
            affichage.internet_timeout_tick = time.time()

        # Interrompue pendant plus que 3s (internet_timeout)
        if time.time() - affichage.internet_timeout_tick > affichage.internet_timeout:
            affichage.fermer()


######################################################################


class Menu_Attente:
    def __init__(self, fen, menu_precedant, menu_suivant):
        """Crée le menu d'attente pendant qu'un autre joueur se connecte en multijoueur"""
        
        self.fen = fen
        self.menu_precedant = menu_precedant
        self.ouvert = True

        # On initialise l'accès au serveur
        client.cycle(traiter_serveur_attente, self)
        self.creer_gui()

    def creer_gui(self):
        """Crée l'interface tkinter du menu d'attente"""

        for elem in self.fen.winfo_children():
            elem.destroy()
        
        # Espace pour l'image en haut
        titre = tk.Label(self.fen, text="Recherche de joueurs\n...", font=("Arial", 20))
        titre.pack(fill=tk.BOTH, expand=True)
        
        self.desc = tk.Label(self.fen, text="...", font=("Arial", 14))
        self.desc.pack(fill=tk.BOTH, expand=True)

        # Bouton Retour
        img_btn_retour = tk.PhotoImage(file = "assets/btnRetour.png")
        btn_retour = tk.Button(self.fen, image = img_btn_retour, command = self.fermer, bd=0)
        btn_retour.image = img_btn_retour
        btn_retour.place(relx=0, rely=0)

    def fermer(self):
        """Retour au menu précédent et arrêt de l'accès au serveur"""
        client.stop()
        self.ouvert = False
        self.menu_precedant(self.fen, menu_suivant)

    def lancer(self):
        """Lance l'affichage du jeu avec internet activé"""
        Affichage_Jeu(self.fen, Menu_Accueil, True)

def traiter_serveur_attente(client, menu):
    """Fonction appelée lorsque une information du serveur est reçu en menu d'attente"""
    
    if menu.ouvert:
        # Affichage des informations annèxes dans le label de la fenêtre
        if client.recu:
            info = 'Serveur opérationel'
        else:
            info = 'Serveur déconnecté'

        info += f' (ping: {client.freq})\nStatus: {client.status[1]}'
        menu.desc.config(text = info)

        # Si la connection est valide, on démarre le jeu
        if client.valide:
            menu.lancer()


def menu_suivant(fen, menu_precedant, internet):
    """Passe au menu suivant à partir du menu principal"""
    
    if internet:
        # Lancé avec internet
        # --> Lance le Menu_Attente puis Affichage_Jeu
        Menu_Attente(fen, menu_precedant, Affichage_Jeu)
    else:
        # Lancé en local
        # --> Lance l'Affichage_Jeu
        Affichage_Jeu(fen, menu_precedant, False)

        
def initialisation(**options):
    global client
    
    # Création du client au serveur
    client = Client(
        'https://transfer.cyberflixt.repl.co',
        **options
    )

    Menu_Accueil(None, menu_suivant)


# Execution par défaut:
if __name__ == "__main__":
    initialisation(delai = 0)

