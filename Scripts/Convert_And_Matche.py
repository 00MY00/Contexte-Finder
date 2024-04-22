import torch
import json
import numpy as np
from transformers import BertModel, BertTokenizer
from pymilvus import Collection, connections
import logging

# Configurer le niveau de log pour ignorer les avertissements
logging.getLogger("transformers").setLevel(logging.ERROR)

# Initialisation du tokenizer et du modèle BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
model.eval()

def vectorize_word(word):
    """ Vectorise un mot et retourne son vecteur. """
    inputs = tokenizer(word, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    word_vector = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
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
        distances = []  # Liste pour collecter les distances de chaque hit
        for hit in search_result[0]:
            entity_details = collection.query(expr=f"ID_Unique == '{hit.id}'", output_fields=["*"])
            entity_data = {'Distance': convert_numpy(hit.distance)}
            distances.append(entity_data['Distance'])  # Ajout de la distance à la liste des distances
            if entity_details:
                detail = entity_details[0]
                entity_data.update({key: convert_numpy(value) for key, value in detail.items()})
            formatted_result.append(entity_data)
        results[field] = formatted_result
        results[f'Distances_{field}'] = distances  # Ajouter les distances collectées sous une clé spécifique

    return json.dumps(results, indent=4)


def Convert_And_Matche(text, collection_name, vector_field_names, NB_vecteur_Proche, Precision):
    """ Découpe, vectorise et recherche les vecteurs proches pour chaque mot dans un texte sur plusieurs champs spécifiés et retourne les résultats en JSON. """
    words = text.split()
    word_vectors = [vectorize_word(word) for word in words]
    search_results = {}
    for word, vector in zip(words, word_vectors):
        result = search_and_fetch_details(collection_name, vector, vector_field_names, NB_vecteur_Proche, Precision)
        search_results[word] = result
    return json.dumps(search_results, indent=4, default=lambda x: float(x) if isinstance(x, (float, np.float32)) else x)
