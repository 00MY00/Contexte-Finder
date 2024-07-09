import json
import numpy as np
from pymilvus import Collection, connections
import logging
from gensim.models import KeyedVectors

def StartCreat_Tables(VectorModelFile):
    # Configuration des niveaux de journalisation pour ignorer les avertissements
    logging.getLogger("transformers").setLevel(logging.ERROR)
    logging.getLogger("gensim").setLevel(logging.ERROR)

    # Vérifie si le modèle est déjà chargé et le charge si nécessaire
    global model_w2v  # Déclare model_w2v comme variable globale
    if 'model_w2v' not in globals():  # Si model_w2v n'est pas défini, le charger
        model_w2v = {}
        for model_name in VectorModelFile:
            try:
                print(f"Chargement du modèle '{model_name}'...")
                # Chemin vers le fichier de modèle (remplacez par le chemin correct si nécessaire)
                model_path = f'./{model_name}'
                model = KeyedVectors.load_word2vec_format(model_path, binary=False)
                model_w2v[model_name] = model
                print(f"Modèle '{model_name}' chargé avec succès.")
            except FileNotFoundError:
                print(f"Erreur : Fichier de modèle '{model_name}' non trouvé.")
            except ValueError as e:
                print(f"Erreur lors du chargement du modèle '{model_name}': {e}")
    else:
        print("Modèles déjà chargés.")

def vectorize_word(word, language):
    """ Vectorise un mot en utilisant Word2Vec et retourne son vecteur. """
    model = model_w2v.get(language, None)
    if model and word in model.key_to_index:
        word_vector = model[word]
        print(f"Vecteurs Validé : '{word}' dans {language}")
    else:
        # Si le mot n'est pas trouvé dans le modèle de la langue spécifiée, essayer les autres modèles
        word_vector = None
        for lang, alt_model in model_w2v.items():
            if lang != language and word in alt_model.key_to_index:
                word_vector = alt_model[word]
                print(f"Vecteurs Validé dans {lang} : '{word}'")
                break
        if word_vector is None:
            print(f"Vecteurs Non Trouvé : '{word}'")
    return word_vector.tolist() if word_vector is not None else None

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
        for hit in search_result[0]:
            # Modification ici pour traiter l'ID en tant qu'entier
            entity_details = collection.query(expr=f"ID_Unique == {hit.id}", output_fields=["*"])
            if entity_details:
                detail = entity_details[0]
                entity_data = {key: convert_numpy(value) for key, value in detail.items()}
                entity_data['Distance'] = convert_numpy(hit.distance)
                formatted_result.append(entity_data)
        results[field] = formatted_result
    return results

def Convert_And_Matche(text, collection_name, vector_field_names, NB_vecteur_Proche, Precision, language='en'):
    words = text.split()
    word_vectors = {}
    search_results = {}

    for word in words:
        if word not in word_vectors:
            vector = vectorize_word(word, language)
            if vector is not None:
                word_vectors[word] = vector

    for word, vector in word_vectors.items():
        result = search_and_fetch_details(collection_name, vector, vector_field_names, NB_vecteur_Proche, Precision)
        encapsulated_result = {
            "word": word,
            "vector": vector,
            "results": result
        }
        search_results[word] = encapsulated_result
    
    with open('Datas.json', 'w') as file:
        json.dump(search_results, file, indent=4)
    
    return json.dumps(search_results, indent=4)