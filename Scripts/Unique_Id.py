import time
import random

def Unique_Id():
    # Utilisez l'horodatage actuel et ajoutez un nombre aléatoire
    timestamp = int(time.time() * 1000)  # Horodatage en millisecondes
    random_number = random.randint(100, 999)  # Génère un nombre aléatoire entre 100 et 999
    return f"{timestamp}{random_number}"  # Concatène les deux pour former un ID unique

# Crée des IDs uniques
