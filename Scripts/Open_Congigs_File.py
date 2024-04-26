import subprocess
import sys
import os

def Open_Congigs_File(path):
    width = 80
    line = "═" * (width - 2)
    

    # Détecter le système d'exploitation et ouvrir le fichier
    if sys.platform == "win32":
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.run(["open", path])
    else:  # Assume que c'est un système de type Unix/Linux
        subprocess.run(["xdg-open", path])

    print("╔" + line + "╗")
    update_msg = f"║ Ouverture du fichier config."
    update_msg = f"{update_msg:{' '}<{width-2}} ║"
    print(update_msg)
    print("╚" + line + "╝")  # Pour une ligne vide après le cadre


