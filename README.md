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
