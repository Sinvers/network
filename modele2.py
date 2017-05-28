

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
    
    
class Routeur :
    
    """
        - liste_Interfaces : liste des interfaces du routeur : list <Interface>
        - protocole_Ospf : objet correspondant au fonctionnement de OSPF sur ce routeur : <OSPF>
        - protocole_Rip : objet correspondant au fonctionnement de RIP sur ce routeur : <RIP>
    """
    
    def __init__(self, liste_Reseau):
        self.protocole_Ospf = OSPF()
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


class InterfaceReseau :
    
    """
        - adresse : adresse du routeur dans le réseau reseau : String
        - reseau : réseau dans lequel cette interface a les pieds : <Reseau>
    """
    
    def __init__(self, adresse_Du_Routeur, reseau):
        self.adresse = adresse_Du_Routeur
        self.reseau = reseau
    
    
class OSPF :
    
    
    
class CheminOspf :
    
    
    
    
class MessageOspf :
    
    
    

class HelloOspf :
    
    
    
    
class UpdateOspf :
    
    

    
    
class RIP :
    
    


class EltTableRip :
    
    
    

class MessageRip :
    
    
    

