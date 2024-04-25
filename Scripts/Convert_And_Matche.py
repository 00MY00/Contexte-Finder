import gensim.downloader as api
import json
import numpy as np
from pymilvus import Collection, connections
import logging

# Configurer le niveau de log pour ignorer les avertissements
logging.getLogger().setLevel(logging.ERROR)



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



def vectorize_word(word):
    """ Vectorise un mot en utilisant Word2Vec et retourne son vecteur. """
    try:
        word_vector = model_w2v[word]
    except KeyError:
        # Vecteur nul si le mot n'est pas dans le vocabulaire
        word_vector = np.zeros(model_w2v.vector_size)
    return word_vector.tolist()

def convert_numpy(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, list):
        return [convert_numpy(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_numpy(value) for key, value in obj.items()}
    return obj

def search_and_fetch_details(collection_name, query_vector, vector_field_names, NB_vecteur_Proche, Precision):
    connections.connect("default", host="127.0.0.1", port="19530")
    collection = Collection(name=collection_name)
    search_params = {"metric_type": "L2", "params": {"nprobe": int(Precision)}}

    top_k = int(NB_vecteur_Proche)
    results = {}
    for field in vector_field_names:
        search_result = collection.search([query_vector], field, search_params, limit=top_k, output_fields=["*"])
        formatted_result = []
        distances = []
        for hit in search_result[0]:
            # Modification ici pour traiter l'ID en tant qu'entier
            entity_details = collection.query(expr=f"ID_Unique == {hit.id}", output_fields=["*"])
            entity_data = {'Distance': convert_numpy(hit.distance)}
            distances.append(entity_data['Distance'])
            if entity_details:
                detail = entity_details[0]
                entity_data.update({key: convert_numpy(value) for key, value in detail.items()})
            formatted_result.append(entity_data)
        results[field] = formatted_result
        results[f'Distances_{field}'] = distances

    return json.dumps(results, indent=4)

def Convert_And_Matche(text, collection_name, vector_field_names, NB_vecteur_Proche, Precision):
    words = text.split()
    word_vectors = [vectorize_word(word) for word in words]
    search_results = {}
    for word, vector in zip(words, word_vectors):
        result = search_and_fetch_details(collection_name, vector, vector_field_names, NB_vecteur_Proche, Precision)
        search_results[word] = result
    return json.dumps(search_results, indent=4, default=lambda x: float(x) if isinstance(x, (float, np.float32)) else x)
