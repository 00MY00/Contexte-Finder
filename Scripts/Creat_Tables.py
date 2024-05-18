import torch
from gensim.models import KeyedVectors
from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections, utility
import numpy as np
import logging
import gensim.downloader as api
import os
import urllib.request
import time

def download_model_file(model_name, url):
    """Télécharge un fichier de modèle si nécessaire avec une barre de progression."""
    def progress_callback(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percentage = min(100, downloaded * 100 / total_size)
        print(f"\rTéléchargement de {model_name}: {percentage:.2f}% complet", end='')

    if not os.path.exists(model_name):
        print(f"Téléchargement du modèle {model_name} depuis {url}")
        start_time = time.time()
        urllib.request.urlretrieve(url, model_name, reporthook=progress_callback)
        end_time = time.time()
        print(f"\nModèle {model_name} téléchargé avec succès en {end_time - start_time:.2f} secondes.")
    else:
        print(f"Modèle {model_name} déjà présent localement.")
        # Vérification de la taille du fichier
        downloaded_size = os.path.getsize(model_name)
        remote_file_info = urllib.request.urlopen(url).info()
        remote_size = int(remote_file_info['Content-Length'])
        if downloaded_size != remote_size:
            print(f"Taille du fichier local ({downloaded_size} octets) ne correspond pas à la taille distante ({remote_size} octets).")
            user_input = input("Le fichier semble être corrompu. Voulez-vous le supprimer et retélécharger? (oui/non) : ")
            if user_input.lower() == 'oui':
                os.remove(model_name)
                print(f"Fichier {model_name} supprimé. Redémarrage du téléchargement.")
                download_model_file(model_name, url)
            else:
                print("Vous avez choisi de continuer malgré le fichier potentiellement corrompu.")

def StartCreat_Tables(VectorModelFile):
    # Configuration des niveaux de journalisation pour ignorer les avertissements
    logging.getLogger("transformers").setLevel(logging.ERROR)
    logging.getLogger("gensim").setLevel(logging.ERROR)

    # Convertir la liste plate en une liste de tuples
    it = iter(VectorModelFile)
    VectorModelFile = list(zip(it, it))

    # Vérifie si le modèle est déjà chargé et le charge si nécessaire
    global model_w2v  # Déclare model_w2v comme variable globale
    if 'model_w2v' not in globals():  # Si model_w2v n'est pas défini, le charger
        model_w2v = {}
        for model_name, url in VectorModelFile:
            download_model_file(model_name, url)
            print(f"Chargement du modèle '{model_name}'...")
            start_time = time.time()
            model = KeyedVectors.load_word2vec_format(model_name, binary=False)
            end_time = time.time()
            model_w2v[model_name] = model
            print(f"Modèle '{model_name}' chargé avec succès en {end_time - start_time:.2f} secondes.")
    else:
        print("Modèles déjà chargés.")

def vectorize_text(text, language):
    """Vectorise le texte en utilisant Word2Vec et retourne un vecteur moyen pour le texte entier."""
    words = text.split()
    valid_words = []
    # Vérifier si le modèle pour la langue spécifiée est disponible
    if language in model_w2v:
        model = model_w2v[language]
        # Itérer sur les mots et vérifier s'ils sont présents dans le modèle
        for word in words:
            if word in model.key_to_index:
                valid_words.append(word)
            else:
                # Essayer chaque autre modèle si le mot n'est pas dans le modèle actuel
                for lang, alt_model in model_w2v.items():
                    if lang != language and word in alt_model.key_to_index:
                        valid_words.append(word)
                        break

    if valid_words:
        # Calculer les vecteurs de mots et le vecteur moyen
        word_vectors = np.array([model[word] for word in valid_words if word in model.key_to_index])
        mean_vector = np.mean(word_vectors, axis=0)
        return mean_vector.tolist()
    # Retourner un vecteur nul si aucun mot n'est disponible
    return [0] * model.vector_size

def Creat_Tables(collection_name, data, max_varchar_length, language, vector_size):
    connections.connect("default", host="127.0.0.1", port="19530")
 
    if not utility.has_collection(collection_name):
        # Créez la collection avec un schéma approprié si elle n'existe pas
        fields = [
            FieldSchema(name="ID_Unique", dtype=DataType.INT64, is_primary=True, auto_id=True)
        ] + [
            FieldSchema(name=key, dtype=DataType.FLOAT_VECTOR, dim=vector_size) if "Vecteur" in key else
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
                    columns[key].append(vectorize_text(value, language))
                else:
                    columns[key].append(value)

    try:
        mr = collection.insert([columns[field.name] for field in collection.schema.fields if field.name != "ID_Unique"])
        print("Data inserted:", mr.primary_keys)
    except Exception as e:
        print(f"Error inserting data: {e}")





