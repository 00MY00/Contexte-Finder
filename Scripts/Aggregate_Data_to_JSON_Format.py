import json


def Aggregate_Data_to_JSON_Format(datas, DBTables):
    # Convertir la chaîne en dictionnaire Python
    data_dict = json.loads(datas)
    
    # Ajouter 'Distance' à DBTables si elle n'y est pas déjà
    if 'Distance' not in DBTables:
        DBTables.append('Distance')
    
    # Collecter les clés disponibles dans les données
    available_keys = data_dict.keys()
    
    # Filtrer DBTables pour inclure seulement les clés qui existent dans les données
    filtered_db_tables = [key for key in DBTables if key in available_keys]

    # Vérification pour s'assurer que toutes les listes ont la même longueur
    lengths = [len(data_dict[key]) for key in filtered_db_tables if isinstance(data_dict[key], list)]
    if not all(x == lengths[0] for x in lengths):
        raise ValueError("Les listes de données n'ont pas la même longueur.")

    # Création d'un nouveau dictionnaire pour le format désiré
    result = {}

    # Itérer sur les éléments de la liste par leur index
    for i in range(lengths[0]):
        id_unique = data_dict[filtered_db_tables[0]][i]  # Assumer que le premier élément de filtered_db_tables est l'ID unique
        entry_data = {key: data_dict[key][i] for key in filtered_db_tables[1:]}  # Créer un sous-dictionnaire pour les autres données
        
        # Structurer chaque ID avec les données associées
        result[id_unique] = entry_data

    # Convertir le résultat en JSON formaté pour une meilleure lisibilité
    return json.dumps(result, indent=4)





