from pymilvus import Collection, connections, MilvusException

def Print_Files_VDB(collection_name, MaxReturnResultShowFilsVDB):
    width = 100
    line = "═" * (width - 2)
    print("╔" + line + "╗")
    welcome_msg = "Connexion à la base de données et récupération des données uniques du champ 'Nom_Document'"
    welcome_msg = f"║ {welcome_msg: <{width-3}}║"  # Ajustement de l'espacement pour bien aligner avec le cadre
    print(welcome_msg)
    print("╠" + line + "╣")

    connections.connect("default", host="127.0.0.1", port="19530")

    try:
        collection = Collection(name=collection_name)
        collection.load()
        success_msg = f"Collection '{collection_name}' chargée avec succès."
        print(f"║ {success_msg: <{width-3}}║")
    except MilvusException as e:
        error_msg = f"Erreur Milvus : {e}"
        print(f"║ {error_msg: <{width-4}}║")
        return
    except Exception as e:
        general_error_msg = f"Erreur générale : {e}"
        print(f"║ {general_error_msg: <{width-3}}║")
        return

    field_name = "Nom_Document"
    schema = collection.schema

    if field_name not in [field.name for field in schema.fields]:
        not_found_msg = f"Le champ '{field_name}' n'est pas trouvé dans la collection '{collection_name}'."
        print(f"║ {not_found_msg: <{width-3}}║")
        return

    try:
        results = collection.query("", output_fields=[field_name], limit=MaxReturnResultShowFilsVDB)
        test_msg = f"Test - Nombre de documents trouvés : {len(results)}"
        print(f"║ {test_msg: <{width-3}}║")

        results = collection.query(expr=f"{field_name} != ''", output_fields=[field_name])
        results_msg = f"Nombre de résultats : {len(results)}"
        print(f"║ {results_msg: <{width-3}}║")
        
        values = set(result[field_name] for result in results if field_name in result)
        if values:
            for value in values:
                value_msg = f"{value}"
                print(f"║ {value_msg: <{width-3}}║")
        else:
            no_values_msg = "Aucune valeur unique trouvée."
            print(f"║ {no_values_msg: <{width-3}}║")
    except Exception as e:
        query_error_msg = f"Erreur lors de la requête : {e}"
        print(f"║ {query_error_msg: <{width-3}}║")

    print("╚" + line + "╝")
    print()  # Pour une ligne vide après le cadre
