
LIMIT = 15                  #Limite du nombre de saut pour RIP.

AMELIORATION = True                 #Active (True) ou désactive (False) les améliorations.

DEBUG = True                    #Active ou désactive le mode débug.



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
