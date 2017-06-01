

cent_G_Bits_Sec = 100000000000
dix_G_Bits_Sec = 10000000000
un_G_Bits_Sec = 1000000000

cent_M_Bits_Sec = 100000000
dix_M_Bits_Sec = 10000000
un_M_Bits_Sec = 1000000

cent_K_Bits_Sec = 100000
dix_K_Bits_Sec = 10000
un_K_Bits_Sec = 1000


def listeNomRouteur(nombre):
    liste_Nom_Routeur = []
    rout_String = 'routeur'
    
    for i in range(nombre):
        liste_Nom_Routeur.append(rout_String+str(i))
    
    return liste_Nom_Routeur
