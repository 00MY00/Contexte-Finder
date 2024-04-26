import os
import re
import random

def Extract_Context(filepath, ResumWordSiz, FeirstContextTriger, MaxContextWords, VectorisAll):

    VectorisAll = VectorisAll.strip()

    if VectorisAll == 'False':
        mots_predefinis = FeirstContextTriger
        regex_mots_predefinis = '|'.join(map(re.escape, mots_predefinis))

        # Lire le contenu du fichier
        with open(filepath, 'r', encoding='utf-8') as file:
            texte = file.read()

        # Nettoyage et préparation du texte
        texte = re.sub(r'-', ' ', texte)
        texte = re.sub(r'[^\w\s]', '', texte).lower()

        # Séparation en mots et sélection basée sur la longueur
        mots = [mot for mot in texte.split() if len(mot) > int(ResumWordSiz)]
        mots_selectionnes = set()

        indices_utilises = set()
        index = 0
        while index < len(mots):
            mot = mots[index]
            if re.search(regex_mots_predefinis, mot) and index not in indices_utilises:
                for i in range(1, 4):
                    new_index = index + i
                    if new_index < len(mots) and new_index not in indices_utilises:
                        mots_selectionnes.add(mots[new_index])
                        indices_utilises.add(new_index)
            index += 1
            if len(mots_selectionnes) >= int(MaxContextWords) or index >= len(mots):
                break

        # Ajout de mots aléatoires si nécessaire pour atteindre le minimum requis
        while len(mots_selectionnes) < int(MaxContextWords) and len(mots) > len(mots_selectionnes):
            mots_selectionnes.add(random.choice(mots))

        # Extraire le nom de fichier nettoyé
        nom_fichier_nettoye = os.path.basename(filepath)
        nom_fichier_nettoye = re.sub(r'[-_]', ' ', nom_fichier_nettoye)
        nom_fichier_nettoye = re.sub(r'[.]', ' ', nom_fichier_nettoye)
        nom_fichier_nettoye = re.sub(r'[^\w\s]', '', nom_fichier_nettoye).lower()

        # Ajouter le nom du fichier aux mots sélectionnés
        resultat_final = nom_fichier_nettoye + ' ' + ' '.join(mots_selectionnes)

        return resultat_final


    if VectorisAll == 'True':
        # Lire le contenu du fichier
        with open(filepath, 'r', encoding='utf-8') as file:
            texte = file.read()

        # Nettoyage et préparation du texte
        texte = re.sub(r'-', ' ', texte)
        texte = re.sub(r'[^\w\s]', '', texte).lower()

        # Séparation en mots et sélection basée sur la longueur
        mots = [mot for mot in texte.split() if len(mot) >= int(ResumWordSiz)]
        mots_selectionnes = set(mots)  # Prend tous les mots qui respectent la condition de longueur

        # Ajout de mots aléatoires si nécessaire pour atteindre le minimum requis
        while len(mots_selectionnes) < int(MaxContextWords):
            mots_selectionnes.add(random.choice(mots))

        # Extraire le nom de fichier nettoyé
        nom_fichier_nettoye = os.path.basename(filepath)
        nom_fichier_nettoye = re.sub(r'[-_]', ' ', nom_fichier_nettoye)
        nom_fichier_nettoye = re.sub(r'[.]', ' ', nom_fichier_nettoye)
        nom_fichier_nettoye = re.sub(r'[^\w\s]', '', nom_fichier_nettoye).lower()

        # Ajouter le nom du fichier aux mots sélectionnés
        resultat_final = nom_fichier_nettoye + ' ' + ' '.join(mots_selectionnes)

        return resultat_final