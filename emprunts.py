from objects import *
from helper import *
from datetime import date
from PyQt5.QtWidgets import QMessageBox

def ajouter(nce, reference, dateEmprunt="", dateRetour="", nombreExemplaires=""):
    return Emprunt(nce, reference, dateEmprunt, dateRetour, nombreExemplaires)

def supprimer(emprunts, windows, livres):
    for indEmp in sorted(set([i.row() for i in windows.table_3.selectedIndexes()]), reverse=True):
        if(indEmp in range(0, len(emprunts))):
            nce = windows.table_3.model().data(windows.table_3.model().index(indEmp, 0))
            reference = windows.table_3.model().data(windows.table_3.model().index(indEmp, 1))
            #nbExemp = windows.table_3.model().data(windows.table_3.model().index(indEmp, 4))

            #borrowedBook = list(filter(lambda x: x.reference == reference, livres))[0]
            #borrowedBook.nombreExemplaires = str(int(borrowedBook.nombreExemplaires) + int(nbExemp))

            emprunts.remove(ajouter(nce, reference)) #creer une instance avec le meme nce comme reference de comparaison
                                        #puisque le nce seulement est comparé dans "__eq__"
        else:
            raise Exception("L'indice de l'etudiant n'existe pas!")

def retourner(emprunts, windows, livres):
    for indEmp in sorted(set([i.row() for i in windows.table_3.selectedIndexes()]), reverse=True):
        if(indEmp in range(0, len(emprunts))):
            nce = windows.table_3.model().data(windows.table_3.model().index(indEmp, 0))
            reference = windows.table_3.model().data(windows.table_3.model().index(indEmp, 1))
            nbExemp = windows.table_3.model().data(windows.table_3.model().index(indEmp, 4))

            if(emprunts[emprunts.index(ajouter(nce, reference))].dateRetour != "--/--/--"):
                alert(msg="Emprunt deja retournee!")
                return

            borrowedBook = list(filter(lambda x: x.reference == reference, livres))[0]
            borrowedBook.nombreExemplaires = str(int(borrowedBook.nombreExemplaires) + int(nbExemp))

            current_dateRetour = date.today()
            formatted_dateRetour = current_dateRetour.strftime("%d/%m/%Y")
            emprunts[emprunts.index(ajouter(nce, reference))].dateRetour = formatted_dateRetour
            #emprunts.remove(ajouter(nce, reference)) #creer une instance avec le meme nce comme reference de comparaison
                                        #puisque le nce seulement est comparé dans "__eq__"
        else:
            raise Exception("L'indice de l'etudiant n'existe pas!")


def alert(msg="Warning", title="Warning MessageBox"):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setText(msg)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec_()