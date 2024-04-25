import json
import textwrap  # Importation nécessaire pour la gestion du wrapping de texte

def Fiend_Nearst(DistanceMin, DistanceMax, NB_Resultat_Afficher, datas, FullTextBrut):
    
    FullTextBrut = FullTextBrut.strip()

    print(f"'{FullTextBrut}'")
    if FullTextBrut.lower() == "false":

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
        lines = "═" * width  # ajuster pour aligner avec les bordures verticales
        print("╔" + lines + "╗")  # Ligne supérieure du cadre

        # Parcourir et afficher les résultats
        for index, doc in enumerate(documents_tries[:NB_Resultat_Afficher]):
            # Affichage des informations de chaque document
            info_lines = [
                f"Rang {index + 1}:",
                f"Nom du Document: {doc['Nom_Document']}",
                f"Distance: {doc['Distance']}",
                "Texte Brut:"
            ]
            
            # Gestion de l'affichage du Texte Brut selon le paramètre FullTextBrut
            txt_brut_lines = doc['Txt_Brute'].split('\n')
            # Afficher une partie du texte brut
            first_line = textwrap.shorten(doc['Txt_Brute'], width=width - 4, placeholder='... (truncated)')
            info_lines.append(first_line)

            # Imprimer chaque ligne formatée dans le cadre
            for line in info_lines:
                formatted_line = f"║ {line:{' '}<{width-2}} ║"
                print(formatted_line)
            
            # Ligne vide pour séparer les entrées
            empty_line = "║" + " " * (width - 2) + "  ║"
            print(empty_line)

        # Ligne inférieure du cadre
        print("╚" + lines + "╝")

    elif FullTextBrut.lower() == "true":
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
        lines = "═" * width  # ajuster pour aligner avec les bordures verticales
        print("╔" + lines + "╗")  # Ligne supérieure du cadre

        # Parcourir et afficher les résultats
        for index, doc in enumerate(documents_tries[:NB_Resultat_Afficher]):
            # Affichage des informations de chaque document
            info_lines = [
                f"Rang {index + 1}:",
                f"Nom du Document: {doc['Nom_Document']}",
                f"Distance: {doc['Distance']}",
                "Texte Brut:"
            ]
            # Affichage du Texte Brut dans le cadre
            txt_brut_lines = doc['Txt_Brute'].split('\n')
            for line in txt_brut_lines:
                wrapped_text = textwrap.wrap(line, width=width - 4)
                info_lines.extend(wrapped_text or [""])

            # Imprimer chaque ligne formatée dans le cadre
            for line in info_lines:
                formatted_line = f"║ {line:{' '}<{width-2}} ║"
                print(formatted_line)
            
            # Ligne vide pour séparer les entrées
            empty_line = "║" + " " * (width - 2) + "  ║"
            print(empty_line)

        # Ligne inférieure du cadre
        print("╚" + lines + "╝")
    else:
        print("Erreur de paramètre 'FullTextBrut' (True ou False)")
