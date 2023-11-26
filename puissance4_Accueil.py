
import tkinter as tk

class Accueil:
    def __init__(self, suivant, fen = None):
        """Menu d'accueil afin de choisir le mode de jeu"""

        # Fenêtre suivante à afficher
        self.suivant = suivant
        
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
        image = tk.PhotoImage(file="assets/menu.png") 
        image_menu = tk.Label(self.fen, image=image)
        image_menu.image = image
        image_menu.pack()
        
        # Bouton "Jouer Local"
        img_btn_local = tk.PhotoImage(file = "assets/btnLocal.png")
        btn_local = tk.Button(self.fen, image = img_btn_local, command=self.demarrer_local, bd=0)
        btn_local.image = img_btn_local
        btn_local.pack()
        
        # Bouton "Jouer En Ligne"
        img_btn_internet = tk.PhotoImage(file = "assets/btnOnline.png")
        btn_internet = tk.Button(self.fen, image = img_btn_internet, command=self.demarrer_internet, bd=0)
        btn_internet.image = img_btn_internet
        btn_internet.pack(pady=10)

        
        # Bouton Fermer
        img_btn_close = tk.PhotoImage(file = "assets/btnClose.png")
        btn_local = tk.Button(self.fen, image = img_btn_close, command=self.fermer, bd=0)
        btn_local.image = img_btn_close
        btn_local.place(relx=0, rely=0)

    def fermer(self):
        self.fen.destroy()
    
    def demarrer_local(self):
        jeu = self.suivant(self.fen) # Démarrer le jeu Puissance 4
    
    def demarrer_internet(self):
        jeu = self.suivant(self.fen, True) # Démarrer le jeu Puissance 4
