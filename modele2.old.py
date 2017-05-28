#On prendra dans tout le modèle le masque 255.255.255.0; on a alors au maximum 254 equipements sur notre réseau (on garde une adresse pour le réseau et une pour le broadcast).

from threading import Thread, RLock

class Reseau :
    
    """ Reseau ayant :
        - une adresse
        - une liste ayant des 1 si l'indice correspondant est associé à une adresse déjà utilisée ou 0 sinon.
    """
    
    def __init__(self,  adresse):
        self.adresse = adresse
        self.routeurs_In = [1]                   #Liste qui contiendra 0 si l'indice correspond à une adresse disponible (non marquée) pour un routeur ou 1 si elle ne l'est pas (déjà utilisée ie. marquée).
        self.

    def enregistrerRouteur(self):                    #Modifie la liste des disponibilité d'adresse dans le réseau et renvoie l'adresse disponible
        n = len(self.routeurs_In)
        indice_Dispo = -1
        booleen = False
        indice = 0
        while not booleen and indice<n:
            if self.routeurs_In[indice] == 0 :
                self.routeurs_In[indice] = 1
                indice_Dispo = indice
                booleen = True
            indice += 1

        if n<255 and not booleen:
            self.routeurs_In.append(1)
            indice_Dispo = n
        
        if indice_Dispo == -1 :
            raise BufferError("Le reseau est sature, on ne peut ajouter de routeur dans ce reseau")
        else :
            return self.getAdresseGenerique()+str(indice_Dispo)
    
    def getAdresseGenerique(self):
        h_Index = self.adresse.rfind('.')
        return self.adresse[:h_Index]+'.'



class Routeur :

    """ Routeur ayant :
        - une liste de ses interfaces avec les adresses des réseaux auxquels elles sont connectées
        - une liste contenant les routeurs directement adjacents (à l'initialisation elle est vide)
        - une liste table de routage pour OSPF
        - une liste table de routage pour RIP.
    """

    def __init__(self, reseaux) :                 #reseaux est une liste contenant les différents réseaux dans lesquels le routeur a les pieds.
        n = len(reseaux)
        self.interfaces = []
        for indice in range(n):
            adresse_Interface = reseaux[indice].enregistrerRouteur()
            self.interfaces.append((indice, adresse_Interface))                  #On construit la liste des interfaces avec leur numéro et leur adresse ip (on leur donne un numéro de façon arbitraire). On peut avoir un nombre infini d'interface.
        
        self.routeur_Adjacents = []                 #Uniquement utile pour OSPF.
        
        self.buffer = []                    #File d'attente des messages à traiter par RIP sur un routeur.
        self.verrou = RLock()                   #Lock qui empèche aux threads d'accéder en meme temps au buffer.
        
        
    
    def addMessage(self, message):
        self.verrou.acquire()
        self.buffer.append(message)
        self.verrou.release()



class RipTableElement :
    
    """ RipTableElement ayant :
        - un triplet (destination, cout, next_Hop).                  #C'est une ligne de notre table de routage.
    """
    
    def __init__(self, destination, cout, next_Hop):                 #destination est l'adresse ip du réseau destination; cout est le cout pour atteindre cette destination (le nombre de saut); next_Hop est l'adresse du routeur par lequel il faut passer pour la première étape. 
        self.ligne = (destination, cout, next_Hop)



#class TableOspf :



class MessageRip :
    
    def __init__(self, adresse_Expediteur, table):
        self.expediteur = adresse_Expediteur
        self.table_A_Traiter = table



class ThreadRipEnvoie(Thread):
    
    #Thread qui s'occupe d'envoyer les messagesRip au routeur sur le meme réseau (en broadcast).
    
    def __init__(self, routeur):
        Thread.__init__(self)
        self.routeur = routeur
    
    def run(self):
        



class ThreadRipTraitement(Thread):
    
    #Thread qui traite la file d'attente des tables à traiter.
