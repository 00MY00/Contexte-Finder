import torch
from transformers import BertModel, BertTokenizer
from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections, utility
import logging
from transformers import BertModel, BertTokenizer

# Configurer le niveau de log pour ignorer les avertissements
logging.getLogger("transformers").setLevel(logging.ERROR)
# Initialisation du tokenizer et du modèle BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
model.eval()  # Mode évaluation

def print_collection_fields(collection_name):
    # Connexion à Milvus
    connections.connect("default", host="127.0.0.1", port="19530")

    # Vérification de l'existence de la collection
    if utility.has_collection(collection_name):
        # Récupération de la collection
        collection = Collection(name=collection_name)
        
        # Accès au schéma de la collection
        schema = collection.schema
        
        # Extraction et affichage des noms des champs
        field_names = [field.name for field in schema.fields]
        print("Colonnes de la collection '{}':".format(collection_name))
        print(field_names)
    else:
        print(f"La collection '{collection_name}' n'existe pas.")



def vectorize_text(text, MaxVarcharLeng):
    """ Vectorise le texte en utilisant BERT et retourne un vecteur moyen pour le texte entier. """
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    vecteur_moyen = outputs.last_hidden_state[0, 1:-1, :].mean(0).numpy()
    return vecteur_moyen.tolist()  # Conversion en liste unidimensionnelle

def Creat_Tables(collection_name, data, MaxVarcharLeng):
    connections.connect("default", host="127.0.0.1", port="19530")

    # Découverte dynamique des champs à partir des clés de données
    sample_record = data[0]
    fields = []
    for key, value in sample_record.items():
        if "Vecteur" in key:
            # Supposons que tous les champs contenant 'Vecteur' doivent être des vecteurs
            fields.append(FieldSchema(name=key, dtype=DataType.FLOAT_VECTOR, dim=768))
        else:
            # Autres champs considérés comme VARCHAR
            fields.append(FieldSchema(name=key, dtype=DataType.VARCHAR, max_length=int(MaxVarcharLeng)))

    # Définir le champ de clé primaire
    primary_field = "ID_Unique"  # Vous pouvez choisir n'importe quel champ comme clé primaire

    # Créer le schéma de la collection avec le champ de clé primaire spécifié
    schema = CollectionSchema(fields, primary_field=primary_field, description="Collection for testing")

    # Création de la collection
    collection = Collection(name=collection_name, schema=schema)

    columns = {field.name: [] for field in fields}
    for record in data:
        for key, value in record.items():
            if "Vecteur" in key:
                columns[key].append(vectorize_text(value, MaxVarcharLeng))
            else:
                columns[key].append(value)

    data_to_insert = [columns[field.name] for field in fields]
    mr = collection.insert(data_to_insert)
    print("Données insérées dans la nouvelle collection, ID des entrées :", mr.primary_keys)

# data = [
#     {"user_id": "user1", "secret_key": "key1", "Vecteur_Description": "Example of text input for BERT model."},
#     {"user_id": "user2", "secret_key": "key2", "Vecteur_Description": "Another example of text for BERT."}
# ]


# Teste d'execution
#Creat_Tables("test_collection", data)  # Nom de la collection les nom des collones et leur valeur ci la colone contien Vecteur les valeur sont transformer en vecteurs
#print_collection_fields("test_collection")  # Affiche les collones