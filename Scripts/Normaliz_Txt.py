
import re
from unidecode import unidecode
from spellchecker import SpellChecker
from nltk.corpus import wordnet as wn
import nltk
import langid
import os
import spacy
from spacy.cli import download









def load_model(language_code):
    try:
        # Tente de charger le modèle s'il est déjà installé
        nlp = spacy.load(language_code)
        print(f"Modèle '{language_code}' chargé avec succès.")
    except OSError:
        # Si le modèle n'est pas trouvé, tente de le télécharger
        print(f"Modèle pour '{language_code}' non trouvé. Téléchargement en cours...")
        download(language_code)
        nlp = spacy.load(language_code)  # Charge le modèle après le téléchargement
        print(f"Modèle '{language_code}' téléchargé et chargé avec succès.")
    return nlp







#os.system('cls')    # Clear terminal



# Charger les modèles de langues au début pour éviter de les recharger à chaque appel de la fonction
nlp_fr = load_model('fr_core_news_sm')
nlp_de = load_model('de_core_news_sm')
nlp_en = load_model('en_core_web_sm')
nlp_it = load_model('it_core_news_sm')





nltk.download('wordnet')
nltk.download('omw-1.4')


# NormalisePathFile = '..\\Normaliz_Codex.txt'
# MaxLangueTrust = 100            # ci dépasse un écar de 100 entre MaxLangueTrust et DistancTrust alors la lange trouver est juste
# LanguePourcntValid = 60         # permet de changer la valeur de langu d'une phrace ci elle est = ou plus grand que le chiffre entrée
data_dict = {}


def detect_language(text):
    try:
        lang, confidence = langid.classify(text)
        return lang, confidence
    except Exception as e:
        print(f"Erreur lors de la détection de la langue : {e}")
        return "Unknow", 0  # Retourner une chaîne vide et 0% de confiance si une erreur survient





def evaluer_distance(DistNew, DistancTrust, MaxLangueTrust, LanguePourcntValid):
    # Calculer la différence absolue entre DistNew et DistancTrust
    difference = abs(DistNew - DistancTrust)
    
    # Vérifier si la différence dépasse MaxLangueTrust
    if DistNew > MaxLangueTrust:
        pourcent = '000'
        return True, pourcent

    # Calculer le pourcentage de DistNew par rapport à DistancTrust
    # Gestion du cas où DistancTrust est zéro pour éviter la division par zéro
    if DistancTrust == 0:
        return False, "Erreur : DistancTrust est zéro, calcul impossible."

    # Calcul du pourcentage en utilisant la valeur absolue de DistancTrust pour gérer correctement les valeurs négatives
    DistancTrust = DistancTrust / 1.5
    pourcent = (DistNew / abs(DistancTrust)) * 100
    pourcent_formatte = f"{pourcent:.2f}"  # Formater le pourcentage avec deux décimales
    pourcent_formatte = pourcent_formatte.replace('-', '')
    
    # Vérification si le pourcentage est supérieur à un seuil valide
    if float(pourcent_formatte) >= LanguePourcntValid:
        return True, pourcent_formatte
    else:
        return False, pourcent_formatte




def is_number_un(sentence, lang):
    """
    Remplace le mot 'un' par le chiffre '1' lorsque le contexte indique un chiffre numérique.
    
    :param sentence: La phrase à analyser.
    :param lang: La langue de la phrase (actuellement non utilisée mais peut être utile pour l'extension future).
    :return: La phrase modifiée.
    """
    # Sélectionner le modèle de langue approprié
    nlp = nlp_fr
    doc = nlp(sentence)
    changes = []  # Liste pour stocker les changements

    for token in doc:
        if token.lemma_ == 'un':  # Utilisation du lemme pour être plus précis
            # Condition pour remplacer "un" par "1"
            if is_number_context(token):
                changes.append((token.idx, token.idx + len(token.text), '1'))
                #print(f"Remplacement de '{token.text}' par '1' dans le contexte : '{token.sent}'")

    # Appliquer les changements à la phrase
    new_sentence = list(sentence)
    for start, end, replacement in reversed(changes):
        new_sentence[start:end] = replacement

    return ''.join(new_sentence)

def is_number_context(token):
    """
    Détecte le contexte numérique spécifique pour "un".
    
    :param token: Le token à analyser.
    :return: True si le contexte indique un chiffre numérique, sinon False.
    """
    next_token = token.nbor(1) if token.i + 1 < len(token.doc) else None
    prev_token = token.nbor(-1) if token.i > 0 else None

    # Vérification des conditions pour déterminer si "un" doit être un chiffre
    if next_token and next_token.pos_ in ['NOUN', 'NUM']:
        if next_token.dep_ in ['nummod', 'amod', 'attr', 'dobj']:
            return True
    
    if prev_token and prev_token.pos_ in ['DET', 'ADJ', 'VERB', 'ADV']:
        return False
    
    if prev_token and prev_token.pos_ == 'ADP':
        if next_token and next_token.pos_ in ['NOUN', 'NUM']:
            return True
    
    return False









def normalize_text_to_infinitive(text, lang):
    """
    Normalise le texte en remplaçant les verbes conjugués par leur forme infinitive.
    
    :param text: Le texte à normaliser.
    :param lang: Le code de langue (fr, de, it, en).
    :return: Le texte normalisé.
    """
    # Sélectionner le modèle de langue approprié
    if lang == 'fr':
        nlp = nlp_fr
    elif lang == 'de':
        nlp = nlp_de
    elif lang == 'it':
        nlp = nlp_it
    elif lang == 'en':
        nlp = nlp_en
    else:
        raise ValueError(f"Langue non supportée : {lang}")

    # Analyser le texte avec le modèle de langue
    doc = nlp(text)
    new_sentence = []

    for token in doc:
        # Si le token est un verbe, lemmatiser pour obtenir l'infinitif
        if token.pos_ == 'VERB':
            new_sentence.append(token.lemma_)
        else:
            new_sentence.append(token.text)

    return ' '.join(new_sentence)















def replace_de_with_germany(sentence):              # Specifique au francais entre 'de' et l'acronime Allmagne
    nlp = spacy.load('fr_core_news_sm')
    doc = nlp(sentence)
    new_sentence = []

    i = 0
    while i < len(doc):
        word = doc[i].text
        # Vérifier si le mot actuel est 'de' et s'il est suivi par 'Allemagne'
        if word.lower() == 'de' and i + 1 < len(doc) and doc[i + 1].text.lower() == 'allemagne':
            # Remplacer 'de' par 'Allemagne'
            new_sentence.append('Allemagne')
            i += 1  # Sauter le mot 'Allemagne' dans l'itération suivante
        else:
            new_sentence.append(word)
        i += 1

    # Reconstruire la phrase modifiée
    return ' '.join(new_sentence)







def find_and_replace(word, langue_requise, filepath):
    # Dictionnaire pour stocker les résultats
    global data_dict

    if not data_dict:
        # Ouvrir le fichier en mode lecture
        with open(filepath, 'r', encoding='utf-8') as file:  # Assurez-vous d'utiliser l'encodage approprié
            # Lire chaque ligne du fichier
            for line in file:
                
                # Ignorer les lignes qui commencent par '#'
                if line.startswith('#'):
                    continue
                
                # Diviser la ligne en parties basées sur ':', et convertir chaque partie en str
                parts = [str(part) for part in line.strip().split(':')]
                
                # Ignorer les lignes qui ne contiennent pas exactement 2 ou 3 valeurs
                if not (2 <= len(parts) <= 3):
                    continue
                
                # Choix de la clé selon le nombre de valeurs dans la ligne
                if len(parts) == 2:
                    key = parts[0]
                    key = key.replace(' ', '')
                else:
                    key = parts[1]
                    key = key.replace(' ', '')
                
                # Initialiser le sous-dictionnaire pour la clé si nécessaire
                if key not in data_dict:
                    data_dict[key] = {}
                
                # Ajouter ou mettre à jour les informations de la langue et du remplacement
                data_dict[key] = {
                    'langue': parts[0].replace(' ', '') if len(parts) == 3 else None,  # Langue uniquement si 3 parties
                    'replacement': parts[-1] 
                }

    #print(data_dict)
    # Vérification de la présence du mot et de la correspondance de la langue
   # Vérifier si le mot est dans le dictionnaire et si la langue requise est 'fr'
    if word in data_dict:
        info_mot = data_dict[word]

        # Si le mot est 'de' et la langue requise est 'fr', ne pas le remplacer
        if word == 'de' and langue_requise == 'fr':
            #print(f"Mot '{word}' non modifié car il est en français.")
            return word

        # Vérifie si 'langue' est disponible et si la condition de 3 valeurs est remplie
        if 'langue' in info_mot and info_mot['langue']:
            if info_mot['langue'] == langue_requise:
                #print(f"Remplacer: {word}, par: {info_mot['replacement']}")
                return info_mot['replacement']
            else:
                #print(f"Langue non correspondante pour '{word}': '{info_mot['langue']}' au lieu de '{langue_requise}'")
                return word
        elif info_mot.get('langue') is None:
            #print(f"Remplacer {word} par {info_mot.get('replacement', word)}")
            return info_mot.get('replacement', word)
        else:
            #print(f"Langue non correspondante pour '{word}': '{info_mot.get('langue', 'aucune')}' au lieu de '{langue_requise}'")
            return word
    else:
        #print(f"Le mot '{word}' n'est pas trouvé dans le dictionnaire.")
        return word

    









def text_processing(text, filepath):

    global processed_words
    
    processed_words = []

    # Correction orthographique
    spell = SpellChecker()
    text = spell.correction(text) if spell.correction(text) else word 


    # Déterminer la langue principale du texte complet
    main_lang, main_confidence = detect_language(text)

    if main_lang:
        print(f"Langue trouver du txt complait {main_lang} à {main_confidence}%")       # main_confience represente la valeur la plus proche a atiendre sur chaque mot pour etre sure que ceu mot est dans la même langue !

    else:
        print("Erreur valeur de langue trouver vide !")

    
    # Découpage est gardée ponctuation
    pattern = re.compile(r'[^.,:!?;]+[.,:!?;]*')
    matches = pattern.finditer(text)
    phrases = [match.group(0) for match in matches]
    

    
    

    for phrase in phrases:

        

        # Détection de langue pour chaque phrase et comparaison avec la langue principale
        Phrase_Langue, lang_confidence = detect_language(phrase)

        # Verifier chaque frase pour etre sure de la langue dans la quel elle est écrit
        if Phrase_Langue != main_lang:
            ReturnedValu, Pourcent = evaluer_distance(lang_confidence, main_confidence, MaxLangueTrust, LanguePourcntValid)
            if ReturnedValu:
                lang_to_use = Phrase_Langue
            else:
                lang_to_use = main_lang
            #print(f"\nWord : {phrase} \nValus : {ReturnedValu} \nPourcent : {Pourcent}% \nLangue : {Phrase_Langue} \nLangConfidence : {lang_confidence} \nLangue Utilisée : {lang_to_use}\n")
        
        else:
            lang_to_use = Phrase_Langue
            #print(f"\nPhrase : {phrase} \nLangue : {Phrase_Langue} \n")




        phrase = is_number_un(phrase, lang_to_use)
        phrase = replace_de_with_germany(phrase)

        phrase = normalize_text_to_infinitive(phrase, lang_to_use)
        

        words = phrase.split()
        

        for word in words:
            word_lower = word.lower()
            word_accent_removed = unidecode(word_lower)
            word_special_char_removed = re.sub(r'[!/>\\<:;\']', '', word_accent_removed)

            final_word = find_and_replace(word_special_char_removed, lang_to_use, filepath)

            processed_words.append(final_word)

    


    # Utiliser filter pour retirer les éléments vides
    processed_words = list(filter(None, processed_words))

    print(processed_words)

    stopwords = set([
        'dans', 'et', 'la', 'le', 'de', 'un', 'une', 'du', 'des', 'à', 'les', 'en', 'au', 'aux', 'pour', 'sur', 'par',  # French
        'and', 'the', 'to', 'of', 'a', 'in', 'that', 'is', 'it', 'for', 'on', 'with', 'as', 'by', 'at', 'from', 'this', 'an', 'be', 'or', 'which', 'you', 'his', 'her', 'their', 'its',  # English
        'und', 'die', 'das', 'ist', 'im', 'zu', 'den', 'von', 'mit', 'auf', 'für', 'an', 'es', 'nicht', 'der', 'in', 'ein', 'eine', 'dem', 'wie', 'als', 'auch', 'sich', 'des', 'ein', 'noch', 'war',  # German
        'e', 'di', 'che', 'non', 'un', 'una', 'il', 'la', 'del', 'della', 'a', 'i', 'con', 'per', 'su', 'come', 'da', 'ma', 'è', 'al', 'le', 'si', 'gli', 'dei', 'delle', 'dei', 'nel', 'ci', 'mi', 'ti'  # Italian
    ])
    final_text = ' '.join([phrase for phrase in processed_words if phrase not in stopwords])


    print(f"'{final_text}'")
    return final_text











# Exemple d'utilisation
# input_text = "Je suis un texte francais et je parlais de un Franc Suisse en CH, and i now how to speak english allso. J'ai acheté un livre et un ordinateur."
# processed_text = text_processing(input_text, NormalisePathFile)
# print("\n")
# print(processed_text)
# print("\n")













