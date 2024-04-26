import subprocess
import sys
import os

def Open_Congigs_File(path):
    # Détecter le système d'exploitation et ouvrir le fichier
    if sys.platform == "win32":
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.run(["open", path])
    else:  # Assume que c'est un système de type Unix/Linux
        subprocess.run(["xdg-open", path])



