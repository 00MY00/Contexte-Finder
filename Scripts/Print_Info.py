def Print_Info(UserNameLocal, InstallPacketAtStart):
    width = 80
    line = "═" * (width - 2)
    print("╔" + line + "╗")

    # Message d'accueil personnalisé
    welcome_msg = f"║ Bienvenue {UserNameLocal} ! (tapez 'help' pour l'aide, 'exit' pour quitter) "
    welcome_msg = f"{welcome_msg:{' '}<{width-2}} ║"
    print(welcome_msg)

    # Message de mise à jour automatique
    update_msg = f"║ Auto Update : {InstallPacketAtStart} "
    update_msg = f"{update_msg:{' '}<{width-2}} ║"
    print(update_msg)

    # Ligne vide pour la symétrie
    empty_line = "║" + " " * (width - 2) + "║"
    print(empty_line)

    # Répétition de la ligne supérieure/inférieure pour fermer le cadre
    
    print("╚" + line + "╝")  # Pour une ligne vide après le cadre



