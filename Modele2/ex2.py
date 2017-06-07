from structures import *
from constantes import *

#EXEMPLE 2 : RIP et OSPF donnent des chemins différents.

avec_Amelioration = True                   #Activation de l'amélioration ?
switchAmelioration(avec_Amelioration)

numero_Mode = 0
switchMode(numero_Mode)

reseau1 = Reseau('11.0.0.0',  un_G_Bits_Sec)                    #Réseaux très rapides
reseau2 = Reseau('12.0.0.0',  un_G_Bits_Sec)                    #
reseau3 = Reseau('13.0.0.0',  un_G_Bits_Sec)                    #
reseau4 = Reseau('14.0.0.0',  un_G_Bits_Sec)                    #
reseau5 = Reseau('15.0.0.0',  un_K_Bits_Sec)                    #

routeur1 = Routeur('routeur1', [reseau1])
routeur2 = Routeur('routeur2', [reseau1, reseau2])
routeur3 = Routeur('routeur3', [reseau2, reseau3])
routeur4 = Routeur('routeur4', [reseau3, reseau4])
routeur5 = Routeur('routeur5', [reseau4, reseau5])

liste_Des_Routeurs = [routeur1, routeur2, routeur3, routeur4, routeur5]

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


#On ajoute une connexion entre le routeur 1 et le réseau 5 :
routeur1.ajouterReseau(reseau5)
print()
print("---------------------------------------- Connexion du routeur 1 au réseau 5 ----------------------------------------")

for i in range(6):
    print()
    print("---------------------------------------- Tour n°", i+1, "----------------------------------------")
    for routeur in liste_Des_Routeurs:
        routeur.envoyerLesMessages()
        
    for routeur in liste_Des_Routeurs:
        routeur.traiterLesMessages()
    
    estTermine(liste_Des_Routeurs)
    afficher(liste_Des_Routeurs)
    print()

#Avec RIP le chemin le plus court (en nombre de saut) sera préféré tandis qu'avec OSPF le chemin le plus rapide le sera.
#Comparaison du temps pour transmettre un paquet avec Rip et avec Ospf.

