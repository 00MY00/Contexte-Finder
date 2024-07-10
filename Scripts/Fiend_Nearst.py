import json
import numpy as np
from collections import defaultdict

def get_vector(entry):
    for i in range(1, 5):
        vector_key = f'Vecteur_{i}'
        if vector_key in entry:
            return entry[vector_key]
    return None

def format_multiline(text, length):
    lines = []
    while len(text) > length:
        space_index = text.rfind(' ', 0, length)
        if space_index == -1:
            space_index = length
        lines.append(text[:space_index])
        text = text[space_index:].strip()
    lines.append(text)
    return lines

def Fiend_Nearst(DistanceMin, DistanceMax, NB_Resultat_Afficher, ResultSerch, FullTextBrut, DBTabls):
    data = json.loads(ResultSerch)

    print("FullTextBrut : ", FullTextBrut)  # Débug

    filtered_results = defaultdict(list)
    document_counter = defaultdict(int)

    for word, details in data.items():
        if 'results' in details:
            entries = details['results']
            for field, entry_list in entries.items():
                if isinstance(entry_list, list):
                    for entry in entry_list:
                        if isinstance(entry, dict):
                            entry['word'] = word  # Ajouter le mot à l'entrée
                            distance = entry.get('Distance', None)
                            vector = get_vector(entry)
                            if distance is not None and vector is not None:
                                if np.all(np.array(vector) == 0):
                                    continue
                                if DistanceMin <= distance <= DistanceMax:
                                    filtered_results[entry['Nom_Document']].append(entry)
                                    document_counter[entry['Nom_Document']] += 1

    merged_results = {}
    for doc_name, entries in filtered_results.items():
        # Trier les entrées par distance croissante
        entries.sort(key=lambda x: x['Distance'])
        # Prendre l'entrée avec la distance la plus petite
        merged_entry = entries[0]
        merged_entry['Occurrences'] = document_counter[doc_name]
        # Si FullTextBrut est False, remplacer Txt_Brute par 'False'
        if not str(FullTextBrut) == 'True':
            merged_entry['Txt_Brute'] = 'False'
        merged_results[doc_name] = merged_entry

    # Trier les résultats fusionnés par le nombre d'occurrences décroissantes
    sorted_results = sorted(merged_results.items(), key=lambda x: x[1]['Occurrences'], reverse=True)
    # Limiter les résultats à NB_Resultat_Afficher
    top_results = sorted_results[:NB_Resultat_Afficher]

    max_length = 70

    border = "═" * (max_length + 2)
    print(f"╔{border}╗")
    print(f"║{'Résultats de la Recherche':^{max_length}}  ║")
    print(f"╚{border}╝")

    for doc_name, entry in top_results:
        doc_length = len(doc_name)
        doc_border = "═" * (doc_length + 2)
        print(f"╔{doc_border}╗")
        print(f"║ {doc_name} ║")
        print(f"╚{doc_border}╝")
        entry_border = "─" * (max_length + 2)
        print(f"┌{entry_border}┐")
        for column in DBTabls:
            if 'Vecteur' not in column:
                value = entry.get(column, 'N/A')
                formatted_lines = format_multiline(f"{column}: {value}", max_length)
                for line in formatted_lines:
                    print(f"│ {line:<{max_length}} │")
        print(f"│ {'Mot recherché: ' + entry['word']:<{max_length}} │")
        print(f"│ {'Occurrences: ' + str(entry['Occurrences']):<{max_length}} │")
        print(f"│ {'Distance: ' + str(entry['Distance']):<{max_length}} │")
        print(f"└{entry_border}┘")

        

    print(f"╔{border}╗")
    print(f"║{'Fin des Résultats':^{max_length}}  ║")
    print(f"╚{border}╝")

    #return merged_results
