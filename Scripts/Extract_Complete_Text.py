import re
import os

def Extract_Complete_Text(filepath, resume_word_size, first_context_trigger, max_context_words):
    predefined_words = first_context_trigger
    regex_predefined_words = '|'.join(map(re.escape, predefined_words))

    # Lire le contenu complet du fichier
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read()

    # Nettoyage et préparation du texte
    text = re.sub(r'-', ' ', text)
    text = re.sub(r'[^\w\s]', '', text).lower()

    # Séparation en mots et sélection basée sur la longueur
    words = [word for word in text.split() if len(word) > int(resume_word_size)]
    selected_words = set()

    used_indices = set()
    index = 0
    while index < len(words):
        word = words[index]
        if re.search(regex_predefined_words, word) and index not in used_indices:
            for i in range(1, 4):
                new_index = index + i
                if new_index < len(words) and new_index not in used_indices:
                    selected_words.add(words[new_index])
                    used_indices.add(new_index)
        index += 1
        if len(selected_words) >= int(max_context_words) or index >= len(words):
            break

    # Ajout de mots aléatoires si nécessaire pour atteindre le minimum requis
    while len(selected_words) < int(max_context_words) and len(words) > len(selected_words):
        selected_words.add(random.choice(words))

    # Extraire le nom de fichier nettoyé
    cleaned_filename = os.path.basename(filepath)
    cleaned_filename = re.sub(r'[-_]', ' ', cleaned_filename)
    cleaned_filename = re.sub(r'[.]', ' ', cleaned_filename)
    cleaned_filename = re.sub(r'[^\w\s]', '', cleaned_filename).lower()

    # Ajouter le nom du fichier et le texte complet aux mots sélectionnés
    final_result = cleaned_filename + ' ' + ' '.join(selected_words) + ' ' + text

    return final_result
