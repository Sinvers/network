#On prendra dans tout le modèle le masque 255.255.255.0; on a alors au maximum 254 equipements sur notre réseau (on garde une adresse pour le réseau et une pour le broadcast).


class Reseau :
    
    """ Reseau ayant :
        - une adresse
        - une liste ayant des 1 si l'indice correspondant est associé à une adresse déjà utilisée ou 0 sinon.
    """
    
    def __init__(self,  adresse):
        self.adresse = adresse
        self.routeurs_In = [1]                   #Liste qui contiendra 0 si l'indice correspond à une adresse disponible (non marquée) pour un routeur ou 1 si elle ne l'est pas (déjà utilisée ie. marquée).

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
        - une liste contenant les routeurs directement adjacents (à l'initialisation elle est vide).
    """
    
    def __init__(self, reseaux) :                 #reseaux est une liste contenant les différents réseaux dans lesquels le routeur a les pieds.
        n = len(reseaux)
        self.interfaces = []
        for indice in range(n):
            adresse_Interface = reseaux[indice].enregistrerRouteur()
            self.interfaces.append((indice, adresse_Interface))                  #On construit la liste des interfaces avec l'adresse du réseau dans lequel cette interface est (on leur donne un numéro de façon arbitraire). On peut avoir un nombre infini d'interface.
        
        self.routeur_Adjacents = []
    
    
class RipTableElement :
    
    
    
    
    
#class TableOspf :
    
    
    
