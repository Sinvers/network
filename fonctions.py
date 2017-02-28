def updateTable (table, couple, emetteur):
    dest, cout=couple
    #print("Couple a traiter :")
    #print(couple)
    trouve=0
    for i in range(len(table)) :
        i_reseau, i_cout,  i_emetteur=table[i]
        if i_reseau == dest :
            if cout+1<i_cout:
                table[i]=i_reseau, cout+1, emetteur
            elif emetteur==i_emetteur:
                table[i]=i_reseau, cout+1, emetteur
            trouve=1
            break
    if trouve == 0 :
        table.append((dest, cout+1, emetteur))
    #print(table)

def printTablesDeRoutage(megaListe):
    for i in range(len(megaListe)):
        print()
        old_table, new_table, vois=megaListe[i]
        print("*****Routeur numero ", i, ":")
        if old_table==[] and new_table==[] and vois==[]:
            print("Ce routeur est deconnecte")
        else:
            print("Sa (old)table est : ", old_table)
            print("Ses voisins sont : ",  vois)
        

def broadcast(voisins, table_old, self, megaListe):
    for vois in voisins:
        #print("Vois :")
        #print(vois)
        for elt in table_old:
            res, dist, emet=elt
            vois_oldtable, vois_newtable, vois_vois=megaListe[vois]
            updateTable(vois_newtable, (res, dist), self)

def newTableVersOldTable(megaListe):
    for i in range(len(megaListe)):
        old_table, new_table, vois_liste = megaListe[i]
        old_table=[]
        for j in new_table:
            old_table.append(j)
        megaListe[i] = old_table, new_table, vois_liste
    #print("Liste mise a jour :")
    #print(megaListe)

def miseAJourUnitaire (megaListe):                              #Attention cette fonction ne copie pas la new_table vers la old_table !
    for num_routeur in range(len(megaListe)):
        #print("--routeur :" +str(num_routeur))
        table_old, table_new, liste_vois=megaListe[num_routeur]
        broadcast(liste_vois, table_old, num_routeur, megaListe)
    #print (megaListe)
    
def mettreAJour(megaListe, nbr):
    for i in range(nbr):
        miseAJourUnitaire(megaListe)
        newTableVersOldTable(megaListe)
    #printTablesDeRoutage(megaListe)
    
def ajoutRouteur(megaListe, voisins):
    n=len(megaListe)
    megaListe.append(([n, 0, n], [n, 0, n], voisins))
    for i in voisins:
        old_table, new_table, vois = megaListe[i]
        vois.append(n)
        megaListe[i]=old_table, new_table, vois

def supprimeRouteur(megaListe, n):
    megaListe[n]=([], [], [])
    for i in range(len(megaListe)) :
        if i!=n:
            old_table, new_table, vois=megaListe[i]
            for j in range(len(vois)):
                if vois[j]==n:
                    vois.pop(j)
                    break
            megaListe[i]=old_table, new_table, vois
            
def activeRouteur(megaListe, n, voisins):
    megaListe[n]=([n, 0, n], [n, 0, n], voisins)
    for i in voisins:
        old_table, new_table, vois=megaListe[i]
        vois.append(n)
        megaListe[i]=old_table, new_table, vois
        
def copieListe(liste):
    copie=[]
    for i in range(len(liste)):
        copie.append(liste[i])
    return copie

def copieMegaListe(megaListe):
    copie=[]
    for i in range(len(megaListe)):
        old_table, new_table, vois = megaListe[i]
        copie.append((copieListe(old_table), copieListe(new_table), copieListe(vois)))
    return copie

def nbrDeToursNecessaire(megaListe):
    i=0
    megaListeNew=copieMegaListe(megaListe)
    mettreAJour(megaListeNew, 1)
    while megaListeNew!=megaListe:
        i+=1
        megaListe=megaListeNew
        megaListeNew=copieMegaListe(megaListe)
        mettreAJour(megaListeNew, 1)
    return i
