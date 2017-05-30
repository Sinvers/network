
infini = float('inf')
LIMIT = 15                  #Limite du nombre de saut pour RIP.
AMELIORATION = True                 #Active (True) ou désactive (False) les améliorations.

def copieListe(liste):                  #Crée et retourne une copie de liste. 
    copie=[]
    for i in range(len(liste)):
        copie.append(liste[i])
    return copie




class Reseau :
    
    
    """
        - adresse : String
        - routeurs_In : liste de routeurs présents dans ce réseau (initialement aucun routeur n'est présent, on les rajoute au fur et à mesure que l'on ajoute des routeurs : list <Routeur>
        - adresse_Dispo : liste de booléen dont l'indice représente la fin de l'adresse ip et la valeur du booléen donne si cette adresse est disponible ou non (True si elle est prise, False si elle est disponible) : list bool
        - bande_Passante : bande passante du réseau : int
    """
    
    def __init__(self, adresse, debit):
        self.adresse = adresse
        self.routeur_In = []                    
        self.adresse_Dispo = [True]                 #L'adresse 0 est celle du routeur (donc indisponible).
        self.bande_Passante = debit
    
    """def __str__(self):
        print("Réseau ", self.adresse, " ayant les routeurs ",  self.routeur_In, " et de bande passante ",  self.debit)"""
    
    
    def getAdresseGenerique(self):
        Index = self.adresse.rfind('.')
        return self.adresse[:Index]+'.'
    
    def enregistrerRouteur(self, routeur):
        n = len(self.adresse_Dispo)
        indice_Dispo = -1
        booleen = False
        indice = 0
        while not booleen and indice<n:
            if self.adresse_Dispo[indice] == False :
                self.adresse_Dispo[indice] = True
                indice_Dispo = indice
                booleen = True
            indice += 1

        if n<255 and not booleen:
            self.adresse_Dispo.append(True)
            indice_Dispo = n
        
        if indice_Dispo == -1 :
            raise BufferError("Le reseau est sature, on ne peut ajouter de routeur dans ce reseau")
        else :
            self.routeur_In.append(routeur)
            return self.getAdresseGenerique()+str(indice_Dispo)
    
    def supprimerRouteur(self, routeur):
        try:
            index = self.routeur_In.index(routeur)
            self.routeur_In.pop(index)
            
            indice_Routeur = routeur.getIndice(self)
            self.adresse_Dispo[indice_Routeur] = False
            
            routeur.supprimeReseau(self)
            
        except ValueError:
            print("Le routeur n'est pas dans le réseau ou le réseau n'est pas dans le routeur ou l'adresse du routeur sur le réseau n'était pas réservée...")
        except IndexError:
            print("L'indice du routeur n'est pas dans la liste des adresses réservées")
    
    def broadcastOspf(self, message_Ospf):                    #message_Ospf est du type <MessageOspf>
        for routeur in self.routeur_In:
            routeur.ajoutMessageOspf(message_Ospf)
    
    def broadcastRip(self, message_Rip):
        for routeur in self.routeur_In:
            routeur.ajoutMessageRip(message_Rip)


class Routeur :
    
    """
        - liste_Interfaces : liste des interfaces du routeur : list <Interface>
        - protocole_Ospf : objet correspondant au fonctionnement de OSPF sur ce routeur : <OSPF>
        - protocole_Rip : objet correspondant au fonctionnement de RIP sur ce routeur : <RIP>
    """
    
    def __init__(self, liste_Reseau):                   #liste_Reseau est une liste de <Reseau>.
        self.protocole_Ospf = OSPF(self)
        self.protocole_Rip = RIP(self)
        
        self.liste_Interfaces = []
        n=len(liste_Reseau)
        for indice in range(n):
            try:
                adresse_Sur_Reseau = liste_Reseau[indice].enregistrerRouteur(self)
                interface = InterfaceReseau(adresse_Sur_Reseau, liste_Reseau[indice])
                self.liste_Interfaces.append(interface)
            except BufferError:
                print("Le routeur n'a pas pu etre ajouté au reseau ",  liste_Reseau[indice], " car il est saturé")

    """def __str__(self):
        return "Routeur ayant " #+ self.liste_Interfaces"""
    
    
    def getIndice(self, reseau):
        adresse_Sur_Reseau = self.getAdresse(reseau)
        index = adresse_Sur_Reseau.rfind('.')
        indice_Routeur = adresse_Sur_Reseau[(index+1):]
        return indice_Routeur
    
    def getAdresse(self, reseau):
        for interface in self.liste_Interfaces:
            if interface.reseau == reseau:
                return interface.adresse
        raise ValueError("Le routeur n'est pas dans le reseau recherché")



    def ajoutMessageOspf(self, message_Ospf):
        self.protocole_Ospf.recevoirMessage(message_Ospf)
    
    def ajoutMessageRip(self, message_Rip):
        self.protocole_Rip.recevoirMessage(message_Rip)



    def envoyerMessages(self):
        self.protocole_Ospf.envoyer(self.liste_Interfaces)
        self.protocole_Rip.envoyer(self.liste_Interfaces)
    
    def traiterLesMessages(self):
        self.protocole_Ospf.traiter()
        self.protocole_Rip.traiter()


    def supprimerReseau(self, reseau):
        for indice_Interface in range(len(self.liste_Interfaces)):
            if self.liste_Interfaces[indice_Interface].reseau == reseau:
                self.liste_Interfaces.pop(indice_Interface)
                break




class InterfaceReseau :
    
    """
        - adresse : adresse du routeur dans le réseau reseau : String
        - reseau : réseau dans lequel cette interface a les pieds : <Reseau>
    """
    
    def __init__(self, adresse_Du_Routeur, reseau):
        self.adresse = adresse_Du_Routeur
        self.reseau = reseau
    
    """def __str__(self):
        return "Routeur étant dans " + adresse"""
    
class OSPF :
    
    """
        - matrice : c'est l'ensemble du reseau où chaque routeur est représenté par un indice, le lien se fait grace à la liste routeur_To_Index; l'élément dans la case (i, j) est la distance directe du routeur i au routeur j et inf si ils ne sont pas directement reliés : list list int
        - routeur_To_Index : fait le lien entre un routeur et son indice dans matrice qui est aussi son indice dans routeur_To_Index : list <Routeur>
        - liste_Chemin : la liste que l'on cherche à obtenir, celle qui donne le chemin a emprunter : liste <CheminOspf>
        - messages_A_Traiter : liste des messages qui devront etre traité lors de l'étape de traitement : list <MessageOspf>
        - messages_A_Envoyer : liste des messages qui devront etre envoyer lors de l'étape d'envoie : list <UpdateOspf>
        - voisins : liste des routeurs qui sont les proches voisins du routeur concerné et qui contient un booléen qui donne si oui ou non le routeur a envoyé un message hello lors de la phase d'envoie : list (<Routeur>, bool)
    """
    
    def __init__(self, routeur):
        self.matrice = [[0]]
        self.routeur_To_Index = [routeur]
        self.liste_Chemin = []
        self.messages_A_Traiter = []
        self.messages_A_Envoyer = []
        self.voisins = []
        self.routeur = routeur
    
    """def __str__(self):
        return "Protocole OSPF associé à " + print(self.routeur) + "dont la matrice associée au protocole OSPF : " +  self.matrice + " avec pour correspondance : " +  print(self.routeur_To_Index)"""
    
    def recevoirMessage(self, message):
        self.messages_A_Traiter.append(message)
    
    def envoyer(self, liste_Interfaces):
        """On envoie les messages à envoyer puis on envoie les hellos à tous les voisins."""
        
        hello = HelloOspf(self)                 #On crée le message hello qui sera destiné à tous les voisins.
        
        for interface in liste_Interfaces:
            
            for message in self.messages_A_Envoyer:
                interface.reseau.broadcastOspf(message)
            
            interface.reseau.broadcastOspf(hello)
    
    
    def trouverRouteurDansChemin(self, routeur):
        for chemin in self.liste_Chemin:
            if chemin.chemin[-1] == routeur:
                chemin_Recherche = chemin
                break
        return chemin_Recherche
    
    def traiter(self):
        """On traite chacun des messages grace à leur méthode traiter(), puis on regarde dans voisins si tous les voisins sont encore là, sinon on agit en conséquence. Puis on applique Dijkstra pour avoir liste_Chemin."""
        
        for message in self.messages_A_Traiter:
            message.traiter(self.voisins, self.matrice, self.routeur_To_Index)
        
        indice = 0
        while indice < len(self.voisins):
            routeur, bool = self.voisins[indice]
            if bool==False:                 #Si le routeur n'a pas envoyé de message hello.
                self.voisins.pop(indice)                    #On l'enlève des voisins.
                
                indice_In_Mat = self.routeur_To_Index.index(routeur)
                for elt in self.matrice:
                    elt.pop(indice_In_Mat)                  #On l'enlève de matrice.
                self.matrice.pop(indice_In_Mat)                 #On enlève sa colonne entièrement.
                
                self.routeur_To_Index.pop(indice_In_Mat)                    #On l'enlève de la liste des correspondances.
            
            indice += 1
        
        self.liste_Chemin = self.dijkstra()
    
    def dijkstra (self):
        liste_Chemin=[]                    #C'est la liste qui contiendra les objets <CheminOspf>. //distances de indice_Routeur au routeur représenté par l'indice de la liste ainsi que le chemin à emprunter (sera sous forme de liste de couples (int list, int)).
        indice_Routeur_Self = self.routeur_To_Index.index(self.routeur)
        
        for indice in range(len(self.matrice)):                 #On initialise les chemins depuis self jusqu'aux routeurs concernés.
            obj_Chemin = CheminOspf(self.routeur_To_Index[indice], self.matrice[indice][indice_Routeur_Self], [self.routeur_To_Index[indice]])
            liste_Chemin.append(obj_Chemin)
            #if indice == indice_Routeur_Self:
            #    obj_Chemin_Self = obj_Chemin
        
        n = len(self.matrice)
        S = [self.routeur]                    #Contient les routeurs déjà traités.
        S_Compl = []                    #Contiendra les routeurs non encore traités.
        for i in range(n):
            if i != indice_Routeur_Self :
                routeur_I = self.routeur_To_Index[i]
                S_Compl.append(routeur_I)
        #print("S_Compl = ", S_Compl)
        
        while len(S_Compl) != 0:            
            min = S_Compl[0]                   #Indice du routeur.
            indice_Min_S_Compl = 0                    #Indice du routeur dans S_Compl.
            for j in range(len(S_Compl)) :                  #Recherche du routeur parmis S_Compl dont la distance à indice_Routeur_Self est la plus faible.
                #chemin_Min, distance_Min = d[min]
                chemin_Min = self.trouverRouteurDansChemin(min)
                chemin_Temp = self.trouverRouteurDansChemin(S_Compl[j])

                distance_Min = chemin_Min.cout
                distance_Temp = chemin_Temp.cout

                
                #_, distance_Temp = d[S_Compl[j]]
                if distance_Temp<distance_Min :
                    min = S_Compl[j]
                    indice_Min_S_Compl = j
            
            S.append(min)                    #On ajoute à S le routeur que l'on vient de traiter.
            S_Compl.pop(indice_Min_S_Compl)                  #On l'enlève de S_Compl.
            
            chemin_Min = self.trouverRouteurDansChemin(min)
            distance_Min = chemin_Min.cout
            chemin = chemin_Min.chemin                      #C'est la liste des routeurs.
            
            for k in range(len(S_Compl)):                   #Pour chaque routeur non encore traité, on compare sa distance à indice_Routeur qu'on avait précédemment (dans d) avec celle en passant par le routeur à distance minimale de cette étape.
                
                chemin_Temp = self.trouverRouteurDansChemin(S_Compl[k])
                ancienne_Dist = chemin_Temp.cout
                nouvelle_Dist = distance_Min+self.matrice[self.routeur_To_Index.index(min)][self.routeur_To_Index.index(S_Compl[k])]
                if ancienne_Dist>nouvelle_Dist:
                    chemin_Nouv = copieListe(chemin)
                    chemin_Nouv.append(S_Compl[k])
                    
                    chemin_Temp.chemin = chemin_Nouv
                    chemin_Temp.cout = nouvelle_Dist
            #print("S_Compl = ", S_Compl)
            
        return liste_Chemin                    #On a alors la distance minimale de self.routeur à chaque routeur ainsi que le chemin à parcourir le tout dans des objets CheminOspf.


class CheminOspf :
    
    """
        - destination : adresse du reseau destination : String ////// Pour l'instant c'est <Routeur>
        - cout : le coout pour atteindre cette destination : int
        - chemin : c'est le chemin a emprunter pour atteindre destination en cout : list <Routeur>
    """
    
    def __init__(self, destination, cout, chemin):
        self.destination = destination
        self.cout = cout
        self.chemin = chemin
    
    
class MessageOspf :
    
    """
        Ne contient qu'une méthode.
    """
    
    def traiter(self, voisins, matrice, routeur_To_Index):
        pass



class HelloOspf(MessageOspf):
    
    """
        - expediteur : représente l'expediteur du message hello : <Routeur>
        #- reseau : c'est le reseau par lequel transite ce message hello : <Reseau>
    """
    
    def __init__(self, expediteur):
        self.expediteur = expediteur
    
    
    def traiter(self, voisins, matrice, routeur_To_Index):
        indice_Recherche = -1
        for indice in range(len(voisins)):
            routeur, bool = voisins[indice]
            if routeur == self.expediteur:
                indice_Recherche = indice
                break
        if indice_Recherche == -1 :
            voisins.append((self.expediteur, True))
        else :
            voisins[indice_Recherche] = (self.expediteur, True)
        
        #Creer message update que l'on traite tout de suite.
        
        
    """def traiter(self, voisins, matrice, routeur_To_Index):
        expediteur = self.expediteur
        if expediteur in routeur_To_Index :
            try:
                indice = voisins.index((expediteur, False))
                rout, booleen = voisins[indice]
                voisins[indice] = (rout, True)
            except ValueError:
                print("La liste routeur_To_Index n'est pas à jour (il y a le routeur dans routeur_To_Index mais pas dans voisins) ou le booleen n'a pas été remis à False")
            
            try:
                debit = self.reseau.bande_Passante
                indice_Expediteur = routeur_To_Index.index(expediteur)
                indice_Self = routeur_To_Index.index(self)
                if debit < matrice[indice_Expediteur][indice_Self]:
                    matrice[indice_Expediteur][indice_Self] = debit
                    matrice[indice_Self][indice_Expediteur] = debit
            except ValueError:
                print("La liste routeur_To_Index ne contient pas l'expéditeur ou self")
        
        else:
            n=len(routeur_To_Index)
            routeur_To_Index.append(routeur)
            debit = self.reseau.bande_Passante
            matrice
    """
    
class UpdateOspf(MessageOspf):
    
    """
        - coupleRouteur : le couple de routeur à mettre à jour : (<Routeur>, <Routeur>)
        - cout : cout pour passer d'un routeur à l'autre : int
    """
    
    def __init__(self, routeur_1, routeur_2, cout):
        self.coupleRouteur = (routeur_1, routeur_2)
        self.cout = cout
    
    
    def traiter(self, voisins, matrice, routeur_To_Index):
        routeur_1, routeur_2 = self.coupleRouteur
        
        try:
            indice_Routeur_1 = routeur_To_Index.index(routeur_1)
        except ValueError:                  #Cas où on découvre le routeur_1.
            n=len(matrice)
            for i in range(n):
                matrice[i].append(infini)
            new_Line = []
            for i in range(n):
                new_Line.append(infini)
            new_Line.append(0)
            matrice.append(new_Line)
            routeur_To_Index.append(routeur_1)
            indice_Routeur_1 = n
        
        try:
            indice_Routeur_2 = routeur_To_Index.index(routeur_2)
        except ValueError:                  #Cas où on découvre le routeur_2.
            n=len(matrice)
            for i in range(n):
                matrice[i].append(infini)
            new_Line = []
            for i in range(n):
                new_Line.append(infini)
            new_Line.append(0)
            matrice.append(new_Line)
            routeur_To_Index.append(routeur_2)
            indice_Routeur_2 = n
        
        matrice[indice_Routeur_1][indice_Routeur_2] = self.cout
        matrice[indice_Routeur_2][indice_Routeur_1] = self.cout



class RIP :
    
    """
        - table : correspond à la table du routeur associée au protocole RIP : list <EltTableRip>
        - voisins : Liste des voisins où l'on stockera un booléen qui est True si on a reçu la table du voisin en question et False sinon : list (<Routeur>, bool)
        - message_A_Traiter : liste des messages que l'on va devoir traiter lors des traitements : list <MessageRip>
        - routeur : c'est le routeur sur lequel est initialisé le protocole RIP : <Routeur>   #??????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
    """
    
    def __init__(self, routeur):
        self.table = []
        self.voisins = []
        self.messages_A_Traiter = []
        self.routeur = routeur
    
    def recevoirMessage(self, message):
        self.messages_A_Traiter.append(message)
    
    def envoyer(self, liste_Interfaces):
        for interface in liste_Interfaces:
            message = MessageRip(self.routeur, self.table)
            interface.reseau.broadcastRip(message)
    
    def UpdateAvecUneLigne(self, ligne_Table, expediteur):                  #Met à jour la table avec un seul EltTableRip.
        destination = ligne_Table.destination
        nouveau_Cout = ligne_Table.cout
        
        trouve = False
        for indice in range(len(self.table)):
            ligne_Temp = self.table[indice]
            if ligne_Temp.destination == destination:
                if nouveau_Cout+1 < ligne_Temp.cout:
                    self.table[indice].cout = nouveau_Cout+1
                    self.table[indice].next_Hop = expediteur
                    trouve = True
                elif ligne_Temp.next_Hop == expediteur:
                    self.table[indice].cout = nouveau_Cout+1
                    trouve = True
        
        if not trouve:
            nouv_Ligne = EltTableRip(destination, nouveau_Cout+1, expediteur)
            self.table.append(nouv_Ligne)
        
        if AMELIORATION:
            j=0
            while j<len(self.table):
                if self.table[j].cout>LIMIT:
                    self.table.pop(j)
                else :
                    j+=1
    
    def confirmeVoisin(self, expediteur):
        trouve = False
        
        for indice in range(len(self.voisins)):
            i_Routeur, i_Bool = self.voisins[indice]
            if i_Routeur == expediteur:
                self.voisins[indice] = (i_Routeur, True)
                trouve = True
        
        if trouve == False:
            self.voisins.append((expediteur, True))
    
    

    def traiter(self):
        """On traite les messages à traiter en appelant leur fonction traiter, et si certain des messages n'ont pas été traité, on les retire de la table."""
        
        for message in self.messages_A_Traiter:
            for elt in message.table:
                self.UpdateAvecUneLigne(elt, message.expediteur)
            self.confirmeVoisin(message.expediteur)
        
        
        indice = 0
        while indice < len(self.voisins):
            routeur, bool = self.voisins[indice]
            if not bool:                        #Si on a pas reçu la table d'un voisin,
                self.voisins.pop(indice)                    #On l'enlève des voisins.
                
                indice2=0
                while indice2 < len(self.table):
                    if self.voisins[indice2].next_Hop == self.voisins[indice]:
                        self.voisins.pop(indice)                    #Si le next_Hop d'une ligne est un voisin qui a disparu, on enlève la ligne.
                    indice2+=1
            indice+=1


class EltTableRip :
    
    """
        - destination : c'est l'adresse du réseau de destination : String ////////// Routeur destination : <Routeur>
        - cout : c'est le cout du chemin : int
        - next_Hop : c'est le routeur suivant par lequel il faut passer pour atteindre la destination : <Routeur>
    """
    
    def __init__(self, dest, cout, next_Hop):
        self.destination = dest
        self.cout = cout
        self.next_Hop = next_Hop


class MessageRip :
    
    """
        - expediteur : le routeur d'où provient le message : <Routeur>
        - table : la table de l'expediteur : list <EltTableRip>
        - protocole_Rip : protocole RIP qui est activé sur le routeur : <Routeur>
    """
    
    def __init__(self, expediteur, table):
        self.expediteur = expediteur
        self.table = table
    
    """def traiter(self):
        for elt in self.table:
            self.protocole_Rip.UpdateAvecUneLigne(elt, self.expediteur)
        self.protocole_Rip.confirmeVoisin(self.expediteur)"""
