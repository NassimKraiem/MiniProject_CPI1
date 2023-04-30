from objects import *
from helper import *

def ajouter(nce, reference, dateEmprunt="", dateRetour="", nombreExemplaires=""):
    return Emprunt(nce, reference, dateEmprunt, dateRetour, nombreExemplaires)

def supprimer(emprunts, windows, livres):
    for indEmp in sorted(set([i.row() for i in windows.table_3.selectedIndexes()]), reverse=True):
        if(indEmp in range(0, len(emprunts))):
            nce = windows.table_3.model().data(windows.table_3.model().index(indEmp, 0))
            reference = windows.table_3.model().data(windows.table_3.model().index(indEmp, 1))
            nbExemp = windows.table_3.model().data(windows.table_3.model().index(indEmp, 4))

            borrowedBook = list(filter(lambda x: x.reference == reference, livres))[0]
            borrowedBook.nombreExemplaires = str(int(borrowedBook.nombreExemplaires) + int(nbExemp))

            emprunts.remove(ajouter(nce, reference)) #creer une instance avec le meme nce comme reference de comparaison
                                        #puisque le nce seulement est comparé dans "__eq__"
        else:
            raise Exception("L'indice de l'etudiant n'existe pas!")