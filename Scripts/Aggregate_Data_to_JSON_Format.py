import json

# def Aggregate_Data_to_JSON_Format(datas, DBTables):
#     # Si 'datas' est une chaîne, convertir en dictionnaire Python
#     if isinstance(datas, str):
#         data_dict = json.loads(datas)
#     elif isinstance(datas, dict):
#         data_dict = datas
#     else:
#         raise TypeError("Les données doivent être une chaîne JSON ou un dictionnaire.")

#     # Ajouter 'Distance' à DBTables si elle n'y est pas déjà
#     if 'Distance' not in DBTables:
#         DBTables.append('Distance')

#     # Collecter les clés disponibles dans les données
#     available_keys = data_dict.keys()
#     print(f"Clés disponibles dans les données fournies : {available_keys}")

#     # Filtrer DBTables pour inclure seulement les clés qui existent dans les données
#     filtered_db_tables = [key for key in DBTables if key in available_keys]
#     print(f"Clés filtrées : {filtered_db_tables}")

#     # Vérification pour s'assurer que toutes les listes ont la même longueur
#     lengths = [len(data_dict[key]) for key in filtered_db_tables if isinstance(data_dict[key], list)]
#     print(f"Longueurs des listes pour les clés filtrées : {lengths}")

#     if not lengths:
#         raise ValueError("Aucune des clés filtrées ne contient de liste.")
#     if not all(x == lengths[0] for x in lengths):
#         raise ValueError("Les listes de données n'ont pas la même longueur.")

#     # Création d'un nouveau dictionnaire pour le format désiré
#     result = {}

#     # Itérer sur les éléments de la liste par leur index
#     for i in range(lengths[0]):
#         id_unique = data_dict[filtered_db_tables[0]][i]  # Assumer que le premier élément de filtered_db_tables est l'ID unique
#         entry_data = {key: data_dict[key][i] for key in filtered_db_tables[1:] if i < len(data_dict[key])}  # Créer un sous-dictionnaire pour les autres données

#         # Structurer chaque ID avec les données associées
#         result[id_unique] = entry_data

#     # Convertir le résultat en JSON formaté pour une meilleure lisibilité
#     return json.dumps(result, indent=4)


def Aggregate_Data_to_JSON_Format(datas, DBTables):
    # Si 'datas' est une chaîne, convertir en dictionnaire Python
    print("1 : DBTables 2 : ", DBTables)
    if isinstance(datas, str):
        print("Les données sont une chaîne. Tentative de conversion en dictionnaire...")
        data_dict = json.loads(datas)
    elif isinstance(datas, dict):
        print("Les données sont déjà un dictionnaire.")
        data_dict = datas.copy()
    else:
        raise TypeError("Les données doivent être une chaîne JSON ou un dictionnaire.")

    print(f"Contenu des données après conversion : {data_dict}")

    # Ajouter 'Distance' à DBTables si elle n'y est pas déjà
    if 'Distance' not in DBTables:
        DBTables.append('Distance')

    # Collecter les clés disponibles dans les données
    available_keys = data_dict.keys()
    print(f"Clés disponibles dans les données fournies : {available_keys}")

    # Afficher les types de valeurs pour chaque clé et les premières valeurs
    for key in available_keys:
        print(f"Clé : {key}, Type de valeur : {type(data_dict[key])}, Exemples de valeurs : {data_dict[key][:5] if isinstance(data_dict[key], list) else data_dict[key]}")

    # Filtrer DBTables pour inclure seulement les clés qui existent dans les données
    filtered_db_tables = [key for key in DBTables if key in available_keys]
    print(f"Clés filtrées : {filtered_db_tables}")

    # Vérification pour s'assurer que toutes les listes ont la même longueur
    lengths = [len(data_dict[key]) for key in filtered_db_tables if isinstance(data_dict[key], list)]
    print(f"Longueurs des listes pour les clés filtrées : {lengths}")

    if not lengths:
        raise ValueError("Aucune des clés filtrées ne contient de liste.")
    if not all(x == lengths[0] for x in lengths):
        raise ValueError("Les listes de données n'ont pas la même longueur.")

    # Création d'un nouveau dictionnaire pour le format désiré
    result = {}

    # Itérer sur les éléments de la liste par leur index
    for i in range(lengths[0]):
        id_unique = data_dict[filtered_db_tables[0]][i]  # Assumer que le premier élément de filtered_db_tables est l'ID unique
        entry_data = {key: data_dict[key][i] for key in filtered_db_tables[1:] if i < len(data_dict[key])}  # Créer un sous-dictionnaire pour les autres données

        # Structurer chaque ID avec les données associées
        result[id_unique] = entry_data

    # Convertir le résultat en JSON formaté pour une meilleure lisibilité
    return json.dumps(result, indent=4)




