from structures import *

"""Ce qu'on peut faire :
    - créer un réseau
    - créer un routeur connecté à un certain nombre de réseaux
    - supprimer un routeur d'un réseau
    - envoyer les messages
    - traiter les messages
"""

reseau1 = Reseau('10.0.0.0',  100)
reseau2 = Reseau('11.0.0.0',  150)
reseau3 = Reseau('12.0.0.0',  200)
reseau4 = Reseau('13.0.0.0',  1000)
reseau5 = Reseau('14.0.0.0',  50)

routeur1 = Routeur([reseau1, reseau2])
routeur2 = Routeur([reseau2, reseau3, reseau4])
routeur3 = Routeur([reseau3, reseau4])
routeur4 = Routeur([reseau4, reseau1])
routeur5 = Routeur([reseau4, reseau5])
routeur6 = Routeur([reseau5, reseau1])

liste_Des_Routeurs = [routeur1, routeur2, routeur3, routeur4, routeur5, routeur6]

for routeur in liste_Des_Routeurs:
    routeur.envoyerMessages()

for routeur in liste_Des_Routeurs:
    routeur.traiterLesMessages()

print(routeur1.protocole_Ospf.matrice)
print(routeur2.protocole_Ospf.matrice)

print(routeur1.protocole_Rip.table)
