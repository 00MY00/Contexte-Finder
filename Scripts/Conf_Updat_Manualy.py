def print_frame(message, width=90):
    line = "═" * width
    print("╔" + line + "╗")

    def wrapped_text(text):
        # Cette fonction enveloppe le texte en fonction de la largeur spécifiée sans couper les mots
        words = text.split()  # Split sur les espaces
        wrapped_lines = []
        current_line = ""
        
        for word in words:
            # Vérifie si l'ajout du mot actuel dépasse la largeur maximale autorisée
            if len(current_line) + len(word) + 1 > width - 4:  # 2 espaces pour les bordures + 2 pour l'espacement intérieur
                wrapped_lines.append(current_line)
                current_line = word
            else:
                if current_line:
                    current_line += " "  # Ajout d'un espace entre les mots
                current_line += word
        
        if current_line:  # Ajout de la dernière ligne si nécessaire
            wrapped_lines.append(current_line)

        return wrapped_lines

    # Gestion des listes ou des messages simples
    if isinstance(message, list):
        for msg in message:
            lines = wrapped_text(msg)
            for line in lines:
                formatted_msg = f"║ {line:{' '}<{width-2}} ║"  # -2 pour les bordures
                print(formatted_msg)
    else:
        lines = wrapped_text(message)
        for line in lines:
            formatted_msg = f"║ {line:{' '}<{width-2}} ║"  # -2 pour les bordures
            print(formatted_msg)
    line = "═" * width
    print("╚" + line + "╝")
    print()  # Pour une ligne vide après le cadre


def Conf_Updat_Manualy(configs, newConfigs):
    try:
        # Clé à vérifier et retirer car ajouter automatiquement
        key = 'DBTabls'
        value_to_remove = 'Distance'

        # Vérification et suppression de la valeur dans newConfigs et configs
        if key in newConfigs and isinstance(newConfigs[key], list):
            if value_to_remove in newConfigs[key]:
                newConfigs[key].remove(value_to_remove)         

        if key in configs and isinstance(configs[key], list):
            if value_to_remove in configs[key]:
                configs[key].remove(value_to_remove)

                        
        print_frame("Début de la mise à jour des configurations...")
        
        tempVar = 0

        # Vérification et mise à jour des variables globales
        for cle, nouvelle_valeur in newConfigs.items():
            # Vérifie si la clé existe dans les configurations actuelles et si la valeur est différente
            if cle in configs and configs[cle] != nouvelle_valeur:
                print_frame(f"La valeur de '{cle}' va changer de {configs[cle]} à {nouvelle_valeur}.")
                tempVar = 1
            # Mise à jour des configurations actuelles avec les nouvelles valeurs
            configs[cle] = nouvelle_valeur

        if tempVar == 0:
            print_frame("Aucune valeur changée !")
        
        # Message de confirmation de la mise à jour
        print_frame("Mise à jour des configurations terminée!")
        print()  # Pour une ligne vide après le cadre

        # Optionnel : Retourner le dictionnaire mis à jour pour un usage ultérieur
        return configs

    except Exception as e:
        print_frame(f"Erreur lors de la mise à jour des configurations : {e}")
        return None  # Retourne None en cas d'erreur

