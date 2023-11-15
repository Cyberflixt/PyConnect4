
import tkinter as tk
from tkinter.colorchooser import askcolor

references = [] # tkinter supprime les images, si elles ne sont pas stockés, ez

class Joueur:
    def __init__(self, i):
        self.i = i
        self.pions_restants = 21
        
        colors = ["white", "red", "yellow"]
        self.couleur = colors[i]

class Pion:
    def __init__(self,canvas,x,y, couleur = "white"):
        self.canvas = canvas
        self.x = x
        self.y = y

        self.taille_pion = 60
        self.joueur = 0

        self.image = self.afficher_pion()

    def afficher_pion(self, couleur):
        px = self.x * self.taille_pion + 60
        py = self.y * self.taille_pion + 60
        pion = self.canvas.create_oval(
            px,
            py,
            px + self.taille_pion,
            py + self.taille_pion,
            outline = "black",
            fill = self.couleur
        )
        return pion

    def couleur_joueur(self, joueur):
        couleur = joueur.couleur
        
        self.joueur = joueur
        self.couleur = couleur
        self.image.config(fill = couleur)
        
        

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
        # Ajouter la logique pour le jeu en ligne ici
        pass

class Puissance4:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Puissance 4")
        
        self.pions = [[0] * 6 for i in range(7)] # 7 colonnes, 6 lignes
        self.taille = [7,6]
        

        self.taille_pion = 60 # pixels
        
        self.current_player = 0
        self.colors = {0: "white", 1: "red", 2: "yellow"}
        self.remaining_pions = {1: 21, 2: 21}
        self.started = False  # Variable pour suivre l'état de démarrage
        self.winner_message = None
        self.player_labels = {1: None, 2: None}
        
        self.create_gui()

    def creer_pion(self, x,y, couleur):
        px = x * self.taille_pion + 60
        py = y * self.taille_pion + 60
        pion = self.canvas.create_oval(
            px,
            py,
            px + self.taille_pion,
            py + self.taille_pion,
            outline = "black",
            fill = couleur
        )
        return pion
    
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
        left_pions = tk.Label(left_space, text=f"Pions restants: {self.remaining_pions[1]}", font=("Arial", 12))
        left_pions.pack()
        self.left_color_button = tk.Button(left_space, text="Choisir Couleur", command=lambda: self.choisir_couleur(1))
        self.left_color_button.pack()
        self.player_labels[1] = left_label
        
        # Espace pour "Joueur 2" à droite
        right_space = tk.Frame(self.window, width=50)
        right_space.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_label = tk.Label(right_space, text="Joueur 2", font=("Arial", 14))
        right_label.pack()
        right_pions = tk.Label(right_space, text=f"Pions restants: {self.remaining_pions[2]}", font=("Arial", 12))
        right_pions.pack()
        self.right_color_button = tk.Button(right_space, text="Choisir Couleur", command=lambda: self.choisir_couleur(2))
        self.right_color_button.pack()
        self.player_labels[2] = right_label
        
        self.label = tk.Label(self.window, text="Cliquez sur 'Démarrer' pour commencer la partie")
        self.label.pack()
        
        self.center_message = tk.Label(self.window, text="", font=("Arial", 20), bg="white", relief=tk.SOLID, borderwidth=2)
        self.center_message.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.center_message.place_forget()

        # création des emplacements libres
        for x in range(self.taille[0]):
            for y in range(self.taille[1]):
                emplacement = self.creer_pion(x,y,"white")
                
                self.canvas.tag_bind(
                    emplacement,
                    "<Button-1>",
                    lambda event, i=x: self.placer_pion(i)
                )
        
        self.window.geometry("800x700")  # Taille initiale de la fenêtre
        self.window.mainloop()
    
    def start_game(self):
        if not self.started:
            self.started = True
            self.current_player = 1  # Définir le premier joueur après le démarrage
            self.label.config(text=f"Tour du joueur 1")
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
        while y>=0 and self.pions[x][y] != 0:
            y -= 1

        # si le y trouvé n'est pas en dehors de la grille
        if y>=0:
            # alors on place le pion
            self.pions[x][y] = self.current_player
            self.creer_pion(x,y, self.colors[self.current_player])
            self.remaining_pions[self.current_player] -= 1

            # le pion placé a-t'il permit de gagner?
            if self.verifier_gagnant(x,y):
                # joueur à gagné
                self.afficher_gagnant()

            # pas de pion en reserve?
            elif sum(self.remaining_pions.values()) == 0:
                # match nul
                self.label.config(text="Match nul!")
                self.canvas.unbind("<Button-1>")
            else:
                # tour suivant
                self.current_player = 3 - self.current_player
                self.label.config(text=f"Tour du joueur {self.current_player}")
                self.show_player_label(self.current_player)

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
        directions = [(1, 0), (1,1), (0, 1), (-1, 1), (-1,0), (-1, -1), (0,-1), (1,-1)]
        for dir_x, dir_y in directions:
            pions_aligne = 0
            for i in range(4):
                pos_x = x + dir_x*i
                pos_y = y + dir_y*i
                if 0 <= pos_x < self.taille[0] and 0 <= pos_y < self.taille[1]:
                    if self.pions[pos_x][pos_y] == self.current_player:
                        pions_aligne += 1
                    #break # inutile de continuer si on cherche hors de la grille
                
            if pions_aligne==4:
                return True
    
    def show_player_label(self, player):
        for p in self.player_labels:
            if p == player:
                self.player_labels[p].config(bg=self.colors[player])
            else:
                self.player_labels[p].config(bg="SystemButtonFace")
    
    def afficher_gagnant(self):
        self.center_message.config(text=f"Joueur {self.current_player} a gagné!", fg=self.colors[self.current_player])
        self.center_message.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.canvas.unbind("<Button-1>")
    

if __name__ == "__main__":
    accueil = Accueil()


