import subprocess

def Install_packet(packages):
    # Récupère la liste des packages installés et obsolètes
    installed_packages = subprocess.run("pip list", text=True, shell=True, capture_output=True).stdout
    outdated_packages = subprocess.run("pip list --outdated", text=True, shell=True, capture_output=True).stdout

    for package in packages:
        # Vérifie si le package est déjà installé
        if package in installed_packages:
            # Vérifie si le package est à jour
            if package in outdated_packages:
                print(f"{package} n'est pas à jour. Mise à jour en cours...")
                command = f"pip install {package} --upgrade"
            else:
                print(f"{package} est déjà installé et à jour.")
                continue
        else:
            # Commande pour installer le package
            command = f"pip install {package}"
        
        try:
            # Exécution de la commande
            result = subprocess.run(command, check=True, text=True, shell=True, capture_output=True)
            print(f"L'installation ou la mise à jour de {package} a réussi : {result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Échec de l'installation de {package} : {e.stderr}")

