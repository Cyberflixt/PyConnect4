
import random
import math

class Jeu:
    def __init__(self, fen):
        """Classe Jeu contenant les attributs et méthodes nécéssaires au fonctionnent basique du jeu"""

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
        """Renvoie l'ordonné où placer un pion dans une colonne"""
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
        

