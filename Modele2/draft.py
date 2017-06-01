from structures import *
from constantes import *

reseau1 = Reseau("10.0.0.0", cent_M_Bits_Sec)
reseau2 = Reseau("11.0.0.0",  dix_K_Bits_Sec)
reseau3 = Reseau("12.0.0.0",  dix_M_Bits_Sec)

routeur1 = Routeur('routeur1', [reseau1, reseau2])
routeur2 = Routeur('routeur2', [reseau2, reseau3])
routeur3 = Routeur('routeur3', [reseau1, reseau3])

liste_Routeur = [routeur1, routeur2, routeur3]

routeur1.envoyerLesMessages()
routeur2.envoyerLesMessages()
routeur3.envoyerLesMessages()

routeur1.traiterLesMessages()
routeur2.traiterLesMessages()
routeur3.traiterLesMessages()

routeur1.envoyerLesMessages()
routeur2.envoyerLesMessages()
routeur3.envoyerLesMessages()

routeur1.traiterLesMessages()
routeur2.traiterLesMessages()
routeur3.traiterLesMessages()

print()

#routeur1.protocole_Ospf.afficheMatrice()
#routeur1.protocole_Ospf.afficheCheminsOspf()
#routeur2.protocole_Ospf.afficheCheminsOspf()
#routeur3.protocole_Ospf.afficheCheminsOspf()


