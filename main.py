
from fonctions import *

"""table=[("a", 0, "A"), ("b", 2, "C"), ("c", 6, "A"), ("d", 8, "B")]"""


"""updateTable(table, ("f", 5), "G")
updateTable(table, ("c", 4), "B")
"""

megaListe1= [ \
([(0, 0, 0)], [(0, 0, 0)], [1]), \
([(1, 0, 1)], [(1, 0, 1)], [0]) \
]

megaListe2= [ \
([(0, 0, 0)], [(0, 0, 0)], [1]), \
([(1, 0, 1)], [(1, 0, 1)], [0, 2, 3]), \
([(2, 0, 2)], [(2, 0, 2)], [1, 3]), \
([(3, 0, 3)], [(3, 0, 3)], [1, 2, 4]), \
([(4, 0, 4)], [(4, 0, 4)], [3]) \
]


"""
miseAJourUnitaire(megaListe1)
print("")
print("")
miseAJourUnitaire(megaListe2)
newTableVersOldTable(megaListe2)

print("")
print("")
miseAJourUnitaire(megaListe2)
newTableVersOldTable(megaListe2)

print("")
print("")
miseAJourUnitaire(megaListe2)
newTableVersOldTable(megaListe2)

printTablesDeRoutage(megaListe2)
"""



"""printTablesDeRoutage(megaListe1)
ajoutRouteur(megaListe1, [0, 1])
printTablesDeRoutage(megaListe1)
desactiveRouteur(megaListe1, 0)
printTablesDeRoutage(megaListe1)
activeRouteur(megaListe1, 0, [1])
printTablesDeRoutage(megaListe1)"""

"""
mettreAJour(megaListe1, 2)
printTablesDeRoutage(megaListe1)
print()
print()
print()
mettreAJour(megaListe2, 1)
printTablesDeRoutage(megaListe2)
print("-------")
mettreAJour(megaListe2, 1)
printTablesDeRoutage(megaListe2)
print("-------")
mettreAJour(megaListe2, 1)
printTablesDeRoutage(megaListe2)
print("-------")
mettreAJour(megaListe2, 1)
printTablesDeRoutage(megaListe2)
print("-------")
"""


mettreAJour(megaListe2, nbrDeToursNecessaire(megaListe2))
printTablesDeRoutage(megaListe2)

ajoutRouteur(megaListe2, [3])
print("Nombre de tours necessaires : ", nbrDeToursNecessaire(megaListe2))

ajoutRouteur(megaListe2, [0, 4])
nb=nbrDeToursNecessaire(megaListe2)
print("Nombre de tours necessaires : ",  nb)

mettreAJour(megaListe2, nb)
printTablesDeRoutage(megaListe2)
print("******************************************************")

desactiveRouteur(megaListe2, 3)
print("Table après desactivation : ")
printTablesDeRoutage(megaListe2)

nb=nbrDeToursNecessaire(megaListe2)
print("Nombre de tours necessaires : ",  nb)
mettreAJour(megaListe2, nb)
printTablesDeRoutage(megaListe2)


liste=generateurDeReseau(10)        #Attention 1000 ça bug
printTablesDeRoutage(liste)
