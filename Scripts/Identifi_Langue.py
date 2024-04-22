import re

def Identifi_Langue(filepath):
    mots_francais = {"le", "la", "et", "vous", "je", "suis", "les"}
    mots_allemand = {"der", "die", "das", "und", "ist", "du", "ich"}
    mots_italien = {"il", "la", "e", "tu", "io", "sono", "gli"}
    mots_anglais = {"the", "and", "you", "i", "are", "is", "of"}

    # Lire le contenu du fichier
    with open(filepath, 'r', encoding='utf-8') as file:
        texte = file.read()

    # Préparation du texte pour la comparaison
    mots_texte = set(re.sub(r'[^\w\s]', '', texte).lower().split())

    # Calcul des scores pour chaque langue
    scores = {
        "Français": sum(1 for mot in mots_texte if mot in mots_francais),
        "Allemand": sum(1 for mot in mots_texte if mot in mots_allemand),
        "Italien": sum(1 for mot in mots_texte if mot in mots_italien),
        "Anglais": sum(1 for mot in mots_texte if mot in mots_anglais)
    }

    # Détermination de la langue avec le score le plus élevé
    langue_max_score = max(scores, key=scores.get)

    return langue_max_score if scores[langue_max_score] > 0 else "Inconnue"


# Example
#config = Identifi_Langue('..\DOCs\Biographie_Fictive_Marie_Lefebvre.txt')   # Détecte la langue du fichier
#print(config)