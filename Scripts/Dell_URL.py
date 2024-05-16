# Retirer les url de la liste de model
def Dell_URL(input_list):
    return [element for element in input_list if 'https://' not in element]