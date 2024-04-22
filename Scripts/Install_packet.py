import subprocess

def Install_packet(packages):
    for package in packages:
        # Vérifie si le package est déjà installé et capture les détails
        check_installed = subprocess.run(f"pip show {package}", text=True, shell=True, capture_output=True)
        
        if 'Name:' in check_installed.stdout:
            # Vérifie si le package est à jour
            outdated = subprocess.run(f"pip list --outdated {package}", text=True, shell=True, capture_output=True)
            if package in outdated.stdout:
                print(f"{package} n'est pas à jour. Mise à jour en cours...")
            else:
                #print(f"{package} est déjà installé et à jour.")
                continue  # Passe au package suivant s'il est à jour
        
        # Construction de la commande pour installer ou mettre à jour le package
        command = f"pip install {package} --upgrade"
        
        try:
            # Exécution de la commande
            result = subprocess.run(command, check=True, text=True, shell=True, capture_output=True)
            # Si l'installation réussit, affiche le résultat positif
            print(f"L'installation ou la mise à jour de {package} a réussi : {result.stdout}")
        except subprocess.CalledProcessError as e:
            # Si l'installation échoue, affiche l'erreur
            print(f"Échec de l'installation de {package} : {e.stderr}")

