def Creat_Dictionair(variable_names, default_values):
    """
    Crée un dictionnaire à partir de listes de noms de variables et de valeurs par défaut.

    :param variable_names: Une liste contenant les noms des variables.
    :param default_values: Une liste contenant les valeurs par défaut correspondantes.
    :return: Un dictionnaire avec les noms des variables comme clés et les valeurs par défaut comme valeurs.
    """
    
    # S'assurer que le nombre de valeurs par défaut correspond au nombre de variables
    if len(default_values) != len(variable_names):
        raise ValueError("Le nombre de valeurs par défaut doit correspondre au nombre de variables")

    # Création du dictionnaire en utilisant un dictionnaire comprehension
    tables = {name.strip(): value.strip() for name, value in zip(variable_names, default_values)}
    
    return tables


# Exemple d'utilisation:
# variable_names = ["ID_Unique", "Nom_Document", "Chemin_Document", "Txt_Brute", "Context_Brute", "Context_Vecteurs"]
# default_values = ["ID", "FileName_value", "Value1", "Value2", "Value3", "Value4"]

# Tables = Creat_Dictionair(variables_str, values_str)
# print("Tables =", Tables)
