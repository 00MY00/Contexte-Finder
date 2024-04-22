
def Max_255(text, MaxVarcharLeng):
    # Séparer le texte en mots
    words = text.split()

    # Vérifier si la longueur du texte est déjà inférieure ou égale à 255 caractères
    if len(text) <= int(MaxVarcharLeng):
        return text

    # Réduire la longueur du texte en retirant des mots
    while len(' '.join(words)) > int(MaxVarcharLeng):
        # Supprimer le dernier mot de la liste
        words.pop()

    # Reconstruire le texte avec les mots restants
    reduced_text = ' '.join(words)
    return reduced_text

# Exemple d'utilisation de la fonction
# input_text = "Ceci est un exemple de texte qui dépasse la limite de 255 caractères. Nous devons réduire la longueur de ce texte."
# output_text = reduce_text_length(input_text)
# print("Texte réduit :", output_text)



