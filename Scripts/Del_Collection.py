from pymilvus import connections, utility

def Del_Collection(collection_Name):
    try:
        # Connexion à Milvus
        connections.connect(host="127.0.0.1", port="19530")

        # Vérifie si la collection existe
        if utility.has_collection(collection_Name):
            # Supprime la collection
            utility.drop_collection(collection_Name)
            print(f"Collection existante '{collection_Name}' supprimée.")
        else:
            print(f"La collection '{collection_Name}' n'existe pas.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

# Utilisation de la fonction
#Del_Collection('test_collection') # nom de la collection