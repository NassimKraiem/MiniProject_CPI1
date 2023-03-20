import random
#from objects import *
import etudiant as e
import interfaceFunctions as interface
from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication


app = QApplication([])
windows = loadUi ("main2.ui")
etudPanWin = loadUi("etudiantPanel.ui")
#w2 = loadUi("main.ui")

etudiants = [e.ajouter(nom=f"user{i}", telephone=f"{random.randint(50, 100)} {random.randint(100, 1000)} {random.randint(100, 1000)}", dateN="13/12/2003")for i in range(50)]
#a1 = e.ajouter(nom="Nessim", prenom="Kraiem")
#etudiants.append(a1)

interface.afficherEtudiants(etudiants, windows)

"""print("1: ", *etudiants)

e.modifier(0, etudiants, nom="Nassim")
print("2: ", *etudiants)

e.supprimer(0, etudiants)
print("3: ", *etudiants)"""

def setWindowBtnsState(win, state):
    win.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, state)
    win.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, state)
    win.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, state)

windows.show()
#w2.show()
#w2.switchBtn.clicked.connect(lambda: (w2.close(), windows.show()))
windows.clearBtn.clicked.connect(lambda: windows.searchBar.setText(""))
windows.searchBar.textChanged.connect(lambda: interface.afficherEtudiants(etudiants, windows, windows.searchBar.text()))
windows.delBtn.clicked.connect(lambda: (e.supprimer(windows.table.currentRow(), etudiants),
                                        windows.table.setCurrentCell(-1, -1),
                                   interface.afficherEtudiants(etudiants, windows, "")))
windows.addBtn.clicked.connect(lambda: (windows.setEnabled(False), etudPanWin.show()))
windows.table.itemSelectionChanged.connect(lambda: windows.table.selectRow(windows.table.currentRow()))
windows.table.doubleClicked.connect(lambda: print(windows.table.model().data(windows.table.model().index(windows.table.currentRow(), 0))))

#etudPanWin.  .triggered.connect(lambda: print("closed"))
etudPanWin.setWindowFlags(etudPanWin.windowFlags() | QtCore.Qt.CustomizeWindowHint)
setWindowBtnsState(etudPanWin, False)
etudPanWin.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
etudPanWin.dateN.setAlignment(QtCore.Qt.AlignRight)
etudPanWin.buttonBox.accepted.connect(lambda: (etudiants.append(e.ajouter(
                                                      etudPanWin.nom.text().lower(),
                                                      etudPanWin.prenom.text().lower(),
                                                      etudPanWin.dateN.text().replace('\u200f', ''),
                                                      etudPanWin.adresse.text(),
                                                      etudPanWin.mail.text(),
                                                      etudPanWin.telephone.text(),
                                                      etudPanWin.section.currentText(),
                                                      etudPanWin.niveau.currentText())
                                                 ),
                                                interface.afficherEtudiants(etudiants, windows),
                                                etudPanWin.close(),
                                                windows.setEnabled(True)
                                            )
                                      )
etudPanWin.buttonBox.rejected.connect(lambda: (etudPanWin.close(), windows.setEnabled(True)))

app.exec_()

#n=windows.l.text()
#windows.r.setText(msg)