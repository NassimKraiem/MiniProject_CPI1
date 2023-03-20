from helper import *

class Etudiant:
    #ajouter nce aussi
    def __init__(self, nce, nom, prenom="", dateN="", adresse="", mail="", telephone="", section="", niveau=""):
        self.nce = nce
        self.nom = nom
        self.prenom = prenom
        self.dateN = dateN
        self.adresse = adresse
        self.mail = mail
        self.telephone = telephone
        self.section = section
        self.niveau = niveau
        self.locals = list(locals().values())[1:]
    def __str__(self):
        return f"{self.nce}, {self.nom}{' 'if not empty(self.prenom) else ''}{self.prenom}{', 'if not empty(self.section) else ''}{self.section}{self.niveau}{',né le 'if not empty(self.dateN) else ''}{self.dateN}{', habite à 'if not empty(self.dateN) else ''}{self.adresse}"
    def __eq__(self, other): 
        if not isinstance(other, Etudiant):
            return NotImplemented # don't attempt to compare against unrelated types
        return (self.nce == other.nce)
    def __ne__(self, other):
        return not self.__eq__(other)

class Livre:
    def __init__(self, reference, titre, npAuteur, anneeEdition, nombreExemplaires):
        self.reference = reference
        self.titre = titre
        self.npAuteur = npAuteur
        self.anneeEdition = anneeEdition
        self.nombreExemplaires = nombreExemplaires
    def __eq__(self, other): 
        if not isinstance(other, Livre):
            return NotImplemented
        return (self.reference == other.reference)
    def __ne__(self, other):
        return not self.__eq__(other)

class Emprunt:
    def __init__(self, nce, reference, dateEmprunt, dateRetour, nombreExemplaires):
        self.nce = nce
        self.reference = reference
        self.dateEmprunt = dateEmprunt
        self.dateRetour = dateRetour
        self.nombreExemplaires = nombreExemplaires
    def __eq__(self, other): 
        if not isinstance(other, Etudiant):
            return NotImplemented
        return (
            self.nce == other.nce and
            self.reference == other.reference and
            self.dateEmprunt == other.dateEmprunt and
            self.dateRetour == other.dateRetour and
            self.nombreExemplaires == other.nombreExemplaires
        )
    def __ne__(self, other):
        return not self.__eq__(other)