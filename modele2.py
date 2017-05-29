
infini = float('inf')


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
            routeur.ajoutMessageRip
    
class Routeur :
    
    """
        - liste_Interfaces : liste des interfaces du routeur : list <Interface>
        - protocole_Ospf : objet correspondant au fonctionnement de OSPF sur ce routeur : <OSPF>
        - protocole_Rip : objet correspondant au fonctionnement de RIP sur ce routeur : <RIP>
    """
    
    def __init__(self, liste_Reseau):
        self.protocole_Ospf = OSPF(self)
        self.protocole_Rip = RIP()
        
        self.liste_Interfaces = []
        n=len(liste_Reseau)
        for indice in range(n):
            try:
                adresse_Sur_Reseau = liste_Reseau[indice].enregistrerRouteur(self)
                interface = InterfaceReseau(adresse_Sur_Reseau, liste_Reseau[indice])
                self.liste_Interfaces.append(interface)
            except BufferError:
                print("Le routeur n'a pas pu etre ajouté au reseau ",  liste_Reseau[indice], " car il est saturé")
    
    
    def supprimerReseau(self, reseau):
        for indice_Interface in range(len(self.liste_Interfaces)):
            if self.liste_Interfaces[indice_Interface].reseau == reseau:
                self.liste_Interfaces.pop(indice_Interface)
                break
    
    
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
    
    

class InterfaceReseau :
    
    """
        - adresse : adresse du routeur dans le réseau reseau : String
        - reseau : réseau dans lequel cette interface a les pieds : <Reseau>
    """
    
    def __init__(self, adresse_Du_Routeur, reseau):
        self.adresse = adresse_Du_Routeur
        self.reseau = reseau
    
    
class OSPF :
    
    """
        - matrice : c'est l'ensemble du reseau où chaque routeur est représenté par un indice, le lien se fait grace à la liste routeur_To_Index; l'élément dans la case (i, j) est la distance directe du routeur i au routeur j et inf si ils ne sont pas directement reliés : list list int
        - routeur_To_Index : fait le lien entre un routeur et son indice dans matrice qui est aussi son indice dans routeur_To_Index : list <Routeur>
        - liste_Chemin : la liste que l'on cherche à obtenir, celle qui donne le chemin a emprunter : liste <CheminOspf>
        - messages_A_Traiter : liste des messages qui devront etre traité lors de l'étape de traitement : list <MessageOspf>
        - messages_A_Envoyer : liste des messages qui devront etre envoyer lors de l'étape d'envoie : list <UpdateOspf>
        - voisins : liste des routeurs qui sont les proches voisins du routeur concerné et qui contient un booléen qui donne si oui ou non le routeur a envoyé un message hello lors de la phase d'envoie : list <<Routeur>, bool>
    """
    
    def __init__(self, routeur):
        self.matrice = [[]]
        self.routeur_To_Index = []
        self.liste_Chemin = []
        self.messages_A_Traiter = []
        self.messages_A_Envoyer = []
        self.voisins = []
        self.routeur = routeur
    
    def recevoirMessage(self, message):
        self.messages_A_Traiter.append(message)
    
    def envoyer(self, liste_Interfaces):
        """On envoie les messages à envoyer puis on envoie les hellos à tous les voisins."""
        
        hello = HelloOspf(self)                 #On crée le message hello qui sera destiné à tous les voisins.
        
        for interface in liste_Interfaces:
            
            for message in self.messages_A_Envoyer:
                interface.reseau.broadcastOspf(message)
            
            interface.reseau.broadcastOspf(hello)
        
    
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
                self.matrice.pop(indice_In_Mat)
                
                self.routeur_To_Index.pop(indice_In_Mat)                    #On l'enlève de la liste des correspondances.
            
            indice += 1
        
        self.liste_Chemin = self.dijkstra()
    
    def dijkstra (self):
        liste_Chemin=[]                    #C'est la liste qui contiendra les objets <CheminOspf>. //distances de indice_Routeur au routeur représenté par l'indice de la liste ainsi que le chemin à emprunter (sera sous forme de liste de couples (int list, int)).
        indice_Self = self.routeur_To_Index.index(self.routeur)
        
        for indice in range(len(self.matrice)):                 #On initialise les chemins depuis self jusqu'aux routeurs concernés.
            obj_Chemin = CheminOspf(self.routeur_To_Index[indice], self.matrice[indice][indice_Self], [self.routeur_To_Index[indice]])
            liste_Chemin.append(obj_Chemin)
        
        #n = len(table_Totale[indice_Routeur])
        S = [self.routeur]                    #Contient les routeurs déjà traités.
        S_Compl = []                    #Contiendra les routeurs non encore traités.
        for i in range(n):
            if i != indice_Routeur :
                S_Compl.append(i)
        #print("S_Compl = ", S_Compl)
        
        while len(S_Compl) != 0 :
            #print("d = ", d)
            
            min=S_Compl[0]
            indice_Min=0                    #Indice du routeur dans S_Compl.
            for j in range(len(S_Compl)) :                  #Recherche du routeur parmis S_Compl dont la distance à indice_Routeur est la plus faible.
                chemin_Min, distance_Min = d[min]
                _, distance_Temp = d[S_Compl[j]]
                if distance_Temp<distance_Min :
                    min = S_Compl[j]
                    indice_Min = j
            #print("min, indice : ",  min,  indice_Min)
            S.append(S_Compl[indice_Min])                    #On ajoute à S le routeur que l'on vient de traiter.
            S_Compl.pop(indice_Min)                  #On l'enlève de S_Compl.
            #print("dmin = ", d[min])
            
            chemin_Min, distance_Min = d[min]
            for k in range(len(S_Compl)):                   #Pour chaque routeur non encore traité, on compare sa distance à indice_Routeur qu'on avait précédemment (dans d) avec celle en passant par le routeur à distance minimale de cette étape.
                chemin, ancienne_Dist = d[S_Compl[k]]
                #print("chemin,k",  chemin, k)
                if ancienne_Dist>distance_Min+table_Totale[min][S_Compl[k]]:
                    chemin_Nouv = copieListe(chemin_Min)
                    chemin_Nouv.append(S_Compl[k])
                    #print("Chemin min : ", chemin_Min)
                    #print ("Nouveau chemin : ", chemin_Nouv)
                    d[S_Compl[k]]=(chemin_Nouv, distance_Min + table_Totale[min][S_Compl[k]])
            #print("S_Compl = ", S_Compl)
            #print(d)
            
        return d                    #On a alors la distance minimale de indice_Routeur à chaque routeur ainsi que le chemin à parcourir.


class CheminOspf :
    
    """
        - destination : adresse du reseau destination : String
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



#class RIP :
    
    


#class EltTableRip :
    
    
    

#class MessageRip :
    
    
    

