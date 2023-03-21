from objects import *
from helper import *

def ajouter(ref, titre="", npAuteur="", anneeEdition="", nombreExemplaires="", categorie="", couverture=""):
    return Livre(ref, titre, npAuteur, anneeEdition, nombreExemplaires, categorie, couverture)
    
def modifier(indLivre, livres, ref="", titre="", npAuteur="", anneeEdition="", nombreExemplaires="", categorie="", couverture=""):
    if not empty(ref): livres[indLivre].ref = ref
    if not empty(titre): livres[indLivre].titre = titre
    if not empty(npAuteur): livres[indLivre].npAuteur = npAuteur
    if not empty(anneeEdition): livres[indLivre].anneeEdition = anneeEdition
    if not empty(nombreExemplaires): livres[indLivre].nombreExemplaires = nombreExemplaires
    if not empty(categorie): livres[indLivre].categorie = categorie
    if not empty(couverture): livres[indLivre].couverture = couverture