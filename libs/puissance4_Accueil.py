
import tkinter as tk
import os

class Menu_Accueil:
    def __init__(self, fen, menu_suivant):
        """Menu d'accueil afin de choisir le mode de jeu"""

        # Fenêtre suivante à afficher
        self.menu_suivant = menu_suivant
        
        # Création ou réutilisation de la fenêtre tkinter
        self.nouvelle_fen = fen is None
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
        if self.internet():
            btn_internet = tk.Button(self.fen, image = img_btn_internet,
                                     command=self.demarrer_internet, bd=0)
        else:
            btn_internet = tk.Button(self.fen, image = img_btn_internet,
                                     command=self.demarrer_internet, bd=0,
                                     )
            btn_internet['state'] = 'disabled'
        btn_internet.image = img_btn_internet
        btn_internet.pack(pady=10)
        
        # Bouton Fermer
        img_btn_close = tk.PhotoImage(file = "assets/btnClose.png")
        btn_local = tk.Button(self.fen, image = img_btn_close, command=self.fermer, bd=0)
        btn_local.image = img_btn_close
        btn_local.place(relx=0, rely=0)

        if self.nouvelle_fen:
            self.nouvelle_fen = False
            self.fen.mainloop()
        
    def internet(self):
        """Le joueur peut il jouer en ligne? (requests installé?)"""
        try:
            import requests
            return True
        except Exception:
            return False

    def fermer(self):
        self.fen.destroy()
    
    def demarrer_local(self):
        """Démarrer le jeu Puissance 4 sans internet"""
        jeu = self.menu_suivant(self.fen, Menu_Accueil, False)
    
    def demarrer_internet(self):
        """Démarrer le jeu Puissance 4 avec internet activé"""
        jeu = self.menu_suivant(self.fen, Menu_Accueil, True)
