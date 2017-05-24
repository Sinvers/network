limit=15  #inferieur ou egal // Limite pour RIP

#La mega_Liste repésente l'ensemble des routeur de cette manière : liste de (ancienne table (ie. table non mise à jour, pur éviter les conflits si elle est mise à jour au meme moment), la nouvelle table (peut donc etre la meme que l'ancienne), et la liste des voisins).
#Un routeur est représenté par son indice dans la mega_Liste.

def updateTable (table, couple, emetteur):                  #Met à jour la table envoyée en paramètre avec un nouveau couple couple provenant de emetteur. FONCTION EN PLACE.
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
    j=0
    while j<len(table):
        j_reseau, j_cout, j_emetteur=table[j]
        if j_cout>limit:
            table.pop(j)
        else :
            j+=1
    #print(table)

def printTablesDeRoutage(mega_Liste):                   #Fonction d'affichage d'une mega liste.
    print()
    print("--------------------------------------------------------------------")
    for i in range(len(mega_Liste)):
        print()
        old_table, new_table, vois=mega_Liste[i]
        print("*****Routeur numero ", i, ":")
        if old_table==[] and new_table==[] and vois==[]:
            print("Ce routeur est deconnecte")
        else:
            print("Sa (old)table est : ", old_table)
            print("Ses voisins sont : ",  vois)
    print()
    print("--------------------------------------------------------------------")
    print()

def broadcast(voisins, table_old, self, mega_Liste):                            #Met à jour tous les voisins d'un routeur avec la old_table du routeur en question. FONCTION EN PLACE.
    for vois in voisins:
        #print("Voisin :")
        #print(vois)
        for elt in table_old:
            res, dist, emet=elt
            vois_oldtable, vois_newtable, vois_vois=mega_Liste[vois]
            updateTable(vois_newtable, (res, dist), self)

def newTableVersOldTable(mega_Liste):                   #Copie la new_Table vers la old_table de chaque élément de mega_Liste. FONCTION EN PLACE.
    for i in range(len(mega_Liste)):
        old_table, new_table, vois_liste = mega_Liste[i]
        old_table=[]
        for j in new_table:
            old_table.append(j)
        mega_Liste[i] = old_table, new_table, vois_liste
    #print("Liste mise a jour :")
    #print(mega_Liste)

def miseAJourUnitaire (mega_Liste):                              #Attention cette fonction ne copie pas la new_table vers la old_table ! On a introduit les old_table et new_table pour que lors d'une mise à jour unitaire, il n'y ait pas de notion d'ordre, c'est à dire que tous les routeurs soient traités de la meme façon : on n'appelle les fonctions qu'avec les old_table et dans ces fonctions on met seulement à jour les new_table. FONCTION EN PLACE.
    for num_routeur in range(len(mega_Liste)):
        #print("--routeur :" +str(num_routeur))
        table_old, table_new, liste_vois=mega_Liste[num_routeur]
        broadcast(liste_vois, table_old, num_routeur, mega_Liste)
    #print (mega_Liste)
    
def mettreAJour(mega_Liste, nbr):                   #Met à jour nbr fois la mega_Liste. FONCTION EN PLACE.
    for i in range(nbr):
        miseAJourUnitaire(mega_Liste)                   #On fait une mise à jour sans modifier les old_table.
        newTableVersOldTable(mega_Liste)                    #On va changer toutes les old_table en new_table.
    #printTablesDeRoutage(mega_Liste)
    
def ajoutRouteur(mega_Liste, voisins):                  #Ajoute un routeur à la fin de la mega_Liste (son numéro est donc len(mega_Liste)) et ayant pour voisins les éléments de la liste voisins. FONCTION EN PLACE.
    n=len(mega_Liste)
    mega_Liste.append(([(n, 0, n)], [(n, 0, n)], voisins))
    for i in voisins:
        old_table, new_table, vois = mega_Liste[i]
        vois.append(n)
        mega_Liste[i]=old_table, new_table, vois

def desactiveRouteur(mega_Liste, n):                    #Désactive un routeur (on ne peut le supprimer complètement puisque cela déplacerait le noms de tous les routeurs qui viennent ensuites). FONCTION EN PLACE.
    mega_Liste[n]=([], [], [])
    for i in range(len(mega_Liste)) :
        if i!=n:
            old_table, new_table, vois=mega_Liste[i]
            for j in range(len(vois)):
                if vois[j]==n:
                    vois.pop(j)
                    break
            j=0
            while j<len(old_table):
                j_dest, j_cout, j_emetteur=old_table[j]
                if j_emetteur==n or j_dest==n:
                    old_table.pop(j)
                else :
                    j+=1
            new_table=copieListe(old_table)
            mega_Liste[i]=old_table, new_table, vois
            
def activeRouteur(mega_Liste, n, voisins):                  #Réactive le routeur numéro n avec les voisins voisins.
    if mega_Liste[n]!=([], [], []):
        print ("Vous essayez d'activer un routeur déjà actif. Ajout annulé...")
    else:
        mega_Liste[n]=([n, 0, n], [n, 0, n], voisins)                   #Il connait uniquement le chemin pour aller à lui-meme (il faudra faire des mises à jours).
        for i in voisins:
            old_table, new_table, vois=mega_Liste[i]
            vois.append(n)
            mega_Liste[i]=old_table, new_table, vois
        
def copieListe(liste):                  #Crée et retourne une copie de liste. 
    copie=[]
    for i in range(len(liste)):
        copie.append(liste[i])
    return copie

def copieMegaListe(mega_Liste):                 #Crée et retourne une copie de mega_Liste.
    copie=[]
    for i in range(len(mega_Liste)):
        old_table, new_table, vois = mega_Liste[i]
        copie.append((copieListe(old_table), copieListe(new_table), copieListe(vois)))
    return copie

def nbrDeToursNecessaire(mega_Liste):                   #Retourne le nombre de tours necessaires pour que la mega_Liste soit à jour, c'est à dire qu'elle possède dans sa new_Table/old_table (puisqu'ici elles sont les memes).
    i=0
    mega_Liste_New=copieMegaListe(mega_Liste)                   #On ne peut pas faire de traitement en place puisqu'on ne pourrait plus ensuite comparer la mega_Liste mise à jour et celle qui ne l'a pas été.
    mettreAJour(mega_Liste_New, 1)
    while mega_Liste_New!=mega_Liste:                   #Si elles sont identiques alors le processus est terminé.
        i+=1
        mega_Liste=mega_Liste_New
        mega_Liste_New=copieMegaListe(mega_Liste)
        mettreAJour(mega_Liste_New, 1)
    return i

import random as rd

def generateurDeReseauERREUR(nombre):                 #Génère aléatoirement un réseau constitué de nombre routeurs, génère en fait une mega_Liste.
    mega_Liste = []
    for i in range(nombre):
        n=rd.randint(1, nombre-1)             #1 puisqu'on impose qu'il ait au moins un voisin // C'est le nombre de voisins pour le routeur i
        vois=[]
        choix=[]                                       #Va etre les possibilites de voisins
        for j in range (nombre):
            if j!=i :
                choix.append(j)
        #print(choix)
        for j in range(n):
            #print("len : ",  len(choix))
            nbAlea=rd.randrange(0, len(choix))     #0 puiqu'on veut avoir aussi le 0
            #print(nbAlea)
            vois.append(choix[nbAlea])
            choix.pop(nbAlea)
        mega_Liste.append([[(i,0, i)], [(i,0, i)],  vois])
    return mega_Liste
    
def generateurDeReseau(nombre):                 #Correction de la fonction précédente qui créait un graphe orienté (si A est un voisin de B, B n'était pas forcément un voisin de A). Celle-ci renvoie bien un graphe non orienté.
    mega_Liste = []
    for j in range(nombre):
        choix = []
        for i in range(nombre):
            if j != i:
                choix.append(i)
        nb_Vois=rd.randint(0, nombre - 1)
        vois = rd.sample(choix, nb_Vois)
        mega_Liste.append([[(j,0, j)], [(j,0, j)],  vois])
    for j in range(nombre) :
        old_Table, new_Table, vois = mega_Liste[j]
        for u in vois :
            u_Old_Table, u_New_Table, u_Vois = mega_Liste[u]
            if not (j in u_Vois) :
                u_Vois.append(j)
            mega_Liste[u] = u_Old_Table, u_New_Table, u_Vois
    return mega_Liste

infini = float("inf")

def tableTotale(mega_Liste):                    #Retourne une matrice contenant 1 si les routeurs sont directement connectés, ou -1 si ils ne le sont pas directement. POUR OSPF.
    mat=[]
    n = len(mega_Liste)
    for i in range(n):
        mat.append([])
        for j in range(n):
            mat[i].append(infini)
    for i in range(n):
        mat[i][i]=0
    for i in range(n):
        i_old_table, i_new_table, i_vois = mega_Liste[i]
        for j in i_vois:
            mat[i][j]=1
    return mat


def dijkstra (table_Totale, indice_Routeur):
    
    d=[]                    #C'est la liste qui contiendra les distances de indice_Routeur au routeur représenté par l'indice de la liste.
    for i in range(len(table_Totale[indice_Routeur])):
        d.append(table_Totale[indice_Routeur][i])
    #print("d = ", d)
    
    n = len(table_Totale[indice_Routeur])
    S = [indice_Routeur]                    #Contient les routeurs déjà traités.
    S_Compl = []                    #Contiendra les routeurs non encore traités.
    for i in range(n):
        if i != indice_Routeur :
            S_Compl.append(i)
    #print("S_Compl = ", S_Compl)
    
    while len(S_Compl) != 0 :
        min=S_Compl[0]
        i=0
        for j in range(len(S_Compl)) :                  #Recherche du routeur parmis S_Compl dont la distance à indice_Routeur est la plus faible.
            if d[S_Compl[j]]<d[min] :
                min = S_Compl[j]
                i = j
        #print("min, indice : ",  min,  i)
        S.append(S_Compl[i])                    #On ajoute à S le routeur que l'on vient de traiter.
        S_Compl.pop(i)                  #On l'enlève de S_Compl.
        
        for k in range(len(S_Compl)):                   #Pour chaque routeur non encore traité, on compare sa distance à indice_Routeur qu'on avait précédemment (dans d) avec celle en passant par le routeur à distance minimale de cette étape.
            if d[S_Compl[k]]>d[min]+table_Totale[min][S_Compl[k]]:
                d[S_Compl[k]]=d[min]+table_Totale[min][S_Compl[k]]
        print("S_Compl = ", S_Compl)
        #print(d)
    return d                    #On a alors la distance minimale de indice_Routeur à chaque routeur.
