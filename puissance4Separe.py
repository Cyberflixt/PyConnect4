
import tkinter as tk
from tkinter.colorchooser import askcolor
from puissance4Classes import *

references = [] # tkinter supprime les images, si elles ne sont pas stockés, ez

class Accueil:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Accueil")
        
        self.create_gui()
    
    def create_gui(self):
        # Ecran d'accueil avec image au milieu
        welcome_label = tk.Label(self.window, text="", font=("Arial", 20))
        welcome_label.pack()
        
        image = tk.PhotoImage(file="menu.png") 
        image_label = tk.Label(self.window, image=image)
        image_label.image = image
        image_label.pack()
        
        # Bouton "Jouer Local"
        photo1 = tk.PhotoImage(file = "btnLocal.png")
        references.append(photo1)
        photo2 = tk.PhotoImage(file = "btnOnline.png")
        references.append(photo2)
        play_local_button = tk.Button(self.window, image = photo1, command=self.start_local_game)
        play_local_button.pack()
        
        # Bouton "Jouer En Ligne"
        play_online_button = tk.Button(self.window, image = photo2, command=self.start_online_game)
        play_online_button.pack()
    
    def start_local_game(self):
        self.window.destroy()  # Fermer la fenêtre d'accueil
        puissance4 = Puissance4()  # Démarrer le jeu Puissance 4
    
    def start_online_game(self):
        # 
        pass

class Puissance4:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Puissance 4")
        
        self.pions = []
        self.taille = [7,6]
        

        self.taille_pion = 60 # pixels

        # crée le joueur 1 et le joueur 2
        self.joueurs = [Joueur(self, i) for i in range(2)]
        
        self.joueur_actuel = self.joueurs[0]
        self.started = False  # Variable pour suivre l'état de démarrage
        self.winner_message = None
        
        self.create_gui()
    
    def create_gui(self):
        # Espace pour l'image en haut
        top_space = tk.Frame(self.window, height=50)
        top_space.pack(fill=tk.BOTH, expand=True)
        
        # Bouton "Démarrer" pour commencer la partie
        start_button = tk.Button(top_space, text="Démarrer", command=self.start_game)
        start_button.pack()
        
        # Grille centrale
        self.canvas = tk.Canvas(self.window, width=700, height=600)
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Espace pour "Joueur 1" à gauche
        left_space = tk.Frame(self.window, width=50)
        left_space.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        left_label = tk.Label(left_space, text="Joueur 1", font=("Arial", 14))
        left_label.pack()
        left_pions = tk.Label(left_space, text=f"Pions restants: {self.joueurs[0].pions_restants}", font=("Arial", 12))
        left_pions.pack()
        self.left_color_button = tk.Button(left_space, text="Choisir Couleur", command=lambda: self.choisir_couleur(1))
        self.left_color_button.pack()
        self.joueurs[0].label = left_label
        
        # Espace pour "Joueur 2" à droite
        right_space = tk.Frame(self.window, width=50)
        right_space.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_label = tk.Label(right_space, text="Joueur 2", font=("Arial", 14))
        right_label.pack()
        right_pions = tk.Label(right_space, text=f"Pions restants: {self.joueurs[1].pions_restants}", font=("Arial", 12))
        right_pions.pack()
        self.right_color_button = tk.Button(right_space, text="Choisir Couleur", command=lambda: self.choisir_couleur(2))
        self.right_color_button.pack()
        self.joueurs[1].label = right_label
        
        self.label = tk.Label(self.window, text="Cliquez sur 'Démarrer' pour commencer la partie")
        self.label.pack()
        
        self.center_message = tk.Label(self.window, text="", font=("Arial", 20), bg="white", relief=tk.SOLID, borderwidth=2)
        self.center_message.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.center_message.place_forget()

        # création des emplacements libres
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
        
        self.window.geometry("800x700")  # Taille initiale de la fenêtre
        self.window.mainloop()
    
    def start_game(self):
        if not self.started:
            self.started = True
            
            # Définir le premier joueur après le démarrage
            self.joueur_actuel = self.joueurs[0]
            self.label.config(text=f"Tour du {self.joueur_actuel.nom}")

            # Désactiver le changement de couleur
            self.left_color_button.config(state=tk.DISABLED)
            self.right_color_button.config(state=tk.DISABLED)
            self.show_player_label(1)
        else:
            self.label.config(text="La partie a déjà commencé.")
    
    def placer_pion(self, x):
        if not self.started:
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
            pions_restant = pion.changer_joueur(self.joueur_actuel)
            
            # le pion placé a-t'il permit de gagner?
            if self.verifier_gagnant(x,y):
                self.afficher_gagnant() # joueur à gagné

            # pas de pion en reserve?
            elif pions_restant == 0:
                # match nul
                self.label.config(text="Match nul!")
                self.canvas.unbind("<Button-1>")
            else:
                # tour suivant
                self.tour_suivant()
    
    def tour_suivant(self):
        # tour suivant
        i = 1 - self.joueur_actuel.i
        self.joueur_actuel = self.joueurs[i]

        # actualiser l'interface
        self.label.config(text="Tour de "+self.joueur_actuel.nom)
        self.show_player_label(self.joueur_actuel)
                
    def choisir_couleur(self, player):
        if not self.started:
            color = askcolor(title=f"Choisir une couleur pour Joueur {player}")[1]
            if color:
                self.colors[player] = color
                if player == 1:
                    self.left_color_button.config(state=tk.DISABLED)
                else:
                    self.right_color_button.config(state=tk.DISABLED)
        else:
            self.label.config(text="La partie a déjà commencé. Impossible de changer de couleur.")

    def verifier_gagnant(self, x, y):
        directions = [(1, 0), (1,1), (0, 1), (-1, 1), (-1,0), (-1, -1), (0,-1), (1,-1)]#on regarde toutes les directions possible
        for dir_x, dir_y in directions:
            pions_aligne = 0 #on créer un compteur points_aligne initialement à 0
            for i in range(4): #on regarde 4 pionts qui sont dans la même direction
                pos_x = x + dir_x*i #on regarde toutes les directions x ainsi que toutes les directions autour de x
                pos_y = y + dir_y*i #on regarde toutes les directions y ainsi que toutes les directions autour de y
                if 0 <= pos_x < self.taille[0] and 0 <= pos_y < self.taille[1]: #si ils ne sont pas en dehors de la grille
                    if self.pions[pos_x][pos_y].joueur == self.joueur_actuel: #si ils sont du meme joueur
                        pions_aligne += 1  #on ajoute 1 au compteur points aligné
            # Si 4 pions sont alignés, le joueur a gagné
            if pions_aligne==4:
                return True
    
    def show_player_label(self, actuel):
        for joueur in self.joueurs:
            if actuel == joueur:
                joueur.label.config(bg = joueur.couleur) #met le label joueur qui doit jouer surligné en sa couleur lorsque c'est sont tour
            else:
                joueur.label.config(bg = "SystemButtonFace")#Met le label joueur a qui ce n'est pas le tour de la couleur de base
    
    def afficher_gagnant(self):
        self.center_message.config(text=f"{self.joueur_actuel.nom} a gagné!", fg = self.joueur_actuel.couleur)#le joueur qui a gagné est le joueur qui vient de placer le pion, donc le joueur actuel est appelé pour la victoire
        self.center_message.place(relx=0.5, rely=0.5, anchor=tk.CENTER)#le message est placé au centre de l'écran
        self.canvas.unbind("<Button-1>") #on empeche le joueur de placer des pions lorsque l'écran de victoire est actif
    

if __name__ == "__main__":
    accueil = Accueil()


