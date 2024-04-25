from pymilvus import Collection, utility, connections, FieldSchema, DataType

def Creat_Index(collection_name, field_names, index_params):
    # Connexion à Milvus
    connections.connect("default", host="127.0.0.1", port="19530")
    
    if utility.has_collection(collection_name):
        # Obtenez les informations sur la collection
        collection = Collection(name=collection_name)
        
        # Décrire la collection pour obtenir le schéma
        schema = collection.schema
        
        # Créer l'index sur les champs spécifiés s'ils existent dans la collection et sont de type FLOAT_VECTOR
        for field_name in field_names:
            field = next((f for f in schema.fields if f.name == field_name and f.dtype == DataType.FLOAT_VECTOR), None)
            if field:
                try:
                    # Créer l'index si le champ est un champ vectoriel
                    collection.create_index(field_name, index_params)
                    print(f"Index créé avec succès sur le champ {field_name} de la collection {collection_name}.")
                except Exception as e:
                    print(f"Erreur lors de la création de l'index sur le champ {field_name}: {e}")
            else:
                print(f"Le champ {field_name} n'existe pas comme vecteur dans la collection {collection_name}.")
    else:
        print(f"La collection {collection_name} n'existe pas.")



