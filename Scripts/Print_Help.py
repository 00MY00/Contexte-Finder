def Print_Help():
    width = 90
    line = "═" * (width - 2)
    print("╔" + line + "╗")

    # Message d'accueil
    welcome_msg = "║ Bienvenue dans l'interface de commande !"
    welcome_msg = f"{welcome_msg:{' '}<{width-2}} ║"
    print(welcome_msg)

    # Liste des commandes disponibles
    commands = [
        "help       - Affiche ce message d'aide.",
        " ",
        "exit       - Quitte le programme.",
        "reload     - Recharge le programme.",
        "cls        - Netoy l'affichage.",
        "clear      - Netoy l'affichage.",
        "conf rld   - Recharge les config du fichier config.",
        "show coll  - Affiche les collections de Milvus.",
        "show fvdb  - Affiche les fichiers dans Milvus.",
        "show inf   - Affiche les information et le message de bienvenu du démarage.",
        "start vdb  - Execute les scripts de création de DB vectoriel. (Fermera le programme)"
    ]

    for command in commands:
        command_msg = f"║ {command}"
        command_msg = f"{command_msg:{' '}<{width-2}} ║"
        print(command_msg)

    # Ligne vide pour la symétrie
    empty_line = "║" + " " * (width - 2) + "║"
    print(empty_line)

    # Répétition de la ligne supérieure/inférieure pour fermer le cadre
    print("╚" + line + "╝")
    print()  # Pour une ligne vide après le cadre

