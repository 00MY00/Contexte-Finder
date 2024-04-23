###############
# Script Main #
###############

# Executer le script dans Powershell !
# C script permet de crée la base de donner vectoriel en récupérent du context dans les fichier se trouvent dans DOCs


# Import Moduls
import sys
import os


os.system('cls')    # Clear terminal
print('Chargement des Fonctions .  .  .')

# Ajouter le chemin du répertoire contenant le fichier Del_Collection.py à sys.path
sys.path.append(r'.\Scripts')
####################################################################################
# Import Specifique Fonctions
from Creat_Index import Creat_Index
from Creat_Dictionair import Creat_Dictionair
from Creat_Tables import Creat_Tables
from Del_Collection import Del_Collection
from Extract_Configs import Extract_Configs
from Extract_Context import Extract_Context
from Identifi_Langue import Identifi_Langue
from Vectorisation_Text import Vectorisation_Text
from Partition_Clee import Partition_Clee
from Unique_Id import Unique_Id
from Max_255 import Max_255
from Install_packet import Install_packet
####################################################################################


os.system('cls')    # Clear terminal
print('Prossesing . . .')


# Variable
RootFilesPath = '.\DOCs\\'
ConfFilePath = 'Configs.conf'
CollectionName = 'test_collection'
vecteur_defaut = 'null'     # Pour remplire les table vecteur ci il manque
index_params = {"index_type": "IVF_FLAT","metric_type": "L2","params": {"nlist": 100}}


####################################################################################### Script ########################################################################################


### Récupération config
configs = Extract_Configs(ConfFilePath)




### Définir chaque clé comme une variable globale
for cle, valeur in configs.items():
    globals()[cle] = valeur


### Crée les variables automatique
Tables = Creat_Dictionair(DBTabls, DefaultVal)      # Dictionaire Tables
CollectionName = CollecName


### Installe paquet
if InstallPacketAtStart.lower() == 'true':
    Install_packet(Packedg)


### Suppression de la collection
Del_Collection(CollectionName)







### Listage des fichiers
fichiers = os.listdir(RootFilesPath)
for filepath in fichiers:
    print(filepath)
    langue = Identifi_Langue(RootFilesPath + filepath)
    context = Extract_Context(RootFilesPath + filepath, int(ResumWordSiz), FeirstContextTriger, int(MaxContextWords))
    context = context + ' ' + langue
    #print(context)
    
    # Séparer le texte en mots
    mots = context.split()
    
    dictionnaire_mots = {}

    # Remplir le dictionnaire
    for index, mot in enumerate(mots):
        cle = f"Vecteur_{index+1}"  # Commence l'indexation à 1 pour les clés
        dictionnaire_mots[cle] = mot

    # Ajouter dictionnaire_mots à Tables
    Tables.update(dictionnaire_mots)
    # Afficher le dictionnaire
    #print("Tables:", Tables)

    # Liste des clés contenant le mot 'Vecteur_'
    cles_vecteur = [cle for cle in Tables.keys() if 'Vecteur_' in cle]

    # Partitionner les clés en groupes de 4
    groupes_cles = Partition_Clee(cles_vecteur, 4)

    #print('Group de 4 ', groupes_cles)

    # Parcourir chaque groupe pour créer et remplir la collection
    for groupe in groupes_cles:
        dictionnaire_temporaire = {}

        dictionnaire_temporaire['ID_Unique'] = Unique_Id()  # Générer un ID unique pour chaque groupe
        dictionnaire_temporaire['Nom_Document'] = filepath  # Ajouter le nom du fichier
        dictionnaire_temporaire['Txt_Brute'] = Max_255(context, int(MaxVarcharLeng))  # Ajouter le nom du fichier

        


        # Remplir les vecteurs du groupe ou utiliser une valeur 'null' si le groupe est trop petit
        for i in range(4):
            cle_vecteur = f"Vecteur_{i+1}"
            if i < len(groupe) and groupe[i] in Tables:
                dictionnaire_temporaire[cle_vecteur] = Tables[groupe[i]]
            else:
                dictionnaire_temporaire[cle_vecteur] = vecteur_defaut  # Utiliser la valeur 'null'

        

        print("Output final:", dictionnaire_temporaire)
        Creat_Tables(CollectionName, [dictionnaire_temporaire], MaxVarcharLeng)



os.system('cls')    #Clear terminal
print("Indexation . . .")
print("FieldName : ", FieldName)
Creat_Index(CollectionName, FieldName, index_params)
    
#os.system('cls')    # Clear terminal
print("Chargement des données dans la DB vectoriel terminer !")






