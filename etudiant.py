from objects import *
from helper import *

def ajouter(nom, prenom="", dateN="", adresse="", mail="", telephone="", section="", niveau=""):
    return Etudiant(nom, prenom, dateN, adresse, mail, telephone, section, niveau)

#def supprimer(etud, lo):
#    lo.remove(etud)

def supprimer(indEtud, etudiants):
    if(indEtud in range(0, len(etudiants))):
        etudiants.pop(indEtud)
    else:
        raise Exception("L'indice de l'etudiant n'existe pas!")
    
def modifier(indEtud, etudiants, nom ="", prenom ="", dateN ="", adresse ="", mail ="", telephone ="", section ="", niveau =""):
    if not empty(nom): etudiants[indEtud].nom = nom
    if not empty(prenom): etudiants[indEtud].prenom = prenom
    if not empty(dateN): etudiants[indEtud].dateN = dateN
    if not empty(adresse): etudiants[indEtud].adresse = adresse
    if not empty(mail): etudiants[indEtud].mail = mail
    if not empty(telephone): etudiants[indEtud].telephone = telephone
    if not empty(section): etudiants[indEtud].section = section
    if not empty(niveau): etudiants[indEtud].niveau = niveau