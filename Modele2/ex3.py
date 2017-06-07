from structures import *
from constantes import *

#EXEMPLE 3 : Mise en difficulté de OSPF lors de micro-coupures.
#On peut modéliser la rapidité de Ospf par rapport à Rip en doublant l'envoie et le traitement des messages pour Ospf, ie. là où Ospf enverra et traitera deux fois les messages, Rip ne le fera qu'une fois.

avec_Amelioration = True                   #Activation de l'amélioration ?
switchAmelioration(avec_Amelioration)

numero_Mode = 0
switchMode(numero_Mode)

reseau1 = Reseau('11.0.0.0', un_G_Bits_Sec)                 #Réseaux très rapides
reseau2 = Reseau('12.0.0.0', un_G_Bits_Sec)                 #
reseau3 = Reseau('13.0.0.0', un_G_Bits_Sec)                 #
reseau4 = Reseau('14.0.0.0', un_G_Bits_Sec)                 #
reseau5 = Reseau('15.0.0.0', un_K_Bits_Sec)                 #Réseau à bas débit
reseau6 = Reseau('16.0.0.0', un_G_Bits_Sec)                 #De nouveau rapide
reseau7 = Reseau('17.0.0.0', un_G_Bits_Sec)                 #
reseau8 = Reseau('18.0.0.0', un_G_Bits_Sec)                 #

routeur1 = Routeur('routeur1', [reseau1, reseau2])
routeur2 = Routeur('routeur2', [reseau2, reseau3, reseau4])
routeur3 = Routeur('routeur3', [reseau4, reseau5])
routeur4 = Routeur('routeur4', [reseau1, reseau5])
routeur5 = Routeur('routeur5', [reseau1, reseau8])
routeur6 = Routeur('routeur6', [reseau3, reseau6])
routeur7 = Routeur('routeur7', [reseau6, reseau7])
routeur8 = Routeur('routeur8', [reseau7, reseau5])
routeur9 = Routeur('routeur9', [reseau4, reseau1])

liste_Des_Routeurs = [routeur1, routeur2, routeur3, routeur4, routeur5, routeur6, routeur7, routeur8, routeur9]

#On modifie le fonctionnement habituel de notre modèle en séparant les actions avec Rip de celles avec Ospf.
"""
def envoyerMessagesRip(liste_Des_Routeurs):
    for routeur in liste_Des_Routeurs:
        routeur.protocole_Rip.envoyerRip(routeur.liste_Interfaces)
def traiterMessagesRip(liste_Des_Routeurs):
    for routeur in liste_Des_Routeurs:
        routeur.protocole_Rip.traiterRip()
"""

#On modifie le fonctionnement habituel de notre modèle en séparant les actions avec Rip de celles avec Ospf.
def envoyerMessagesOspf(liste_Des_Routeurs):
    for routeur in liste_Des_Routeurs:
        routeur.protocole_Ospf.envoyerOspf(routeur.liste_Interfaces)
def traiterMessagesOspf(liste_Des_Routeurs):
    for routeur in liste_Des_Routeurs:
        routeur.protocole_Ospf.traiterOspf()


#Mise à jour du réseau simple :
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

print()
print("----------------------------------------------------------------------------------------------------------")
print("------------------------------------------- Déconnexion rapide -------------------------------------------")
print("----------------------------------------------------------------------------------------------------------")
print()

#On déconnecte (pour un court moment un lien.
reseau3.supprimerRouteur(routeur2)

envoyerMessagesOspf(liste_Des_Routeurs)
traiterMessagesOspf(liste_Des_Routeurs)

estTermine(liste_Des_Routeurs)
afficher(liste_Des_Routeurs)


print()
print("----------------------------------------------------------------------------------------------------------")
print("------------------------------------------- Reconnexion -------------------------------------------")
print("----------------------------------------------------------------------------------------------------------")
print()
#On le remet, puisqu'alors, uniquement Ospf aura détecté la déconnexion.
routeur2.ajouterReseau(reseau3)


#Mise à jour du réseau simple :
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
