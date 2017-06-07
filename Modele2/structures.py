
from ospf import *
from rip import *


#Mode 0 : active OSPF et RIP
#Mode 1 : active OSPF uniquement
#Mode 2 : active RIP uniquement.
MODE = 0

def switchMode(numero):
    global MODE
    MODE = numero

DEBUG = False                    #Active ou désactive le mode débug.

def afficher(liste_Des_Routeurs):                   #Affiche, suivant le mode activé la table RIP et/ou les chemins Ospf.
    for routeur in liste_Des_Routeurs:
        print()
        print()
        print(routeur.___nom___, ':')
        if MODE == 0 or MODE == 1:
            print("Table OSPF :")
            routeur.protocole_Ospf.afficheCheminsOspf()
        
        if MODE == 0 or MODE == 2:
            print("Table RIP :")
            routeur.protocole_Rip.afficherTableRip()

def estTermine(liste_Des_Routeurs):                 #Affiche si au moment de l'appel, la taille de la table rip comporte autant d'éléments que le nombre de routeurs; idem pour la taille de la liste des chemins ospf.
    nb_Routeurs = len(liste_Des_Routeurs)
    if MODE == 0 or MODE == 1:
        termine = True
        for routeur in liste_Des_Routeurs:
            termine = termine and (nb_Routeurs == len(routeur.protocole_Ospf.liste_Chemin))
        if termine:
            print("Tous les routeurs sont à jour avec OSPF.")
    
    if MODE == 0 or MODE == 2:
        termine = True
        for routeur in liste_Des_Routeurs:
            termine = termine and (len(routeur.protocole_Rip.table) == nb_Routeurs)
        if termine:
            print("Tous les routeurs sont à jour avec RIP")
    
def estTermineBoolOspf(liste_Des_Routeurs):                 #Pareil que la fonction précédente mais renvoie un booléen concernant Ospf.
    nb_Routeurs = len(liste_Des_Routeurs)
    if MODE == 0 or MODE == 1:
        termine = True
        for routeur in liste_Des_Routeurs:
            termine = termine and (nb_Routeurs == len(routeur.protocole_Ospf.liste_Chemin))
        if termine:
            return True
        else:
            return False

def estTermineBoolRip(liste_Des_Routeurs):                  #Pareil que la fonction précédente mais renvoie un booléen concernant Rip.
    nb_Routeurs = len(liste_Des_Routeurs)
    if MODE == 0 or MODE == 2:
        termine = True
        for routeur in liste_Des_Routeurs:
            termine = termine and (nb_Routeurs == len(routeur.protocole_Rip.table))
        if termine:
            return True
        else:
            return False

class Reseau :
    
    
    """
        - adresse : String
        - routeurs_In : liste de routeurs présents dans ce réseau (initialement aucun routeur n'est présent, on les rajoute au fur et à mesure que l'on ajoute des routeurs : list <Routeur>
        - adresse_Dispo : liste de booléen dont l'indice représente la fin de l'adresse ip et la valeur du booléen donne si cette adresse est disponible ou non (True si elle est prise, False si elle est disponible) : list bool
        - bande_Passante : bande passante du réseau en bits/sec : int
    """
    
    def __init__(self, adresse, debit):
        self.adresse = adresse
        self.routeur_In = []                    
        self.adresse_Dispo = [True]                 #L'adresse 0 est celle du routeur (donc indisponible).
        self.bande_Passante = debit
        
        if DEBUG:
            print("Création du réseau d'adresse : ", self.adresse, " et de débit : ", debit)
    
    def __str__(self):
        return "Réseau " + self.adresse
    
    
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
            
            if DEBUG:
                print("On a ajouté un routeur au réseau : ", self.adresse)
            
            return self.getAdresseGenerique()+str(indice_Dispo)
    
    def supprimerRouteur(self, routeur):
        try:
            index = self.routeur_In.index(routeur)
            self.routeur_In.pop(index)
            
            indice_Routeur = routeur.getIndice(self)
            self.adresse_Dispo[indice_Routeur] = False
            
            routeur.supprimerReseau(self)
            
            if DEBUG:
                print("On a bien supprimé un routeur du réseau ", self.adresse)
            
        except ValueError:
            print("Le routeur n'est pas dans le réseau ou le réseau n'est pas dans le routeur ou l'adresse du routeur sur le réseau n'était pas réservée...")
        except IndexError:
            print("L'indice du routeur n'est pas dans la liste des adresses réservées")
    
    def broadcastOspf(self, message_Ospf):                    #Simulation d'un broadcast sur un réseau. message_Ospf est du type <MessageOspf>; envoie un message Ospf.
        """
        if DEBUG:
            print("Début d'un broadcast Ospf")
        """
        
        for routeur in self.routeur_In:
            if not routeur == message_Ospf.expediteur:                  #On ne broadcast pas au routeur qui envoie le message.
                routeur.ajoutMessageOspf(message_Ospf)
    
    def broadcastRip(self, message_Rip):                    #Simultation d'un broadcast sur un réseau.
        """
        if DEBUG:
            print("Début d'un broadcast Rip")
        """
        
        for routeur in self.routeur_In:
            if not routeur == message_Rip.expediteur:                   #On ne broadcast pas au routeur qui envoie le message.
                routeur.ajoutMessageRip(message_Rip)


class Routeur :
    
    """
        - ___nom___ : c'est le nom unique (il doit l'etre lors de la création du routeur) du routeur : string
        - liste_Interfaces : liste des interfaces du routeur : list <Interface>
        - protocole_Ospf : objet correspondant au fonctionnement de OSPF sur ce routeur : <OSPF>
        - protocole_Rip : objet correspondant au fonctionnement de RIP sur ce routeur : <RIP>
    """
    
    def __init__(self, nom, liste_Reseau):                   #liste_Reseau est une liste de <Reseau>.
        
        if DEBUG:
            print("Création de ", nom)
        
        self.___nom___ = nom
        
        if MODE == 0 or MODE == 1:
            self.protocole_Ospf = OSPF(self)
        
        if MODE == 0 or MODE == 2:
            self.protocole_Rip = RIP(self)
        
        self.liste_Interfaces = []
        n=len(liste_Reseau)
        for indice in range(n):
            try:
                adresse_Sur_Reseau = liste_Reseau[indice].enregistrerRouteur(self)
                interface = InterfaceReseau(adresse_Sur_Reseau, liste_Reseau[indice])
                self.liste_Interfaces.append(interface)
                
                if DEBUG:
                    print("Ce routeur a pour adresse ", adresse_Sur_Reseau, " sur le réseau ", liste_Reseau[indice].adresse)
                    
            except BufferError:
                print("Le routeur n'a pas pu etre ajouté au reseau ",  liste_Reseau[indice], " car il est saturé")
    
    def __str__(self):
        string = ""
        for interface in self.liste_Interfaces:
            string = string + interface.adresse + '  '
        return "Routeur : " + self.___nom___ + "; d'adresses ip : " + string
    
    def getIndice(self, reseau):
        adresse_Sur_Reseau = self.getAdresse(reseau)
        index = adresse_Sur_Reseau.rfind('.')
        indice_Routeur = adresse_Sur_Reseau[(index+1):]
        return int(indice_Routeur)
    
    def getAdresse(self, reseau):
        for interface in self.liste_Interfaces:
            if interface.reseau == reseau:
                return interface.adresse
        raise ValueError("Le routeur n'est pas dans le reseau recherché")



    def ajoutMessageOspf(self, message_Ospf):
        """
        if DEBUG:
            print("On ajoute un message Ospf")
        """
        self.protocole_Ospf.recevoirMessageOspf(message_Ospf)
    
    def ajoutMessageRip(self, message_Rip):
        """
        if DEBUG:
            print("On ajoute un message Rip")
        """
        
        self.protocole_Rip.recevoirMessageRip(message_Rip)



    def envoyerLesMessages(self):
        if MODE == 0 or MODE == 1:
            if DEBUG:
                print("On envoie les messages Ospf")
            
            self.protocole_Ospf.envoyerOspf(self.liste_Interfaces)
        
        if MODE == 0 or MODE == 2:
            if DEBUG:
                print("On envoie les messages Rip")
            
            self.protocole_Rip.envoyerRip(self.liste_Interfaces)
    
    
    def traiterLesMessages(self):
        if MODE == 0 or MODE == 1:
            if DEBUG:
                print("Traitement des messages Ospf")
            
            self.protocole_Ospf.traiterOspf()
        
        if MODE == 0 or MODE == 2:
            if DEBUG:
                print("Traitement des messages Rip")
            
            self.protocole_Rip.traiterRip()


    def supprimerReseau(self, reseau):
        indice_Interface = 0
        while indice_Interface < len(self.liste_Interfaces):
            if self.liste_Interfaces[indice_Interface].reseau == reseau:
                self.liste_Interfaces.pop(indice_Interface)
                
                if DEBUG:
                    print("Le réseau a bien été supprimé au niveau du routeur")
                
                break
            indice_Interface += 1
    
    def ajouterReseau(self, reseau):
        adresse_Routeur_New_Reseau = reseau.enregistrerRouteur(self)
        new_Interface = InterfaceReseau(adresse_Routeur_New_Reseau, reseau)
        self.liste_Interfaces.append(new_Interface)
        
        if DEBUG:
            print('Le réseau a bien été ajouté')




class InterfaceReseau :
    
    """
        - adresse : adresse du routeur dans le réseau reseau : String
        - reseau : réseau dans lequel cette interface a les pieds : <Reseau>
    """
    
    def __init__(self, adresse_Du_Routeur, reseau):
        self.adresse = adresse_Du_Routeur
        self.reseau = reseau
