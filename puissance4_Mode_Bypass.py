
"""

### /!\ Pour le wifi de l'école

Variante du programme de base,

Lance le programme avec les paramêtres nécéssaires
afin de lancer le mode multijoeur avec la librairie selenium
et d'autres modification au client

"""

# On importe le fichier puissance4 principal
from puissance4 import initialisation

# On utilise la fonction d'initialisation avec bypass = True
initialisation(
    delai = 0,
    bypass = True,
    headless = False,
)

