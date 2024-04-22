import json


def Fiend_Nearst(DistanceMin, DistanceMax, NB_Resultat_Afficher, datas):
    # Convertir la chaîne JSON en dictionnaire si nécessaire
    if isinstance(datas, str):
        datas = json.loads(datas)
    
    # Filtrer les documents dans la plage de distances spécifiée
    documents_filtrés = [
        doc for doc in datas.values() if DistanceMin <= doc['Distance'] <= DistanceMax
    ]
    
    # Trier les documents filtrés par la proximité de leur distance à DistanceMin
    documents_tries = sorted(documents_filtrés, key=lambda doc: abs(doc['Distance'] - DistanceMin))
    
    # Préparation du cadre
    width = 100
    lines = "═" * (width)  # ajuster pour aligner avec les bordures verticales
    print("╔" + lines + "╗")  # Ligne supérieure du cadre

    # Parcourir et afficher les résultats
    for index, doc in enumerate(documents_tries[:NB_Resultat_Afficher]):
        # Affichage des informations de chaque document
        document_info = (
            f"Rang {index + 1}:\n"
            f"Nom du Document: {doc['Nom_Document']}\n"
            f"Distance: {doc['Distance']}\n"
            f"Texte Brut: {doc['Txt_Brute'][:50]}... (truncated)"
        )
        document_info_lines = document_info.split("\n")
        for line in document_info_lines:
            formatted_line = f"║ {line:{' '}<{width-2}} ║"
            print(formatted_line)
        
        # Ligne vide pour séparer les entrées
        empty_line = "║" + " " * (width - 2) + "  ║"
        print(empty_line)

    # Ligne inférieure du cadre
    print("╚" + lines + "╝")
