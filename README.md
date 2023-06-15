# Explorateur_Fichiers
Un explorateur qui va analyser un répertoires et ses sous répertoires en python selon des critères bien spécifiques pour y trouver certains fichiers.
L'explorateur est un outil qui va explorer un dossier ciblé, avec ses sous-dossiers afin de lister des fichiers selon les critères suivants:
- Nombre de fichiers au total dans le répertoire + sous-répertoires
- Fichiers avec la date de création et de modification la plus ancienne et la plus récente(tous fichiers confondus)
- Nombre de fichiers par types de fichiers (sur 9 fichiers au total, il y aura 4 pdf et 5 png..)
- Fichiers avec la date de création et de modification la plus ancienne et la plus récente (par type de fichier identifié précédemment)

Quelques fonctionnalités :
- Rendu en couleur dans la console grâce à colorama
- Possibilité de sauvegarder les résultats dans un fichier texte
- Utilisation de re et strip_color_codes afin de retirer la couleur du string pour une sauvegarde propre sans hex
- Possibilité de relancer une nouvelle analyse après la fin d'une première analyse

Imports de bibliothèques :
- os (détection et interaction avec le système d’exploitation)
- collections (création de dictionnaires afin de stocker nos fichiers selon nos critères mentionnés ci-dessus)
- pathlib (chemin de systèmes de fichiers)
- datetime (déterminer date et heure de création/modification de nos fichiers)
- colorama (rendu en couleur + style en console pour des résultats plus lisibles)
- re (retire les couleurs de notre string result avant de faire une sauvegarde)

À noter également que le programme détermine l'extension du fichier en prenant le terme qui vient après le dernier point dans le nom du fichier (Ex: chat.png sera un type png car c’est le dernier terme après le point). Donc, les fichiers ne contenant pas de points dans leur nom de fichier seront catégorisés par le type "sans extension". L'une des faiblesses de ce programme est qu'il saura déterminer le type d'extension qu'avec le nom du fichier et rien d'autre. 
Voyez des imports comme python-magic, magic-bin, identify ou chardet pour des programmes analysant la structure des fichiers, leurs signatures etc
