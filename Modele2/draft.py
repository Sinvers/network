from structures import *

reseau1 = Reseau("10.0.0.0", 100)
reseau2 = Reseau("11.0.0.0",  50)
reseau3 = Reseau("12.0.0.0",  1000)

routeur1 = Routeur('routeur1', [reseau1, reseau2])
routeur2 = Routeur('routeur2', [reseau2, reseau3])
routeur3 = Routeur('routeur3', [reseau1, reseau3])

print(routeur1)
print(reseau1)

liste_Routeur = [routeur1, routeur2, routeur3]

routeur1.envoyerMessages()
routeur2.envoyerMessages()
routeur3.envoyerMessages()

routeur1.traiterLesMessages()
print(routeur1.protocole_Ospf.matrice)

routeur2.traiterLesMessages()
print(routeur2.protocole_Ospf.matrice)

routeur3.traiterLesMessages()
print(routeur3.protocole_Ospf.matrice)

routeur1.envoyerMessages()
routeur2.envoyerMessages()
routeur3.envoyerMessages()

routeur1.traiterLesMessages()
print(routeur1.protocole_Ospf.matrice)

routeur2.traiterLesMessages()
print(routeur2.protocole_Ospf.matrice)

routeur3.traiterLesMessages()
print(routeur3.protocole_Ospf.matrice)

for routeur in liste_Routeur:
    print("matrice du routeur ", routeur.nom, " ", routeur.protocole_Ospf.matrice)
