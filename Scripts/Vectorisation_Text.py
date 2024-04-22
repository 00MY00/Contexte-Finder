import sys
import json
from transformers import BertModel, BertTokenizer
import torch

# Initialiser le tokenizer et le modèle
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
model.eval()  # Passer le modèle en mode évaluation

def Vectorisation_Text(text):
    """Extrait les vecteurs caractéristiques de chaque mot d'un texte en utilisant un modèle BERT pré-entraîné."""
    # Initialiser le tokenizer et le modèle
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    model.eval()  # Passer le modèle en mode évaluation

    # Préparer les vecteurs pour chaque mot
    vecteurs_par_mot = []
    
    # Traitement de chaque mot individuellement pour garder leur ordre et vecteur associé
    mots = text.split()
    for mot in mots:
        # Tokeniser chaque mot séparément
        inputs = tokenizer(mot, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            # Récupérer les sorties du modèle pour chaque mot
            outputs = model(**inputs)
        # Exclure les tokens spéciaux [CLS] et [SEP] si nécessaire et prendre le premier token comme représentation du mot
        vecteur = outputs.last_hidden_state[0, 1:-1, :].numpy()  # Exclure [CLS] et [SEP]
        vecteurs_par_mot.append(vecteur.tolist())

    return vecteurs_par_mot

# Teste
#Config = Vectorisation_Text('biographie')  # Vectorise mot par mot  
#print(Config)