
infini = float('inf')
dixPuissNeuf = 1000000000

DEBUG = False                    #Active ou désactive le mode débug.

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
    
    def afficheCheminsOspf(self):                   #Affiche l'ensemble des chemins du routeur sur lequel est activé cet objet OSPF.
        for chemin in self.liste_Chemin:
            string = 'Chemin depuis ' + self.routeur.___nom___ + ' vers ' + chemin.destination.___nom___ + ' :' + chemin.donnerChemin()
            print(string)
    
    def afficheMatrice(self):                   #Affiche la matrice et la correspondance indice/routeur.
        nom_Routeur_To_Index = []
        for indice in range(len(self.routeur_To_Index)):
            nom_Routeur_To_Index.append((indice, self.routeur_To_Index[indice].___nom___))
        print(nom_Routeur_To_Index)
        print(self.matrice)
    
    
    def recevoirMessageOspf(self, message):
        self.messages_A_Traiter.append(message)
    
    def ajouterMessageAEnvoyerOspf(self, message):
        self.messages_A_Envoyer.append(message)
    
    def envoyerOspf(self, liste_Interfaces):
        """On envoie les messages à envoyer puis on envoie les hellos à tous les voisins."""
        
        while not len(self.messages_A_Envoyer)==0:
            self.messages_A_Envoyer[0].reseau_Emission.broadcastOspf(self.messages_A_Envoyer[0])
            self.messages_A_Envoyer.pop(0)
        
        for interface in liste_Interfaces:
            
            """for message in self.messages_A_Envoyer:                      #On n'envoie pas tous les messages sur tous les réseaux, mais uniquement sur le réseau qui est inscrit emission dans le message.
                interface.reseau.broadcastOspf(message)"""
            
            hello = HelloOspf(self.routeur, interface.reseau)                   #On crée et on envoie les messages hello pour que nos voisins soient au courant que l'on est pas mort.
            interface.reseau.broadcastOspf(hello)
    
    """def envoyerUnMessageOspfPartoutSauf(self, message):                 #Fait un broadcast 
        reseau_Ne_Pas_Envoyer = message.reseau_Emission
        
        for interface in self.routeur.liste_Interfaces:
            if not interface.reseau == reseau_Ne_Pas_Envoyer:
                interface.reseau.broadcastOspf(message)"""
    
    def envoyerMatriceSur(self, reseau):
        if DEBUG:
            print("On ajoute une matrice complète aux messages à envoyer")
        
        taille_Mat = len(self.matrice)
        for indice_Ligne in range(taille_Mat):
            for indice_Colonne in range(indice_Ligne, taille_Mat):
                message_Update = UpdateOspf(self.routeur_To_Index[indice_Ligne], self.routeur_To_Index[indice_Colonne], reseau, self.routeur, self.matrice[indice_Ligne][indice_Colonne])
                self.routeur.protocole_Ospf.ajouterMessageAEnvoyerOspf(message_Update)
    
    def trouverRouteurDansChemin(self, routeur):
        for chemin in self.liste_Chemin:
            if chemin.chemin[-1] == routeur:
                chemin_Recherche = chemin
                return chemin_Recherche
    
    
    def traiterOspf(self):
        """On traite chacun des messages grace à leur méthode traiter..., on supprime le message, puis on regarde dans voisins si tous les voisins sont encore là, sinon on agit en conséquence. Puis on applique Dijkstra pour avoir liste_Chemin."""
        
        self.liste_Chemin=[]                     #(On la remet à 0, car on va la remplir). C'est la liste qui contiendra les objets <CheminOspf>. //distances de indice_Routeur au routeur représenté par l'indice de la liste ainsi que le chemin à emprunter (sera sous forme de liste de couples (int list, int)).
        
        while not len(self.messages_A_Traiter)==0:
            self.messages_A_Traiter[0].traiter(self.voisins, self.matrice, self.routeur_To_Index, self.routeur)
            self.messages_A_Traiter.pop(0)
        
        indice = 0
        while indice < len(self.voisins):
            routeur, bool = self.voisins[indice]
            if not bool:                 #Si le routeur n'a pas envoyé de message hello.
                self.voisins.pop(indice)                    #On l'enlève des voisins.
                
                """
                indice_In_Mat = self.routeur_To_Index.index(routeur)
                for elt in self.matrice:
                    elt.pop(indice_In_Mat)                  #On l'enlève de matrice.
                self.matrice.pop(indice_In_Mat)                 #On enlève sa colonne entièrement.
                
                self.routeur_To_Index.pop(indice_In_Mat)                    #On l'enlève de la liste des correspondances.
                """
                
                #On met à jour la matrice vis à vis du lien qui a été rompu.
                indice_Routeur_1 = self.routeur_To_Index.index(self.routeur)
                indice_Routeur_2 = self.routeur_To_Index.index(routeur)
                self.matrice[indice_Routeur_1][indice_Routeur_2] = infini
                self.matrice[indice_Routeur_2][indice_Routeur_1] = infini
                
                for interface in self.routeur.liste_Interfaces:
                    message_De_Deconnexion = UpdateOspf(self.routeur, routeur, interface.reseau, self.routeur, infini)
                    self.routeur.protocole_Ospf.ajouterMessageAEnvoyerOspf(message_De_Deconnexion)
            
            indice += 1
        
        self.dijkstra()
        
        for indice in range(len(self.voisins)):                  #On remet la vérification des routeurs à False.
            routeur, bool = self.voisins[indice]
            self.voisins[indice] = (routeur, False)
    
    def dijkstra (self):
        
        indice_Routeur_Self = self.routeur_To_Index.index(self.routeur)
        
        for indice in range(len(self.matrice)):                 #On initialise les chemins depuis self jusqu'aux routeurs concernés.
            obj_Chemin = CheminOspf(self.routeur_To_Index[indice], self.matrice[indice][indice_Routeur_Self], [self.routeur_To_Index[indice]])
            self.liste_Chemin.append(obj_Chemin)
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
            
            #Pas besoin de faire de retrour. On a alors la distance minimale de self.routeur à chaque routeur ainsi que le chemin à parcourir le tout dans des objets CheminOspf.


class CheminOspf :
    
    """
        - destination : adresse du reseau destination : String ////// Pour l'instant c'est <Routeur>
        - cout : le cout pour atteindre cette destination : int
        - chemin : c'est le chemin a emprunter pour atteindre destination en cout : list <Routeur>
    """
    
    def __init__(self, destination, cout, chemin):
        self.destination = destination
        self.cout = cout
        self.chemin = chemin
    
    def donnerChemin(self):                 #Fonction qui retourne un string représentant le chemin.
        string = ''
        for routeur in self.chemin:
            string = string + ' - '+ routeur.___nom___
        return string
    
    
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
        indice_Recherche = -1                   #Représente l'indice du routeur si il est dans les voisins.
        for indice in range(len(voisins)):
            routeur, bool = voisins[indice]
            if routeur == self.expediteur:
                indice_Recherche = indice
                break
        if indice_Recherche == -1 :                 #Si on a découvert un nouveau routeur :
            tuple = (self.expediteur, True)
            voisins.append(tuple)                 #On le rajoute dans la liste des voisins.
            
            #Mise à jour de la matrice
            n=len(matrice)
            for i in range(n):                  #On rajoute un élément à toutes les lignes de la matrice (c'est le nouveau routeur).
                matrice[i].append(infini)
            new_Line = []
            for i in range(n):
                new_Line.append(infini)
            new_Line.append(0)
            matrice.append(new_Line)                    #On ajoute une ligne en plus à notre matrice, elle contient les cout du nouveau routeur vers les autres (le dernier élément est 0 car c'est du routeur vers lui-meme).
            routeur_To_Index.append(self.expediteur)
            
            #On met à jour le coup de la nouvelle liaison dans la matrice.
            indice_Self = routeur_To_Index.index(routeur_Qui_Recoit)
            cout = dixPuissNeuf/self.reseau_Emission.bande_Passante
            matrice[n][indice_Self] = cout
            matrice[indice_Self][n] = cout
            
            """
            update_Perso = UpdateOspf(routeur_Qui_Recoit, self.expediteur, self.reseau_Emission, routeur_Qui_Recoit, dixPuissNeuf/self.reseau_Emission.bande_Passante)                    #on crée une update Ospf qu'on traite immédiatement et qui représente le lien entre ce nouveau routeur et le routeur qui reçoit,
            update_Perso.traiter(voisins, matrice, routeur_To_Index, routeur_Qui_Recoit)                    #on traite immédiatement (pour ne pas perdre un tour),
            """
            
            routeur_Qui_Recoit.protocole_Ospf.envoyerMatriceSur(self.reseau_Emission)                   #on envoie entièrement notre matrice sur le réseau d'où arrive le hello : afin que le nouveau routeur soit au courant des routeurs dans le reseau.
            
            for interface in routeur_Qui_Recoit.liste_Interfaces:
                    message_De_Connexion = UpdateOspf(self.expediteur, routeur_Qui_Recoit, interface.reseau, routeur_Qui_Recoit, cout)
                    routeur_Qui_Recoit.protocole_Ospf.ajouterMessageAEnvoyerOspf(message_De_Connexion)
            
            if DEBUG:
                print("On a découvert un nouveau routeur")
            
        else :
            voisins[indice_Recherche] = (self.expediteur, True)


    
class UpdateOspf(MessageOspf):
    
    """
        - coupleRouteur : le couple de routeur à mettre à jour : (<Routeur>, <Routeur>)
        - cout : cout pour passer d'un routeur à l'autre (ceux du couple) qui est en fait 10^9 / bande passante : int
        - reseau_Emission : réseau d'où provient le message : <Reseau>
        - expediteur : routeur d'où provient le update : <Routeur>
    """
    
    def __init__(self, routeur_1, routeur_2, reseau_Emission, expediteur, cout):
        self.coupleRouteur = (routeur_1, routeur_2)
        self.reseau_Emission = reseau_Emission
        self.expediteur = expediteur
        self.cout = cout                  ##C EST PAS LA BANDE PASSANTE DU RESEAU PAR LEQUEL ON LE RECOIT !!!!!!!!!!!!!!! Mais bien la bande passante qu'on doit définir lors de la création du message.
    
    def __str__(self):
        return "cout = " + str(self.cout)
    
    def traiter(self, voisins, matrice, routeur_To_Index, routeur_Qui_Recoit):                  #traitement du message Update.
        routeur_1, routeur_2 = self.coupleRouteur
        decouvert_Un_Routeur = False                    #A t on découvert un nouveau routeur ?
        
        try:
            indice_Routeur_1 = routeur_To_Index.index(routeur_1)
        except ValueError:                  #Cas où on découvre le routeur_1.
            n=len(matrice)
            for i in range(n):                  #On rajoute un élément à toutes les lignes de la matrice (c'est le nouveau routeur).
                matrice[i].append(infini)
            new_Line = []
            for i in range(n):
                new_Line.append(infini)
            new_Line.append(0)
            matrice.append(new_Line)                    #On ajoute une ligne en plus à notre matrice, elle contient les cout du nouveau routeur vers les autres (le dernier élément est 0 car c'est du routeur vers lui-meme).
            routeur_To_Index.append(routeur_1)
            indice_Routeur_1 = n
            
            decouvert_Un_Routeur = True                 #On a découvert un routeur.
        
        try:
            indice_Routeur_2 = routeur_To_Index.index(routeur_2)
        except ValueError:                  #Cas où on découvre le routeur_2.
            n=len(matrice)
            for i in range(n):                  #On rajoute un élément à toutes les lignes de la matrice (c'est le nouveau routeur).
                matrice[i].append(infini)
            new_Line = []
            for i in range(n):
                new_Line.append(infini)
            new_Line.append(0)
            matrice.append(new_Line)                    #On ajoute une ligne en plus à notre matrice, elle contient les cout du nouveau routeur vers les autres (le dernier élément est 0 car c'est du routeur vers lui-meme).
            routeur_To_Index.append(routeur_2)
            indice_Routeur_2 = n
            
            decouvert_Un_Routeur = True                 #On a découvert un routeur.
        
        ancien_Cout = matrice[indice_Routeur_1][indice_Routeur_2]
        
        modification_Cout = False                   #A t on eu une modification de cout qui entrainerait un renvoie d'update ?
        
        
        if self.cout < ancien_Cout:                 #Si le cout qui est dans la table est plus grand que le cout donné par l'update.
            matrice[indice_Routeur_1][indice_Routeur_2] = self.cout
            matrice[indice_Routeur_2][indice_Routeur_1] = self.cout
            modification_Cout = True
        
        elif self.cout == infini and not ancien_Cout == infini:
            matrice[indice_Routeur_1][indice_Routeur_2] = self.cout
            matrice[indice_Routeur_2][indice_Routeur_1] = self.cout
            modification_Cout = True
        
        if decouvert_Un_Routeur or modification_Cout:                   #Si il y a eu une modification ou un nouveau routeur, on doit renvoyer l'update (mise à jour avec le routeur émission correcte.
            for interface in routeur_Qui_Recoit.liste_Interfaces:
                if not interface.reseau == self.reseau_Emission:                    #Si le réseau n'est pas celui d'où on a reçu l'update, on la diffuse dessus.
                    new_Message_Update = UpdateOspf(routeur_1, routeur_2, interface.reseau, routeur_Qui_Recoit, self.cout)                  #Nouvelle update puisque le réseau d'émission n'est pas forcément le meme que dans self.
                    routeur_Qui_Recoit.protocole_Ospf.ajouterMessageAEnvoyerOspf(new_Message_Update)
            if DEBUG:
                print("renvoie du message update : ", self)
