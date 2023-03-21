from objects import *
from helper import *

def ajouter(ref, titre="", npAuteur="", anneeEdition="", nombreExemplaires="", categorie="", couverture=""):
    return Livre(ref, titre, npAuteur, anneeEdition, nombreExemplaires, categorie, couverture)

#def supprimer(etud, lo):
#    lo.remove(etud)

# def supprimer(indEtud, etudiants, windows):
#     if(indEtud in range(0, len(etudiants))):
#         id = windows.table.verticalHeaderItem(indEtud).text()
#         etudiants.remove(ajouter(id)) #creer une instance avec le meme nce comme reference de comparaison
#                                       #puisque le nce seulement est comparé dans "__eq__"
#     else:
#         raise Exception("L'indice de l'etudiant n'existe pas!")
    
def modifier(indLivre, livres, ref="", titre="", npAuteur="", anneeEdition="", nombreExemplaires="", categorie="", couverture=""):
    if not empty(ref): livres[indLivre].ref = ref
    if not empty(titre): livres[indLivre].titre = titre
    if not empty(npAuteur): livres[indLivre].npAuteur = npAuteur
    if not empty(anneeEdition): livres[indLivre].anneeEdition = anneeEdition
    if not empty(nombreExemplaires): livres[indLivre].nombreExemplaires = nombreExemplaires
    if not empty(categorie): livres[indLivre].categorie = categorie
    if not empty(couverture): livres[indLivre].couverture = couverture