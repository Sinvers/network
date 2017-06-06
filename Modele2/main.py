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

"""
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
"""


#EXEMPLE 3 : RIP qui donne un coup infini lors d'une déconnexion d'un routeur.

reseau1 = Reseau('11.0.0.0',  cent_M_Bits_Sec)
reseau2 = Reseau('12.0.0.0',  cent_M_Bits_Sec)
reseau3 = Reseau('13.0.0.0',  cent_M_Bits_Sec)
reseau4 = Reseau('14.0.0.0',  cent_M_Bits_Sec)
reseau5 = Reseau('15.0.0.0',  cent_M_Bits_Sec)
reseau6 = Reseau('16.0.0.0',  cent_M_Bits_Sec)

routeur1 = Routeur('routeur1', [reseau1, reseau2])
routeur2 = Routeur('routeur2', [reseau2, reseau3])
routeur3 = Routeur('routeur3', [reseau3, reseau4])
routeur4 = Routeur('routeur4', [reseau4, reseau5])
routeur5 = Routeur('routeur5', [reseau5, reseau6])

liste_Des_Routeurs = [routeur1, routeur2, routeur3, routeur4, routeur5]


#Besoin de 4 tours pour que tous les routeurs connaissent l'ensemble du réseau.
#RIP et OSPF ont besoin du meme nombre de tour pour connaitre l'ensemble du réseau lorsque le réseau est en ligne.
#Lors de la suppression du routeur 3, pour OSPF on a dès le premier tour la connaissance de la rupture du lien (au routeur 2), tandis que RIP non. Au tour 2, tous les routeurs sont au courant avec OSPF alors qu'avec RIP, les routeurs pensent toujours pouvoir atteindre les autres routeurs.
#Avec l'amélioration de RIP, il faudra attendre le 13 ième tour avant que les routeurs se rendent compte qu'il ne peuvent plus accéder à tous les autres.


for i in range(4):
    print()
    print()
    print("---------------------------------------- Tour n°", i+1, "----------------------------------------")
    for routeur in liste_Des_Routeurs:
        routeur.envoyerLesMessages()
        
    for routeur in liste_Des_Routeurs:
        routeur.traiterLesMessages()
    
    estTermine(liste_Des_Routeurs)
    afficher(liste_Des_Routeurs)



#On retire le routeur 3 de tous ses réseaux.
reseau3.supprimerRouteur(routeur3)
reseau4.supprimerRouteur(routeur3)
print()
print("---------------------------------------- SUPPRESSION TOTALE DU ROUTEUR 3 ----------------------------------------")
print()



for i in range(13):
    print()
    print()
    print("---------------------------------------- Tour n°", i+1, "----------------------------------------")
    for routeur in liste_Des_Routeurs:
        routeur.envoyerLesMessages()
        
    for routeur in liste_Des_Routeurs:
        routeur.traiterLesMessages()
    
    estTermine(liste_Des_Routeurs)
    afficher(liste_Des_Routeurs)



#On rajoute le routeur 3 sur tous ses réseaux initiaux.
routeur3.ajouterReseau(reseau3)
routeur3.ajouterReseau(reseau4)
print()
print("---------------------------------------- AJOUT DU ROUTEUR 3 ----------------------------------------")
print()



for i in range(3):
    print()
    print()
    print("---------------------------------------- Tour n°", i+1, "----------------------------------------")
    for routeur in liste_Des_Routeurs:
        routeur.envoyerLesMessages()
        
    for routeur in liste_Des_Routeurs:
        routeur.traiterLesMessages()
    
    estTermine(liste_Des_Routeurs)
    afficher(liste_Des_Routeurs)
