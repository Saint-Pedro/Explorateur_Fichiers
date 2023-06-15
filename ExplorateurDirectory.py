import os                                       #import detection + interaction os (possibilité créer,retirer,déplacer...)
import collections                              #import pour les dictionnaires
from datetime import datetime                   #import pour déterminer date + heures fichiers
from colorama import Fore, Style, init          #import couleur + style         py -m pip install colorama // #py -m pip install --upgrade pip
import re                                       #import regex utilisé pour retirer les couleurs avant la sauvegarde sur fichier
from pathlib import Path                        #import pour déterminer le type de fichier avec son extension

# Initialisation colorama (biblio couleurs)
init(autoreset=True)

# verifie si on est bien sur windows
is_windows = os.name == 'nt'

# fonction pour clear l'ecran, utilisé par la suite
def clear_screen():
    os.system('cls' if is_windows else 'clear')

#fonction que l'on utilisera pour supprimer la couleur pour la sauvegarde
def strip_color_codes(string_with_codes):
    return re.sub('\x1b.*?m', '', string_with_codes)


def analyze_directory(directory):
    files = []
    file_type_counts = collections.defaultdict(int) # Initialise un dictionnaire pour compter les types de fichiers
    oldest_file = ''                #Initialise des variables pour stocker noms + date création et modif
    newest_file = ''
    oldest_time = float('inf')
    newest_time = float('-inf')     #float renvoi un nombre - infini et -infini garantit respectivement, garantie fichiers + anciens et fichiers + récent à la suite
    oldest_modified_file = ''
    newest_modified_file = ''
    oldest_modified_time = float('inf')
    newest_modified_time = float('-inf')
    file_type_times = collections.defaultdict(lambda: {"oldest": {"time": float('inf'), "name": ''},
                                                      "newest": {"time": float('-inf'), "name": ''},
                                                      "oldest_modified": {"time": float('inf'), "name": ''},
                                                      "newest_modified": {"time": float('-inf'), "name": ''}})
    #En gros c'est un dictionnaire imbriqué composé des 8 variables que nous avons initialisés ci-dessus. file_type_times va ajouter les types de fichiers à ces variables dans une structure de données plus complète
    #évite d'avoir plusieurs variables indépendantes pour chaque type de fichiers.

#root est le (chemin) répertoire actuel
    for root, _, filenames in os.walk(directory): #fonction os.walk() -> parcours récursivement un répertoire et ses sous-répertoires. Il récupère les noms des dossiers (ignorés ici en utilisant l'underscore _) et les noms des fichiers dans chaque répertoire.
        for file in filenames: #Pour chaque nom de fichier dans liste fichiers (filenames), on exécute les instructions suivantes:
            file_path = os.path.join(root, file)    #créer le chemin complet du fichier en joignant directory actuel + nom fichier
            creation_time = os.path.getctime(file_path) #retourne le temps de création du fichier spécifié par file_path
            modified_time = os.path.getmtime(file_path) #idem mais pour le temps de modification du fichier spécifié

            file_type = Path(file_path).suffix[1:] if Path(file_path).suffix else "sans extension" #obtient extension après dernier point et si suffix vide = pas extension / découpage [1:] exclue le premier caractère (en soi point) de l'extension et assigne l'extension à file_type
            file_type_counts[file_type] += 1                #ajoute +1 au type de fichier existant et si n'existe pas encore, renvoie la valeur int de 0 et incrémente tout de même le type de fichier

     #comparaison heures création + modification + stockage (pour l'ensemble des fichiers)
            if creation_time < oldest_time:
                oldest_time = creation_time         #détermine fichier + ancien
                oldest_file = file

            if creation_time > newest_time:
                newest_time = creation_time         #détermine fichier + récent
                newest_file = file

            if modified_time < oldest_modified_time:
                oldest_modified_time = modified_time    #détermine fichier + ancien en terme de modifs
                oldest_modified_file = file

            if modified_time > newest_modified_time:
                newest_modified_time = modified_time    #détermine fichier + récent en terme de modifs
                newest_modified_file = file

     # comparaison création + modification + stockage dans dico file_type (pour chaque type de fichier différent)
            if creation_time < file_type_times[file_type]["oldest"]["time"]:
                file_type_times[file_type]["oldest"]["time"] = creation_time
                file_type_times[file_type]["oldest"]["name"] = file

            if creation_time > file_type_times[file_type]["newest"]["time"]:
                file_type_times[file_type]["newest"]["time"] = creation_time
                file_type_times[file_type]["newest"]["name"] = file
                                                                                        #comme en haut mais pour les types
            if modified_time < file_type_times[file_type]["oldest_modified"]["time"]:
                file_type_times[file_type]["oldest_modified"]["time"] = modified_time
                file_type_times[file_type]["oldest_modified"]["name"] = file

            if modified_time > file_type_times[file_type]["newest_modified"]["time"]:
                file_type_times[file_type]["newest_modified"]["time"] = modified_time
                file_type_times[file_type]["newest_modified"]["name"] = file

# à la place d'un simple print, on conserve toute l'analyse via une chaine de caractère string
    result = ""
    # donc à la place de print(Fore.CYAN...) on va ecrire result += Fore.CYAN...:
    #print() replacé par result += "\n" :
    result += "\n"
    result += Fore.CYAN + Style.BRIGHT + f"Il y a {sum(file_type_counts.values())} fichier(s) au total.\n"

    if len(file_type_counts) > 1:   #si plus d'un fichier dans le rep execute le code du bloc "if"
        for file_type, count in file_type_counts.items():
            result += Fore.GREEN + Style.BRIGHT + f"Il y a {count} fichier(s) de type {file_type}.\n"

        result += "\n"              #espace pour plus de lisibilité
        result += Fore.WHITE + Style.BRIGHT + f"Rappel Format : Y/M/D - H/M/S 24H.\n"
        result += "\n"
                                                                                                                                                     #formate date et heure en format spécifique Année/Mois/Jour  Heure/minutes/secondes qui est ajouté au string result
        result += Fore.RED + Style.BRIGHT + "Le fichier le plus ancien est " + Fore.BLUE + Style.BRIGHT + f"{oldest_file} " + Fore.RED + Style.BRIGHT + f"datant de {datetime.fromtimestamp(oldest_time).strftime('%Y-%m-%d')} à {datetime.fromtimestamp(oldest_time).strftime('%H:%M:%S')}.\n"
        result += Fore.RED + Style.BRIGHT + "Le fichier le plus récemment créé est " + Fore.BLUE + Style.BRIGHT + f"{newest_file} " + Fore.RED + Style.BRIGHT + f"datant de {datetime.fromtimestamp(newest_time).strftime('%Y-%m-%d')} à {datetime.fromtimestamp(newest_time).strftime('%H:%M:%S')}.\n"
        result += Fore.RED + Style.BRIGHT + "Le fichier avec la modification la plus ancienne est " + Fore.BLUE + Style.BRIGHT + f"{oldest_modified_file} " + Fore.RED + Style.BRIGHT + f"datant de {datetime.fromtimestamp(oldest_modified_time).strftime('%Y-%m-%d')} à {datetime.fromtimestamp(oldest_modified_time).strftime('%H:%M:%S')}.\n"
        result += Fore.RED + Style.BRIGHT + "Le fichier le plus récemment modifié est " + Fore.BLUE + Style.BRIGHT + f"{newest_modified_file} " + Fore.RED + Style.BRIGHT + f"datant de {datetime.fromtimestamp(newest_modified_time).strftime('%Y-%m-%d')} à {datetime.fromtimestamp(newest_modified_time).strftime('%H:%M:%S')}.\n"

     # Affiche les résultats pour chaque type de fichier
    for file_type, times in file_type_times.items():
        result += Fore.YELLOW + f"\nPour les fichiers de type " + Fore.GREEN + Style.BRIGHT + f"{file_type}:\n"

        if file_type_counts[file_type] == 1:
            result += Fore.YELLOW + "Il n'y a qu'un seul fichier de ce type :" + Fore.BLUE + Style.BRIGHT + f"{times['oldest']['name']}\n"
            result += Fore.YELLOW + f"  - Créé le {datetime.fromtimestamp(times['oldest']['time']).strftime('%Y-%m-%d')} à {datetime.fromtimestamp(times['oldest']['time']).strftime('%H:%M:%S')}\n"
            result += Fore.YELLOW + f"  - Modifié pour la dernière fois le {datetime.fromtimestamp(times['oldest_modified']['time']).strftime('%Y-%m-%d')} à {datetime.fromtimestamp(times['oldest_modified']['time']).strftime('%H:%M:%S')}.\n"
        else:
            result += Fore.YELLOW + f"  - Le fichier le plus ancien est " + Fore.BLUE + Style.BRIGHT + f"{times['oldest']['name']} " + Fore.YELLOW + f"datant de {datetime.fromtimestamp(times['oldest']['time']).strftime('%Y-%m-%d')} à {datetime.fromtimestamp(times['oldest']['time']).strftime('%H:%M:%S')}.\n"
            result += Fore.YELLOW + f"  - Le fichier le plus récemment créé est " + Fore.BLUE + Style.BRIGHT + f"{times['newest']['name']} " + Fore.YELLOW + f"datant de {datetime.fromtimestamp(times['newest']['time']).strftime('%Y-%m-%d')} à {datetime.fromtimestamp(times['newest']['time']).strftime('%H:%M:%S')}.\n"
            result += Fore.YELLOW + f"  - Le fichier avec la modification la plus ancienne est " + Fore.BLUE + Style.BRIGHT + f"{times['oldest_modified']['name']} " + Fore.YELLOW + f"datant de {datetime.fromtimestamp(times['oldest_modified']['time']).strftime('%Y-%m-%d')} à {datetime.fromtimestamp(times['oldest_modified']['time']).strftime('%H:%M:%S')}.\n"
            result += Fore.YELLOW + f"  - Le fichier le plus récemment modifié est " + Fore.BLUE + Style.BRIGHT + f"{times['newest_modified']['name']} " + Fore.YELLOW + f"datant de {datetime.fromtimestamp(times['newest_modified']['time']).strftime('%Y-%m-%d')} à {datetime.fromtimestamp(times['newest_modified']['time']).strftime('%H:%M:%S')}.\n"

        result += "\n"

    # retourne le string result quand c'est terminé.
    result_plain = strip_color_codes(result)    #ici on crée également une version sans couleur pour la sauvegarde

    print(result)       # affiche l'analyse dans la console/terminal.

    return result_plain #renvoie les résultats sous forme de string pour la sauvegarde sans colorama


exit_program = False # false -> programme continue si on veut l'arrêter -> true comme ci-dessous avec "q"

while not exit_program:
    start_directory = input(Fore.BLUE + Style.BRIGHT + "Veuillez entrer le chemin du répertoire (q: quitter): ") #input début utilisateur

    if start_directory.lower() == 'q':       #lower -> fait en sorte que ce soit insensible casse, si entrée utilisateur en Majuscule ou minuscule
        print(Fore.BLUE + Style.BRIGHT + "Fin du programme.")
        exit_program = True
        break

    clear_screen()
    result_plain = analyze_directory(start_directory)

#Propositions du programme ; fin programme, déplacement ou nouveau répertoire
    while True: #choice variable qui recoit une entree utilisateur
        choice = input(Fore.BLUE + Style.BRIGHT + "Que souhaitez-vous faire ? (q: quitter, s: sauvegarder, n: nouvelle analyse): ") #input de fin de programme
        if choice.lower() == 'q': ##lower -> fait en sorte que ce soit insensible casse, si entrée utilisateur en Majuscule ou minuscule
            print(Fore.BLUE + Style.BRIGHT + "Fin du programme.")
            exit_program = True
            break #combiné pour bien sortir de la boucle
        elif choice.lower() == 's':
            save_directory = input(Fore.BLUE + Style.BRIGHT + "Veuillez entrer le chemin du répertoire de sauvegarde: ") #input de sauvegarde ; donnez rép
            if not os.path.isdir(save_directory): #vérifie si rép valide et existant
                print(Fore.RED + Style.BRIGHT + "Répertoire invalide. L'analyse n'a pas été sauvegardée.")
            else:
                filename = input(Fore.BLUE + Style.BRIGHT + "Veuillez entrer le nom du fichier: ") #variable entrée utilisateur déterminer nom
                file_path = os.path.join(save_directory, filename + ".txt") #crée chemin complet : directory + nom fichier (filename) + extension .txt
                with open(file_path, 'w') as f: #ouvre fichier en mode écriture
                    f.write(result_plain) #cette ligne écrit le résultat de l'analyse sans couleurs stocké par result_plain
                print(Fore.GREEN + Style.BRIGHT + "L'analyse a été sauvegardée avec succès.")
            break
        elif choice.lower() == 'n':
            clear_screen()
            break
        else:
            print(Fore.RED + Style.BRIGHT + "Choix invalide. Veuillez réessayer.")

#Pour retransformer ce script en application .exe, lancez cette commande en terminal : py -m PyInstaller --onefile C:\Users\UFED\Desktop\astin\Python\Explorateur_de_fichiers_Python\ExplorateurFichiers.py 
#ou remplacer par chemin accès actuel de votre fichier python
#installer pyinstaller si ce n'est pad déja le cas, reprendre la commande pour colorama au début du code et remplacer par pyinstaller


#notes colorama, différentes couleurs possibles :
#Fore.BLACK
#Fore.RED
#Fore.GREEN
#Fore.YELLOW
#Fore.BLUE
#Fore.MAGENTA
#Fore.CYAN
#Fore.WHITE

#Vous pouvez également choisir de rajouter ou supprimer l'aspect Gras du texte avec "  Style.BRIGHT  "


#Regex/Re.sub :
#return re.sub('\x1b.*?m', '', string_with_codes)

#\x1b.*?m  -->  intégralité des différents codes couleurs 
#m délimiteur de fin des codes couleurs



    



