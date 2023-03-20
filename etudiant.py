from objects import *
from helper import *

def ajouter(nce, nom="", prenom="", dateN="", adresse="", mail="", telephone="", section="", niveau=""):
    return Etudiant(nce, nom, prenom, dateN, adresse, mail, telephone, section, niveau)

#def supprimer(etud, lo):
#    lo.remove(etud)

def supprimer(indEtud, etudiants, windows):
    if(indEtud in range(0, len(etudiants))):
        id = windows.table.verticalHeaderItem(indEtud).text()
        etudiants.remove(ajouter(id)) #creer une instance avec le meme nce comme reference de comparaison
                                      #puisque le nce seulement est comparé dans "__eq__"
    else:
        raise Exception("L'indice de l'etudiant n'existe pas!")
    
def modifier(indEtud, etudiants, nce="", nom ="", prenom ="", dateN ="", adresse ="", mail ="", telephone ="", section ="", niveau =""):
    if not empty(nce): etudiants[indEtud].nce = nce
    if not empty(nom): etudiants[indEtud].nom = nom
    if not empty(prenom): etudiants[indEtud].prenom = prenom
    if not empty(dateN): etudiants[indEtud].dateN = dateN
    if not empty(adresse): etudiants[indEtud].adresse = adresse
    if not empty(mail): etudiants[indEtud].mail = mail
    if not empty(telephone): etudiants[indEtud].telephone = telephone
    if not empty(section): etudiants[indEtud].section = section
    if not empty(niveau): etudiants[indEtud].niveau = niveau