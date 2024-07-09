import re
import os


# Suporte un chemin ou du texte directement

def Identifi_Langue(filepath):
    mots_francais = {"le", "la", "et", "vous", "je", "suis", "les"}
    mots_allemand = {"der", "die", "das", "und", "ist", "du", "ich"}
    mots_italien = {"il", "la", "e", "tu", "io", "sono", "gli"}
    mots_anglais = {"the", "and", "you", "i", "are", "is", "of"}

    # Vérifier si filepath est un chemin de fichier valide
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            texte = file.read()
    else:
        # Sinon, considérer filepath comme étant le texte
        texte = filepath

    # Préparation du texte pour la comparaison
    mots_texte = set(re.sub(r'[^\w\s]', '', texte).lower().split())

    # Calcul des scores pour chaque langue
    scores = {
        "fr": sum(1 for mot in mots_texte if mot in mots_francais),
        "de": sum(1 for mot in mots_texte if mot in mots_allemand),
        "it": sum(1 for mot in mots_texte if mot in mots_italien),
        "en": sum(1 for mot in mots_texte if mot in mots_anglais)
    }

    # Détermination de la langue avec le score le plus élevé
    langue_max_score = max(scores, key=scores.get)

    return langue_max_score if scores[langue_max_score] > 0 else "Inconnue"


