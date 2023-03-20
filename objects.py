from helper import *

class Etudiant:
    def __init__(self, nom, prenom, dateN="", adresse="", mail="", telephone="", section="", niveau=""):
        self.nom = nom
        self.prenom = prenom
        self.dateN = dateN
        self.adresse = adresse
        self.mail = mail
        self.telephone = telephone
        self.section = section
        self.niveau = niveau
    def __str__(self):
        return f"{self.nom} {self.prenom}{', 'if not empty(self.section) else ''}{self.section}{self.niveau}{',né le 'if not empty(self.dateN) else ''}{self.dateN}{', habite à 'if not empty(self.dateN) else ''}{self.adresse}"

class Livre:
    def __init__(self, reference, titre, npAuteur, anneeEdition, nombreExemplaires):
        self.reference = reference
        self.titre = titre
        self.npAuteur = npAuteur
        self.anneeEdition = anneeEdition
        self.nombreExemplaires = nombreExemplaires
