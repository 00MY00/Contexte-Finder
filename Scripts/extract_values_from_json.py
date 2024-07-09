import re
import json

# def extract_values_from_json(datas, DBTables, key):
#     # Ajouter table distance
#     if 'distance' not in DBTables:
#         DBTables.append('Distance')

#     data_dict = {}
#     try:
#         # Convertir 'datas' en dictionnaire si c'est une chaîne
#         if isinstance(datas, str):
#             try:
#                 datas = json.loads(datas)
#             except json.JSONDecodeError:
#                 print(f"Erreur de décodage JSON : les données fournies ne sont pas un JSON valide : {datas}")
#                 return {}

#         # Afficher les clés disponibles pour le débogage
#         print("Clés disponibles dans les données fournies :", list(datas.keys()))

#         # Convertir les clés des données et la clé recherchée en minuscules pour la comparaison
#         datas_lower = {k.lower(): v for k, v in datas.items()}
#         key_lower = key.lower()

#         # Vérifier et diviser la clé en mots individuels
#         keys = key_lower.split()
#         data = {}
#         for k in keys:
#             if k in datas_lower:
#                 data[k] = datas_lower[k]
#             else:
#                 print(f"Erreur : La clé '{k}' n'est pas présente dans les données fournies.")
#                 return {}
#     except json.JSONDecodeError as e:
#         print("Erreur de décodage JSON:", e)
#         return {}
#     except TypeError as e:
#         print(f"Erreur de type lors de l'accès aux indices avec la clé '{key}', vérifiez la structure des données:", e)
#         return {}

#     # Fonction récursive pour chercher dans les structures imbriquées et collecter toutes les valeurs pour une clé
#     def find_all_keys(d, key, path=""):
#         results = []
#         if isinstance(d, dict) and key in d:
#             results.append(d[key])
#         elif isinstance(d, dict):
#             for k, v in d.items():
#                 new_path = f"{path}.{k}" if path else k
#                 if isinstance(v, dict):
#                     results.extend(find_all_keys(v, key, new_path))
#                 elif isinstance(v, list):
#                     for i, element in enumerate(v):
#                         if isinstance(element, dict):
#                             results.extend(find_all_keys(element, key, f"{new_path}[{i}]"))
#         return results

#     # Itération à travers chaque clé demandée pour extraire les données
#     for db_key in DBTables:
#         print(f"Recherche de la clé : '{db_key}'")  # Ajout pour débogage
#         values = []
#         for k in keys:
#             if k in data:
#                 values.extend(find_all_keys(data[k], db_key))
#         if values:
#             data_dict[db_key] = values if len(values) > 1 else values[0]
#         else:
#             print(f"Aucune valeur trouvée pour la clé : '{db_key}'")

#     return json.dumps(data_dict, indent=4)

def extract_values_from_json(datas, DBTables, key):
    # Ajouter table distance
    if 'distance' not in DBTables:
        DBTables.append('Distance')

    data_dict = {}
    keys_created = set()
    try:
        # Convertir 'datas' en dictionnaire si c'est une chaîne
        if isinstance(datas, str):
            try:
                datas = json.loads(datas)
            except json.JSONDecodeError:
                print(f"Erreur de décodage JSON : les données fournies ne sont pas un JSON valide : {datas}")
                return {}, []

        # Afficher les clés disponibles pour le débogage
        print("Clés disponibles dans les données fournies :", list(datas.keys()))

        # Convertir les clés des données et la clé recherchée en minuscules pour la comparaison
        datas_lower = {k.lower(): v for k, v in datas.items()}
        key_lower = key.lower()

        # Vérifier et diviser la clé en mots individuels
        keys = key_lower.split()
        data = {}
        for k in keys:
            if k in datas_lower:
                data[k] = datas_lower[k]
                keys_created.add(k)
            else:
                print(f"Erreur : La clé '{k}' n'est pas présente dans les données fournies.")
                return {}, []

    except json.JSONDecodeError as e:
        print("Erreur de décodage JSON:", e)
        return {}, []
    except TypeError as e:
        print(f"Erreur de type lors de l'accès aux indices avec la clé '{key}', vérifiez la structure des données:", e)
        return {}, []

    # Fonction récursive pour chercher dans les structures imbriquées et collecter toutes les valeurs pour une clé
    def find_all_keys(d, key, path=""):
        results = []
        if isinstance(d, dict) and key in d:
            results.append(d[key])
        elif isinstance(d, dict):
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
    for db_key in DBTables:
        print(f"Recherche de la clé : '{db_key}'")  # Ajout pour débogage
        values = []
        for k in keys:
            if k in data:
                values.extend(find_all_keys(data[k], db_key))
        if values:
            data_dict[db_key] = values if len(values) > 1 else values[0]
            keys_created.add(db_key)
        else:
            print(f"Aucune valeur trouvée pour la clé : '{db_key}'")

    return data_dict, list(keys_created)