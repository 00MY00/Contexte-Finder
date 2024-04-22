from pymilvus import Collection, connections, utility, MilvusException

def Print_Files_VDB(DBTabls, collection_name):
    width = 100
    line = "═" * (width - 2)
    print("╔" + line + "╗")
    welcome_msg = "║ Connexion à la base de données et récupération des données uniques du champ 'Nom_Document'"
    welcome_msg = f"{welcome_msg:{' '}<{width-2}} ║"
    print(welcome_msg)
    print("╚" + line + "╝")

    # Connexion à la base de données Milvus
    connections.connect("default", host="127.0.0.1", port="19530")

    try:
        collection = Collection(name=collection_name)
        
        # Vérification si la collection est chargée
        try:
            # Utilisez directement collection.load() sans vérifier is_loaded() car cela provoquait des erreurs dans les versions précédentes
            collection.load()
            #print(f"║ Collection '{collection_name}' chargée avec succès.")
        except Exception as e:
            print(f"║ Erreur lors du chargement de la collection '{collection_name}': {e}")
            return
        
        schema = collection.schema
    except MilvusException as e:
        print(f"Erreur lors de la récupération du schéma de la collection '{collection_name}': {e}")
        return None
    except Exception as e:
        print(f"Erreur générale lors de la récupération de la collection '{collection_name}': {e}")
        return None

    field_name = "Nom_Document"
    field_names = [field.name for field in schema.fields]
    if field_name not in field_names:
        error_msg = f"║ Le champ '{field_name}' n'est pas trouvé dans la collection '{collection_name}'."
        error_msg = f"{error_msg:{' '}<{width-2}} ║"
        print(error_msg)
        print("╔" + line + "╗")
        return
    
    try:
        expr = f"{field_name} != ''"
        results = collection.query(expr=expr, output_fields=[field_name])
        result_msg = f"║ Nombre de résultats : {len(results)}"
        result_msg = f"{result_msg:{' '}<{width-2}} ║"
        print(result_msg)
        print("═" + line + "═")

        values = set(result[field_name] for result in results)  # Utiliser un ensemble pour éviter les doublons
        if not values:
            no_values_msg = "║ Aucune valeur unique trouvée."
            no_values_msg = f"{no_values_msg:{' '}<{width-2}} ║"
            print(no_values_msg)
        else:
            for value in values:
                value_msg = f"║ {value}"
                value_msg = f"{value_msg:{' '}<{width-2}} ║"
                print(value_msg)
    except Exception as e:
        error_msg = f"║ Une erreur est survenue lors de la requête : {e}"
        error_msg = f"{error_msg:{' '}<{width-2}} ║"
        print(error_msg)

    print("╚" + line + "╝")
    print()  # Pour une ligne vide après le cadre
