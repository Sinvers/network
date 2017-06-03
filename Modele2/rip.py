
LIMIT = 15                  #Limite du nombre de saut pour RIP.

AMELIORATION = False                 #Active (True) ou désactive (False) les améliorations.

DEBUG = False                    #Active ou désactive le mode débug.

def copieListe(liste):                  #Crée et retourne une copie de liste. 
    copie=[]
    for i in range(len(liste)):
        copie.append(liste[i])
    return copie



class RIP :
    
    """
        - routeur : c'est le routeur sur lequel est initialisé le protocole RIP : <Routeur>
        - table : correspond à la table du routeur associée au protocole RIP : list <EltTableRip>
        - voisins : Liste des voisins où l'on stockera un couple dont le booléen qui est True si on a reçu la table du voisin en question et False sinon : list (<Routeur>, bool)
        - messages_A_Traiter : liste des messages que l'on va devoir traiter lors des traitements : list <MessageRip>
    """
    
    def __init__(self, routeur):
        self.routeur = routeur
        soi_Meme = EltTableRip(self.routeur, 0, self.routeur)
        self.table = [soi_Meme]
        self.voisins = []
        self.messages_A_Traiter = []
    
    def afficherTableRip(self):
        for elt in self.table:
            print(elt.donnerEltTableRip())

    
    def recevoirMessageRip(self, message):
        self.messages_A_Traiter.append(message)
    
    def envoyerRip(self, liste_Interfaces):
        for interface in liste_Interfaces:
            copie_Table = copieListe(self.table)
            message = MessageRip(self.routeur, copie_Table)
            interface.reseau.broadcastRip(message)
    
    def UpdateAvecUneLigne(self, ligne_Table, expediteur):                  #Met à jour la table avec un seul EltTableRip.
        destination = ligne_Table.destination
        nouveau_Cout = ligne_Table.cout
        
        trouve = False                      #A t on trouvé la destination dans la table sur le routeur ?
        for indice in range(len(self.table)):
            ligne_Temp = self.table[indice]
            if ligne_Temp.destination == destination:
                trouve = True
                
                if nouveau_Cout+1 < ligne_Temp.cout:                    #Si le cout proposé par la nouvelle update + 1 est plus petit que celui d'avant, on modifie notre table.
                    self.table[indice].cout = nouveau_Cout+1
                    self.table[indice].next_Hop = expediteur
                    self.table[indice].confirme = True
                if ligne_Temp.next_Hop == expediteur:                 #Si le routeur qui a envoyé l'update est celui par qui on devait passer on est obligé de modifier notre table car c'est lui qui controle le coup.
                    self.table[indice].cout = nouveau_Cout+1
                    self.table[indice].confirme = True
        
        if not trouve:
            nouv_Ligne = EltTableRip(destination, nouveau_Cout+1, expediteur)
            self.table.append(nouv_Ligne)                   #Si on l'a pas trouvé c'est qu'on a une nouvelle information alors on ajoute cette information à notre table (on recrée un objet car sinon on ajouterait toujours le meme objet).
        
        if AMELIORATION:                    #Une amélioration de RIP consiste à enlever les chemins dont le cout est superieur à une certaine limite (ici LIMIT) afin d'éviter des chemins infinis (qui s'incrémentent à chaque tour).
            j=0
            while j<len(self.table):
                if self.table[j].cout>LIMIT:
                    self.table.pop(j)
                else :
                    j+=1
    
    def confirmeVoisin(self, expediteur):                   #Confirme que le voisin a bien envoyé sa table pendant ce tour, ie. passe à True le booléen correspondant au routeur dans voisins.
        trouve = False                  #A t on trouvé le routeur dans les voisins ?
        
        for indice in range(len(self.voisins)):
            i_Routeur, i_Bool = self.voisins[indice]
            if i_Routeur == expediteur:
                self.voisins[indice] = (i_Routeur, True)                    #Si le voisin dans la liste est celui qui a envoyé le message alors on le marque comme présent (pour ce tour).
                trouve = True
        
        if trouve == False:
            self.voisins.append((expediteur, True))                 #Si le routeur qui a envoyé le message n'est pas dans la liste des voisins alors on le rajoute et on le marque comme présent (pour ce tour).
    
    

    def traiter(self):
        """On traite les messages à traiter en appelant leur fonction traiter, et si certain des messages n'ont pas été traité, on les retire de la table."""
        
        for message in self.messages_A_Traiter:                 #On traite les messages à traiter.
            for elt in message.table:
                self.UpdateAvecUneLigne(elt, message.expediteur)                    #On update self.table avec chacun des éléments de la table qui est dans le message.
            self.confirmeVoisin(message.expediteur)
        
        self.messages_A_Traiter = []                    #On remet la liste vide puisqu'on a alors traité tous les messages.
        
        
        indice = 0
        while indice < len(self.voisins):
            routeur, bool = self.voisins[indice]
            if not bool:                        #Si on a pas reçu la table d'un voisin,
                self.voisins.pop(indice)                    #On l'enlève des voisins.
                
                indice2=0
                while indice2 < len(self.table):
                    if self.voisins[indice2].next_Hop == self.voisins[indice]:
                        self.table.pop(indice)                    #Si le next_Hop d'une ligne est un voisin qui a disparu, on enlève la ligne.
                    indice2+=1
            indice+=1
        
        indice = 0
        while indice < len(self.table):
            if not self.table[indice].confirme: #and not self.table[indice].destination == self.routeur:
                self.table.pop(indice)
            elif not self.table[indice].destination == self.routeur:                    #Le routeur sur lequel est initialisé le routeur sait toujours que le chemin pour aller de lui-même vers lui-même coute 0 en passant par lui-même (on ne doit donc pas mettre confirmer à False).
                self.table[indice].confirme = False
            indice += 1
        
        for elt in self.voisins:
            routeur, _ = elt
            elt = routeur, False


class EltTableRip :
    
    """
        - destination : c'est l'adresse du réseau de destination : String ////////// Routeur destination : <Routeur>
        - cout : c'est le cout du chemin : int
        - next_Hop : c'est le routeur suivant par lequel il faut passer pour atteindre la destination : <Routeur>
        - confirme : explicite si cette ligne de la table est toujours d'actualité (si on l'a bien reçu pendant ce tour) : bool
    """
    
    def __init__(self, dest, cout, next_Hop):
        self.destination = dest
        self.cout = cout
        self.next_Hop = next_Hop
        self.confirme = True
    
    def donnerEltTableRip(self):
        string = 'Destination : ' + self.destination.___nom___ + ' en ' + str(self.cout) + ' et en passant par ' + self.next_Hop.___nom___
        return string


class MessageRip :
    
    """
        - expediteur : le routeur d'où provient le message : <Routeur>
        - table : la table de l'expediteur : list <EltTableRip>
    """
    
    def __init__(self, expediteur, table):
        self.expediteur = expediteur
        self.table = table
    
    """def traiter(self):
        for elt in self.table:
            self.protocole_Rip.UpdateAvecUneLigne(elt, self.expediteur)
        self.protocole_Rip.confirmeVoisin(self.expediteur)"""
