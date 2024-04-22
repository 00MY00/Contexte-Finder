from pymilvus import Collection, utility, connections

def Creat_Index(collection_name, field_names, index_params):
    # Connexion à Milvus
    connections.connect("default", host="127.0.0.1", port="19530")
    
    # Vérifier si la collection existe déjà
    if utility.has_collection(collection_name):
        # Obtenez les informations sur la collection
        collection = Collection(name=collection_name)
        collection_info = collection.describe()
        existing_fields = [field['name'] for field in collection_info['fields']]
        
        # Créer l'index sur les champs spécifiés s'ils existent dans la collection
        for field_name in field_names:
            if field_name in existing_fields:
                try:
                    # Indexation des vecteurs et des métadonnées
                    collection.create_index(field_name, index_params)
                    print(f"Index créé avec succès sur le champ {field_name} de la collection {collection_name}.")
                except Exception as e:
                    print(f"Erreur lors de la création de l'index sur le champ {field_name}: {e}")
            else:
                print(f"Le champ {field_name} n'existe pas dans la collection {collection_name}.")
    else:
        print(f"La collection {collection_name} n'existe pas.")

# Exemple d'utilisation
# collection_name = "Nom_de_ta_collection"
# field_name = "Nom_de_ton_champ"
# index_params = {"index_type": "IVF_SQ8", "metric_type": "L2", "params": {"nlist": 16384}}

# Creat_Index(collection_name, field_name, index_params)










