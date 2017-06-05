from structures import *
from constantes import *

"""Ce qu'on peut faire :
    - créer un réseau
    - créer un routeur connecté à un certain nombre de réseaux
    - supprimer un routeur d'un réseau
    - envoyer les messages
    - traiter les messages
"""

"""
reseau1 = Reseau('10.0.0.0',  un_G_Bits_Sec)
reseau2 = Reseau('11.0.0.0',  un_M_Bits_Sec)
reseau3 = Reseau('12.0.0.0',  dix_M_Bits_Sec)
reseau4 = Reseau('13.0.0.0',  cent_K_Bits_Sec)
reseau5 = Reseau('14.0.0.0',  cent_M_Bits_Sec)

routeur1 = Routeur("routeur1", [reseau1, reseau2])
routeur2 = Routeur("routeur2", [reseau2, reseau3, reseau4])
routeur3 = Routeur('routeur3', [reseau3, reseau4, reseau2])
routeur4 = Routeur("routeur4", [reseau4, reseau1])
routeur5 = Routeur("routeur5", [reseau4, reseau5])
routeur6 = Routeur("routeur6", [reseau5, reseau1])

liste_Des_Routeurs = [routeur1, routeur2, routeur3, routeur4, routeur5, routeur6]

for coup in range(10):
    
    for routeur in liste_Des_Routeurs:
        routeur.envoyerLesMessages()
    
    for routeur in liste_Des_Routeurs:
        routeur.traiterLesMessages()

print("Fini")
#routeur1.protocole_Ospf.afficheMatrice()
#routeur1.protocole_Ospf.afficheCheminsOspf()

reseau3.supprimerRouteur(routeur3)

for coup in range(10):
    
    for routeur in liste_Des_Routeurs:
        routeur.envoyerLesMessages()
    
    for routeur in liste_Des_Routeurs:
        routeur.traiterLesMessages()

routeur1.protocole_Ospf.afficheMatrice()
routeur1.protocole_Ospf.afficheCheminsOspf()
"""


#EXEMPLE 2

reseau1 = Reseau('10.0.0.0', cent_M_Bits_Sec)
reseau2 = Reseau('11.0.0.0', un_G_Bits_Sec)
reseau3 = Reseau('12.0.0.0', cent_K_Bits_Sec)
reseau4 = Reseau('13.0.0.0', dix_M_Bits_Sec)
reseau5 = Reseau('14.0.0.0', un_M_Bits_Sec*5)

routeur1 = Routeur('routeur1', [reseau1, reseau2])
routeur2 = Routeur('routeur2', [reseau2, reseau3, reseau4])
routeur3 = Routeur('routeur3', [reseau4, reseau5])
routeur4 = Routeur('routeur4', [reseau5, reseau1])

liste_Des_Routeurs = [routeur1, routeur2, routeur3, routeur4]


for i in range(2):

    for routeur in liste_Des_Routeurs:
        routeur.envoyerLesMessages()
        
    for routeur in liste_Des_Routeurs:
        routeur.traiterLesMessages()

#routeur1.protocole_Rip.afficherTableRip()
print()
routeur1.protocole_Ospf.afficheCheminsOspf()
print()
routeur2.protocole_Ospf.afficheCheminsOspf()
print()
routeur3.protocole_Ospf.afficheCheminsOspf()
print()
routeur4.protocole_Ospf.afficheCheminsOspf()
print()

print("On supprime le routeur")
reseau1.supprimerRouteur(routeur1)

for i in range(10):

    for routeur in liste_Des_Routeurs:
        routeur.envoyerLesMessages()
        
    for routeur in liste_Des_Routeurs:
        routeur.traiterLesMessages()


print("Table RIP :")
routeur1.protocole_Rip.afficherTableRip()
print()
routeur2.protocole_Rip.afficherTableRip()
print()
routeur3.protocole_Rip.afficherTableRip()
print()
routeur4.protocole_Rip.afficherTableRip()
print()

print("Table OSPF :")
routeur1.protocole_Ospf.afficheCheminsOspf()
print()
routeur2.protocole_Ospf.afficheCheminsOspf()
print()
routeur3.protocole_Ospf.afficheCheminsOspf()
print()
routeur4.protocole_Ospf.afficheCheminsOspf()

routeur1.ajouterReseau(reseau1)
print("On remet le routeur1")

for i in range(11):

    for routeur in liste_Des_Routeurs:
        routeur.envoyerLesMessages()
        
    for routeur in liste_Des_Routeurs:
        routeur.traiterLesMessages()


print("Table RIP :")
routeur1.protocole_Rip.afficherTableRip()
print()
routeur2.protocole_Rip.afficherTableRip()
print()
routeur3.protocole_Rip.afficherTableRip()
print()
routeur4.protocole_Rip.afficherTableRip()
print()

print("Table OSPF :")
routeur1.protocole_Ospf.afficheCheminsOspf()
print()
routeur2.protocole_Ospf.afficheCheminsOspf()
print()
routeur3.protocole_Ospf.afficheCheminsOspf()
print()
routeur4.protocole_Ospf.afficheCheminsOspf()

routeur5 = Routeur('routeur5', [reseau1, reseau4])

liste_Des_Routeurs.append(routeur5)

for i in range(5):

    for routeur in liste_Des_Routeurs:
        routeur.envoyerLesMessages()
        
    for routeur in liste_Des_Routeurs:
        routeur.traiterLesMessages()


print("Table RIP :")
routeur1.protocole_Rip.afficherTableRip()
print()
routeur2.protocole_Rip.afficherTableRip()
print()
routeur3.protocole_Rip.afficherTableRip()
print()
routeur4.protocole_Rip.afficherTableRip()
print()
routeur5.protocole_Rip.afficherTableRip()
print()

print("Table OSPF :")
routeur1.protocole_Ospf.afficheCheminsOspf()
print()
routeur2.protocole_Ospf.afficheCheminsOspf()
print()
routeur3.protocole_Ospf.afficheCheminsOspf()
print()
routeur4.protocole_Ospf.afficheCheminsOspf()
print()
routeur5.protocole_Ospf.afficheCheminsOspf()

print("On enlève routeur2")
reseau2.supprimerRouteur(routeur2)
reseau4.supprimerRouteur(routeur2)

for i in range(10):

    for routeur in liste_Des_Routeurs:
        routeur.envoyerLesMessages()
        
    for routeur in liste_Des_Routeurs:
        routeur.traiterLesMessages()

print("Table RIP :")
routeur1.protocole_Rip.afficherTableRip()
print()
routeur2.protocole_Rip.afficherTableRip()
print()
routeur3.protocole_Rip.afficherTableRip()
print()
routeur4.protocole_Rip.afficherTableRip()
print()
routeur5.protocole_Rip.afficherTableRip()
print()

print("Table OSPF :")
routeur1.protocole_Ospf.afficheCheminsOspf()
print()
routeur2.protocole_Ospf.afficheCheminsOspf()
print()
routeur3.protocole_Ospf.afficheCheminsOspf()
print()
routeur4.protocole_Ospf.afficheCheminsOspf()
print()
routeur5.protocole_Ospf.afficheCheminsOspf()
