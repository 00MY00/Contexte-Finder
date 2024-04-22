def Extract_Configs(filepath):
    variables = {}
    with open(filepath, 'r') as file:
        for line in file:
            # Nettoyage des espaces et vérification si la ligne n'est pas vide
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith('#'):
                # Séparation du nom de la variable et des valeurs
                var_name, values = stripped_line.split(':', 1)
                var_name = var_name.strip()
                values = values.strip()
                # Vérifier si les valeurs contiennent des virgules pour les traiter comme une liste
                if ',' in values:
                    variables[var_name] = [value.strip() for value in values.split(',')]
                else:
                    variables[var_name] = values.strip()

    return variables

# Exemple d'utilisation
#config = Extract_Configs('..\Configs.conf') # Récupère les configs et les valeurs
# Afficher les variable et leurs valeurs 
# for var_name, value in config.items():
#     print(f"{var_name} : {value}")