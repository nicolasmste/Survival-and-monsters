# Survival-and-monsters
il faut que la map varie en fonction de la taille de l'écran

import xml.etree.ElementTree as ET

def modifier_largeur_map(fichier_xml, nouvelle_largeur):
    # Parse le fichier XML
    tree = ET.parse(fichier_xml)
    root = tree.getroot()

    # Modifie la valeur de l'attribut 'width' de l'élément 'map'
    root.set('width', str(nouvelle_largeur))

    # Écrit les modifications dans le fichier XML
    tree.write(fichier_xml, encoding='utf-8', xml_declaration=True)

# Utilisation de la fonction pour rendre la largeur variable
modifier_largeur_map('votre_fichier.xml', 50)  # Par exemple, on change la largeur à 50

Pour jouer à ce super jeux, il faut:
_Un interpréteur Python
_Les librairies :pygame
                pytmx (avec la commande : pip install PyTMX)
                pyscroll (avec la commande : pip install pyscroll)
_Lancer le fichier main.py depuis le répertoire "Survival And Monsters" 
(pour ça rien de plus simple, il suffit d'ouvrir le terminal depuis le répertoire "Survival And Monsters" et entrer : python3 main/main.py)
et voilà ous êtes partit pour des heures de fun !!





