from pymilvus import Collection, utility, connections



def Find_Collection(collection_name):
    
    # Connexion Milvus
    connections.connect("default", host="127.0.0.1", port="19530")
    if utility.has_collection(collection_name):
        collection = Collection(name=collection_name)
        collection.load()  # Chargez la collection sans vérifier si elle est déjà chargée
        return True
    else:
        return False



# Example Test
# Find_Collection(collection_name)













