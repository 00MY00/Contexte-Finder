#################
# Script Prompt #
#################
# Executer le script dans Powershell !
# C script permet de crée la base de donner vectoriel en récupérent du context dans les fichier se trouvent dans DOCs


### Tester la connexion a Milvus
from pymilvus import connections, MilvusException
import sys
def connect_to_milvus():
    try:
        connections.connect("default", host="127.0.0.1", port="19530")
        #print("Connexion réussie à Milvus!")
    except MilvusException as e:
        print(f"Erreur de connexion à Milvus")
        print("Fermeture du programme...")
        sys.exit(1)  # Quitte le programme avec un code d'erreur










# Import Moduls
import sys
import os
import subprocess
import re
import socket
import json


os.system('cls')    # Clear terminal
print('Chargement des Fonctions .  .  .')

# Ajouter le chemin du répertoire racine
sys.path.append(r'.\Scripts')
####################################################################################
# Import Specifique Fonctions
from extract_values_from_json import extract_values_from_json
from Find_Collection import Find_Collection
#from Creat_Dictionair import Creat_Dictionair
#from Creat_Tables import Creat_Tables
from Extract_Configs import Extract_Configs
#from Extract_Context import Extract_Context
from Identifi_Langue import Identifi_Langue
#from Vectorisation_Text import Vectorisation_Text
#from Partition_Clee import Partition_Clee
#from Unique_Id import Unique_Id
from Find_Partial_Match import Find_Partial_Match
from Convert_And_Matche import Convert_And_Matche
from Convert_And_Matche import StartCreat_Tables
from Install_packet import Install_packet
from Print_Milvus_Collections import Print_Milvus_Collections
from Print_Files_VDB import Print_Files_VDB
from Print_Help import Print_Help
from Print_Info import Print_Info
from Aggregate_Data_to_JSON_Format import Aggregate_Data_to_JSON_Format
from Fiend_Nearst import Fiend_Nearst
from Conf_Updat_Manualy import Conf_Updat_Manualy
from Open_Congigs_File import Open_Congigs_File
from Normaliz_Txt import text_processing
from Dell_URL import Dell_URL
from Normaliz_Txt import load_model


####################################################################################

# Variable
RootFilesPath = '.\DOCs\\'
NormalisePathFile = '.\\Normaliz_Codex.txt'
ConfFilePath = 'Configs.conf'
CollectionName = 'test_collection'
vecteur_defaut = 'null'     # Pour remplire les table vecteur ci il manque
UserNameLocal = os.getenv('USERNAME')
script_path = sys.argv[0]       # Récupérer le chemin du script Python actuellement exécuté
# Charger les modèles de langues au début pour éviter de les recharger à chaque appel de la fonction
nlp_fr = load_model('fr_core_news_sm')
nlp_de = load_model('de_core_news_sm')
nlp_en = load_model('en_core_web_sm')
nlp_it = load_model('it_core_news_sm')

####################################################################################### Script ########################################################################################


### Récupération config
configs = Extract_Configs(ConfFilePath)




### Définir chaque clé comme une variable globale
for cle, valeur in configs.items():
    globals()[cle] = valeur

### Variable automatique
CollectionName = CollecName


###############################
VegaModel = Dell_URL(VectorModelFile)

StartCreat_Tables(VegaModel)        # Importer la langue utiliser par le text entrer qui cera utiliser peu gagnier du temps

###############################


### Installe paquet
if InstallPacketAtStart.lower() == 'true':
    Install_packet(Packedg)






### Prompt
os.system('cls')    # Clear terminal
Print_Info(UserNameLocal, InstallPacketAtStart)
### Prompt Loop
while True:
    connect_to_milvus()
    commande = input(" Entrez une commande  : -> ")
    
    if commande.lower() == 'exit':
        print("Fermeture du programme...")
        break
    elif commande.lower() == '':
        print("Commande incorecte !")
    elif commande.lower() == 'help':
        Print_Help()
    elif commande.lower() == 'reload':  # Penser à fermer le processus précédent
        print("Rechargement du programme...")
        command = [sys.executable, script_path]
        subprocess.run(command)
        os._exit(0)  # Termine immédiatement le processus courant
    elif commande.lower() == 'show coll':
        Print_Milvus_Collections(CollectionName)
    elif commande.lower() == 'show fvdb':
        Print_Files_VDB(CollectionName, int(MaxReturnResultShowFilsVDB))
    elif commande.lower() == 'show inf':
        Print_Info(UserNameLocal, InstallPacketAtStart)
    elif commande.lower() == 'cls':
        os.system('cls')    # Clear terminal
    elif commande.lower() == 'clear':
        os.system('cls')    # Clear terminal
    elif commande.lower() == 'conf':
        Open_Congigs_File(ConfFilePath)
    elif commande.lower() == 'conf rld':
        ### Récupération config
        newConfigs = Extract_Configs(ConfFilePath)
        ### Définir chaque clé comme une variable globale
        for cle, valeur in newConfigs.items():
            globals()[cle] = valeur
        Conf_Updat_Manualy(configs, newConfigs)
    elif commande.lower() == 'start vdb':
        print("Rechargement du programme...")
        command = [sys.executable, "main.py"]
        subprocess.run(command)
        os._exit(0)  # Termine immédiatement le processus courant
    else:
        if Find_Collection(CollectionName):
            try:
                #Autre paquet a installer qui nesesite les variable automatique
                
                commande = commande.replace("'", " ")
                commande = commande.replace(",", "")
                phrase = str(commande)
                
                langue = Identifi_Langue(commande)
                
                VegaModel = Dell_URL(VectorModelFile)
                
                Model_langue = Find_Partial_Match(langue, VegaModel)
                
                # Variable word inconu !
                command =  text_processing(phrase, NormalisePathFile)
                # FieldName : est une liste avec les nom des diferante tables
                # NB_vecteur_Proche : le nobre de vécteur a récupérer
                # Precision : définit la pésision pour la recherche de vecteurs
                ResultSerch = Convert_And_Matche(str(commande), CollectionName, FieldName, NB_vecteur_Proche, int(Precision))   # Récupére les distance les plus procheavec tolérée, et organiser les donnée par table est mis en format JSON
                #print("Débuuuugggg 8 Value ResultSerch : ", ResultSerch)
                # with open('Datas.json', 'w') as file:     # Débug
                #     json.dump(ResultSerch, file, indent=4)     
            except Exception as e:
                print(f"Erreur lors de la conversion et du matching : {e}")
            try:
                # DistanceMin : la distance minimale entre les vecteurs des mot trouver et de ceux chercher
                # DistanceMax : la distance maximal séparent les vecteur des mot trouver et de ceux chercher
                # NB_Resultat_Afficher : le nombre de résulta a afficher parmis les plus pertinent
                # ResultSerch : les donnée JSON dans les quel se trouve les données a tréter
                # FullTextBrut : est un booléin permetent de savoir ci oui il faut afficher tous les mot véctoriser dans Milvus relier au fichier ou non 
                ResultDistanceCheque = Fiend_Nearst(int(DistanceMin), int(DistanceMax), int(NB_Resultat_Afficher), ResultSerch, FullTextBrut, DBTabls)     # Récupère le nombre de vecteur / fichier les plus proche est affiche les résultat!
                #print("filtered_results : ",ResultDistanceCheque)
            except Exception as e:
                print(f"Erreur lors de la recherche des distances proches : {e}")


