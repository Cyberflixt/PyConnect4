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
        
        image = tk.PhotoImage(file="menu.png")
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
        puissance4 = Puissance4()  # Démarrer le jeu
    
    def start_online_game(self):
        # Ajouter la logique pour le jeu en ligne ici
        pass

class Puissance4:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Puissance 4")
        
        self.create_gui()
    
    def create_gui(self):
        # Espace pour l'image en haut
        top_space = tk.Frame(self.window, height=50)
        top_space.pack(fill=tk.BOTH, expand=True)
        
        # Bouton "Démarrer" pour commencer la partie
        start_button = tk.Button(top_space, text="Démarrer", command=self.start_game)
        start_button.pack()

if __name__ == "__main__":
    accueil = Accueil()
