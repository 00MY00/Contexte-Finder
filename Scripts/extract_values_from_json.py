import re
import json


def extract_values_from_json(datas, DBTables, key):

    # Ajouter table distance
    if 'distance' not in DBTables:
        DBTables.append('Distance')

    
    data_dict = {}
    try:
        # Convertissons 'datas' en dictionnaire si c'est une chaîne
        if isinstance(datas, str):
            datas = json.loads(datas)
        # Utilisation de la clé fournie pour extraire les données JSON
        data = json.loads(datas[key])  # Cette ligne convertit le JSON contenu dans la clé spécifiée en dictionnaire
    except json.JSONDecodeError as e:
        print("Erreur de décodage JSON:", e)
        return {}
    except TypeError as e:
        print(f"Erreur de type lors de l'accès aux indices avec la clé '{key}', vérifiez la structure des données:", e)
        return {}

    # Fonction récursive pour chercher dans les structures imbriquées et collecter toutes les valeurs pour une clé
    def find_all_keys(d, key, path=""):
        results = []
        if key in d:
            #print(f"Trouvé {key} à {path}")
            results.append(d[key])
        for k, v in d.items():
            new_path = f"{path}.{k}" if path else k
            if isinstance(v, dict):
                results.extend(find_all_keys(v, key, new_path))
            elif isinstance(v, list):
                for i, element in enumerate(v):
                    if isinstance(element, dict):
                        results.extend(find_all_keys(element, key, f"{new_path}[{i}]"))
        return results

    # Itération à travers chaque clé demandée pour extraire les données
    for key in DBTables:
        #print("Recherche de la clé:", key)  # Débogage pour montrer la clé en cours de recherche
        values = find_all_keys(data, key)
        if values:
            data_dict[key] = values if len(values) > 1 else values[0]
            #print(f"Valeurs trouvées pour {key}:", values)  # Affiche les valeurs trouvées pour la clé
        #else:
            #print(f"Aucune valeur trouvée pour {key}")

    return json.dumps(data_dict, indent=4)
