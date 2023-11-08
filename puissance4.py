import tkinter as tk
from tkinter.colorchooser import askcolor


class Accueil:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Accueil")
        
        self.create_gui()
    
    def create_gui(self):
        # Ecran d'accueil avec image au milieu
        welcome_label = tk.Label(self.window, text="", font=("Arial", 20))
        welcome_label.pack()
        
        image = tk.PhotoImage(file="ratspin.gif")  # Remplacez "your_image.gif" par le chemin de votre image
        image_label = tk.Label(self.window, image=image)
        image_label.image = image
        image_label.pack()
        
        # Bouton "Jouer Local"
        play_local_button = tk.Button(self.window, text="Jouer Local", command=self.start_local_game)
        play_local_button.pack()
        
        # Bouton "Jouer En Ligne"
        play_online_button = tk.Button(self.window, text="Jouer En Ligne", command=self.start_online_game)
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
        self.board = [[0] * 7 for _ in range(6)]
        self.current_player = 0
        self.colors = {0: "white", 1: "red", 2: "yellow"}
        self.remaining_pions = {1: 21, 2: 21}
        self.started = False  # Variable pour suivre l'état de démarrage
        self.winner_message = None
        self.player_labels = {1: None, 2: None}
        
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
        left_pions = tk.Label(left_space, text=f"Pions restants: {self.remaining_pions[1]}", font=("Arial", 12))
        left_pions.pack()
        self.left_color_button = tk.Button(left_space, text="Choisir Couleur", command=lambda: self.choose_color(1))
        self.left_color_button.pack()
        self.player_labels[1] = left_label
        
        # Espace pour "Joueur 2" à droite
        right_space = tk.Frame(self.window, width=50)
        right_space.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_label = tk.Label(right_space, text="Joueur 2", font=("Arial", 14))
        right_label.pack()
        right_pions = tk.Label(right_space, text=f"Pions restants: {self.remaining_pions[2]}", font=("Arial", 12))
        right_pions.pack()
        self.right_color_button = tk.Button(right_space, text="Choisir Couleur", command=lambda: self.choose_color(2))
        self.right_color_button.pack()
        self.player_labels[2] = right_label
        
        self.label = tk.Label(self.window, text="Cliquez sur 'Démarrer' pour commencer la partie")
        self.label.pack()
        
        self.center_message = tk.Label(self.window, text="", font=("Arial", 20), bg="white", relief=tk.SOLID, borderwidth=2)
        self.center_message.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.center_message.place_forget()
        
        for i in range(6):
            for j in range(7):
                self.canvas.create_oval(60 * j + 10, 60 * i + 60, 60 * j + 70, 60 * i + 120, outline="black", fill="white")
                self.canvas.tag_bind(self.canvas.create_oval(60 * j + 10, 60 * i + 60, 60 * j + 70, 60 * i + 120, outline="black", fill="white"),
                    "<Button-1>", lambda event, row=i, col=j: self.drop_pion(col))
        
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
    
    def drop_pion(self, col):
        print(self.current_player)
        if not self.started:
            self.label.config(text="Cliquez sur 'Démarrer' pour commencer la partie")
            return

        for i in range(5, -1, -1):
            if self.board[i][col] == 0:
                self.board[i][col] = self.current_player
                self.canvas.create_oval(60 * col + 10, 60 * i + 60, 60 * col + 70, 60 * i + 120, outline="black", fill=self.colors[self.current_player])
                self.remaining_pions[self.current_player] -= 1
                
                if self.check_win(i, col):
                    self.display_winner()
                elif sum(self.remaining_pions.values()) == 0:
                    self.label.config(text="Match nul!")
                    self.canvas.unbind("<Button-1>")
                else:
                    self.current_player = 3 - self.current_player
                    self.label.config(text=f"Tour du joueur {self.current_player}")
                    self.show_player_label(self.current_player)
                break
    
    def choose_color(self, player):
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
    
    def check_win(self, row, col):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for sign in [-1, 1]:
                r, c = row, col
                while 0 <= r + dr * sign < 6 and 0 <= c + dc * sign < 7 and self.board[r + dr * sign][c + dc * sign] == self.current_player:
                    count += 1
                    r, c = r + dr * sign, c + dc * sign
                    if count >= 4:
                        return True
        return False
    
    def show_player_label(self, player):
        for p in self.player_labels:
            if p == player:
                self.player_labels[p].config(bg=self.colors[player])
            else:
                self.player_labels[p].config(bg="SystemButtonFace")
    
    def display_winner(self):
        self.center_message.config(text=f"Joueur {self.current_player} a gagné!", fg=self.colors[self.current_player])
        self.center_message.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.canvas.unbind("<Button-1>")

if __name__ == "__main__":
    accueil = Accueil()
