
infini = float('inf')

DEBUG = True                    #Active ou désactive le mode débug.

def copieListe(liste):                  #Crée et retourne une copie de liste. 
    copie=[]
    for i in range(len(liste)):
        copie.append(liste[i])
    return copie



class OSPF :
    
    """
        - matrice : c'est l'ensemble du reseau où chaque routeur est représenté par un indice, le lien se fait grace à la liste routeur_To_Index; l'élément dans la case (i, j) est la distance directe du routeur i au routeur j et inf si ils ne sont pas directement reliés : list list int
        - routeur_To_Index : fait le lien entre un routeur et son indice dans matrice qui est aussi son indice dans routeur_To_Index : list <Routeur>
        - liste_Chemin : la liste que l'on cherche à obtenir, celle qui donne le chemin a emprunter : liste <CheminOspf>
        - messages_A_Traiter : liste des messages qui devront etre traité lors de l'étape de traitement : list <MessageOspf>
        - messages_A_Envoyer : liste des messages qui devront etre envoyer lors de l'étape d'envoie : list <UpdateOspf>
        - voisins : liste des routeurs qui sont les proches voisins du routeur concerné et qui contient un booléen qui donne si oui ou non le routeur a envoyé un message hello lors de la phase d'envoie : list (<Routeur>, bool)
        - routeur : routeur sur lequel est activé ce protocole Ospf : <Routeur>
    """
    
    def __init__(self, routeur):
        self.matrice = [[0]]
        self.routeur_To_Index = [routeur]
        self.liste_Chemin = []
        self.messages_A_Traiter = []
        self.messages_A_Envoyer = []
        self.voisins = []
        self.routeur = routeur
    
    
    def recevoirMessage(self, message):
        self.messages_A_Traiter.append(message)
    
    def envoyer(self, liste_Interfaces):
        """On envoie les messages à envoyer puis on envoie les hellos à tous les voisins."""
        
        for interface in liste_Interfaces:
            
            for message in self.messages_A_Envoyer:
                interface.reseau.broadcastOspf(message)
            
            hello = HelloOspf(self.routeur, interface.reseau)                   #On crée et on envoie les messages hello pour que nos voisins soient au courant que l'on est pas mort.
            interface.reseau.broadcastOspf(hello)
    
    def envoyerUnMessageOspfPartoutSauf(self, message):
        reseau_Ne_Pas_Envoyer = message.reseau_Emission
        
        for interface in self.routeur.liste_Interfaces:
            if not interface.reseau == reseau_Ne_Pas_Envoyer:
                interface.reseau.broadcastOspf(message)
    
    def envoyerMatriceSur(self, reseau):
        taille_Mat = len(self.matrice)
        for indice_Ligne in range(taille_Mat):
            for indice_Colonne in range(indice_Ligne, taille_Mat):
                message_Update = UpdateOspf(self.routeur_To_Index[indice_Ligne], self.routeur_To_Index[indice_Colonne], reseau)
                reseau.broadcastOspf(message_Update)
    
    def trouverRouteurDansChemin(self, routeur):
        for chemin in self.liste_Chemin:
            if chemin.chemin[-1] == routeur:
                chemin_Recherche = chemin
                break
        return chemin_Recherche
    
    def traiter(self):
        """On traite chacun des messages grace à leur méthode traiter(), puis on regarde dans voisins si tous les voisins sont encore là, sinon on agit en conséquence. Puis on applique Dijkstra pour avoir liste_Chemin."""
        
        for message in self.messages_A_Traiter:
            message.traiter(self.voisins, self.matrice, self.routeur_To_Index, self.routeur)
        
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
        - reseau_Emission : c'est le reseau par lequel transite ce message hello : <Reseau>
    """
    
    def __init__(self, expediteur, reseau_Emission):
        self.expediteur = expediteur
        self.reseau_Emission = reseau_Emission
    
    
    def traiter(self, voisins, matrice, routeur_To_Index, routeur_Qui_Recoit):
        indice_Recherche = -1
        for indice in range(len(voisins)):
            routeur, bool = voisins[indice]
            if routeur == self.expediteur:
                indice_Recherche = indice
                break
        if indice_Recherche == -1 :                 #Si on a découvert un nouveau routeur :
            voisins.append((self.expediteur, True))                 #on le rajoute dans la liste des voisins,
            
            update_Perso = UpdateOspf(routeur_Qui_Recoit, self.expediteur, self.reseau_Emission)                    #on crée une update Ospf qu'on traite immédiatement et qui représente le lien entre ce nouveau routeur et le routeur qui reçoit,
            update_Perso.traiter(voisins, matrice, routeur_To_Index, routeur_Qui_Recoit)                    #on traite immédiatement (pour ne pas perdre un tour),
            
            routeur_Qui_Recoit.protocole_Ospf.envoyerMatriceSur(self.reseau_Emission)                   #on envoie entièrement notre matrice sur le réseau d'où arrive le hello : afin que le nouveau routeur soit au courant des routeurs dans le reseau.
            
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
        - reseau_Emission : réseau d'où provient le message : <Reseau>
    """
    
    def __init__(self, routeur_1, routeur_2, reseau_Emission):
        self.coupleRouteur = (routeur_1, routeur_2)
        self.cout = reseau_Emission.bande_Passante
        self.reseau_Emission = reseau_Emission
    
    
    def traiter(self, voisins, matrice, routeur_To_Index, routeur_Qui_Recoit):
        routeur_1, routeur_2 = self.coupleRouteur
        decouvert_Un_Routeur = False
        
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
            
            decouvert_Un_Routeur = True
        
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
            
            decouvert_Un_Routeur = True
        
        ancien_Cout = matrice[indice_Routeur_1][indice_Routeur_2]
        
        modification_Cout = False
        if ancien_Cout != self.cout:
            matrice[indice_Routeur_1][indice_Routeur_2] = self.cout
            matrice[indice_Routeur_2][indice_Routeur_1] = self.cout
            modification_Cout = True
        
        if decouvert_Un_Routeur or modification_Cout:
            routeur_Qui_Recoit.protocole_Ospf.envoyerUnMessageOspfPartoutSauf(self)
