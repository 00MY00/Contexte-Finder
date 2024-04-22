import time

def Unique_Id():
    # Utilisez l'horodatage actuel pour générer une clé unique
    return str(int(time.time() * 1000))  # Convertit le timestamp en millisecondes en chaîne de caractères


# Crée des IDs unique