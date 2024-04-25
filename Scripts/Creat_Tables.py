import torch
from gensim.models import KeyedVectors
from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections, utility
import numpy as np
import logging
import gensim.downloader as api


# Configuration des niveaux de journalisation pour ignorer les avertissements
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("gensim").setLevel(logging.ERROR)


# Vérifie si le modèle est déjà chargé et le charge si nécessaire
global model_w2v  # Déclare model_w2v comme variable globale
try:
    model_w2v
except NameError:  # Si model_w2v n'est pas défini, le charger
    from gensim import downloader as api
    model_w2v = api.load('word2vec-google-news-300')
    print("Modèle chargé avec succès.")
else:
    print("Modèle déjà chargé.")


def vectorize_text(text):
    """ Vectorise le texte en utilisant Word2Vec et retourne un vecteur moyen pour le texte entier. """
    words = text.split()
    valid_words = [word for word in words if word in model_w2v.key_to_index]
    if valid_words:
        word_vectors = np.array([model_w2v[word] for word in valid_words])
        vecteur_moyen = np.mean(word_vectors, axis=0)
        return vecteur_moyen.tolist()
    return [0] * model_w2v.vector_size

def Creat_Tables(collection_name, data, max_varchar_length=255):
    connections.connect("default", host="127.0.0.1", port="19530")

    if not utility.has_collection(collection_name):
        # Créez la collection avec un schéma approprié si elle n'existe pas
        fields = [
            FieldSchema(name="ID_Unique", dtype=DataType.INT64, is_primary=True, auto_id=True)
        ] + [
            FieldSchema(name=key, dtype=DataType.FLOAT_VECTOR, dim=model_w2v.vector_size) if "Vecteur" in key else
            FieldSchema(name=key, dtype=DataType.VARCHAR, max_length=max_varchar_length) for key in data[0] if key != "ID_Unique"
        ]
        schema = CollectionSchema(fields, description="Collection for testing")
        collection = Collection(name=collection_name, schema=schema)
        print("New collection created with updated schema.")
    else:
        # Utilisez la collection existante
        collection = Collection(name=collection_name)
        print(f"Collection '{collection_name}' already exists. Using existing schema.")

    # Préparer les données pour l'insertion
    columns = {field.name: [] for field in collection.schema.fields if field.name != "ID_Unique"}
    for item in data:
        for key, value in item.items():
            if key in columns:
                if "Vecteur" in key:
                    columns[key].append(vectorize_text(value))
                else:
                    columns[key].append(value)

    try:
        mr = collection.insert([columns[field.name] for field in collection.schema.fields if field.name != "ID_Unique"])
        print("Data inserted:", mr.primary_keys)
    except Exception as e:
        print(f"Error inserting data: {e}")


