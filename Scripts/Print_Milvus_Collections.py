from pymilvus import connections, Collection, utility
def Print_Milvus_Collections(collection_name):
    width = 80
    line = "═" * (width - 2)
    print("╔" + line + "╗")
    
    # Connexion à Milvus
    connections.connect("default", host="127.0.0.1", port="19530")
    
    # Vérifier si la collection existe
    if not utility.has_collection(collection_name):
        error_msg = f"Collection '{collection_name}' does not exist."
        error_msg = f"{error_msg:{' '}<{width-2}} ║"
        print(error_msg)
    else:
        try:
            # Récupération de la collection
            collection = Collection(name=collection_name)
            schema = collection.schema
            
            # Affichage du nom de la collection
            collection_header = f"║ Fields in collection '{collection_name}':"
            collection_header = f"{collection_header:{' '}<{width-2}} ║"
            print(collection_header)

            # Affichage des champs de la collection
            for field in schema.fields:
                field_info = f"║ Field Name: {field.name}, Field Type: {field.dtype}"
                field_info = f"{field_info:{' '}<{width-2}} ║"
                print(field_info)

            # Ligne vide pour la symétrie
            empty_line = "║" + " " * (width - 2) + "║"
            print(empty_line)

        except Exception as e:
            error_msg = f"An error occurred: {e}"
            error_msg = f"{error_msg:{' '}<{width-2}} ║"
            print(error_msg)

    # Répétition de la ligne supérieure/inférieure pour fermer le cadre
    print("╚" + line + "╝")
    print()  # Pour une ligne vide après le cadre
