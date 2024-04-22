def Partition_Clee(cles, taille_groupe):
    """ Partitionne la liste de clés en groupes de taille donnée """
    return [cles[i:i + taille_groupe] for i in range(0, len(cles), taille_groupe)]


# Permet de partitionner les quantiter de vecteur le mak par table dans milvius est de 4