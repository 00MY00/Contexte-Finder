def print_frame(message, width=90):
    line = "═" * width
    print("╔" + line + "╗")
    if isinstance(message, list):
        for msg in message:
            formatted_msg = f"║ {msg:{' '}<{width-2}} ║"
            print(formatted_msg)
    else:
        formatted_msg = f"║ {message:{' '}<{width-2}} ║"
        print(formatted_msg)
    print("╚" + line + "╝")
    print()  # Pour une ligne vide après le cadre

def Conf_Updat_Manualy(ConfFilePath):
    from Extract_Configs import Extract_Configs

    try:
        print_frame("Début de la mise à jour des configurations...")
        
        try:
            configs = Extract_Configs(ConfFilePath)  # Récupération config
        except Exception as e:
            print_frame(f"Erreur: Vérifiez l'existence du fichier {ConfFilePath} Info : {e}")
            return  # Arrête la fonction en cas d'erreur de chargement

        # Vérification et mise à jour des variables globales
        for cle, nouvelle_valeur in configs.items():
            if cle in globals() and globals()[cle] != nouvelle_valeur:
                print_frame(f"La valeur de '{cle}' va changer de {globals()[cle]} à {nouvelle_valeur}.")
            globals()[cle] = nouvelle_valeur  # Mise à jour ou création de la variable globale

        # Message de confirmation de la mise à jour
        print_frame("Mise à jour des configurations terminée!")
    except Exception as e:
        print_frame(f"Erreur lors de la mise à jour des configurations : {e}")


