from structures import *
from constantes import *

#EXEMPLE 1 : RIP qui donne un coup infini lors d'une déconnexion d'un routeur.

avec_Amelioration = False                   #Activation de l'amélioration ?
switchAmelioration(avec_Amelioration)

numero_Mode = 0
switchMode(numero_Mode)

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

