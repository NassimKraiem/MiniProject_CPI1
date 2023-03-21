import aside
from connects import openAddWindow
import dbManager
import etudiant as e
import livre as l
import interfaceFunctions as interface
from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication
from connects import *

app = QApplication([])
windows = loadUi("ui/main.ui")
etudPanWin = loadUi("ui/etudiantPanel.ui")
livrePanWin = loadUi("ui/livrePanel.ui")

etudiants = dbManager.charger("etudiants")
interface.afficherEtudiants(etudiants, windows)

livres = dbManager.chargerLivre("livres")
interface.afficherLivres(livres, windows)

def loadTabLivres(windows):
    global etudiants
    global livrePanWin

    def setWindowBtnsState(win, state):
        win.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, state)
        win.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, state)
        win.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, state)

    def charger():
        global livres
        livres = dbManager.chargerLivre("livres")
        interface.afficherLivres(livres, windows)
    
    windows.ajouterLivreBtn.clicked.connect(lambda: openAddWindow(windows, livrePanWin))

    livrePanWin.setWindowFlags(livrePanWin.windowFlags() | QtCore.Qt.CustomizeWindowHint)
    setWindowBtnsState(livrePanWin, False)
    livrePanWin.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
    livrePanWin.buttonBox.accepted.connect(lambda: (livres.append(
                                                    l.ajouter(
                                                        livrePanWin.ref.text(),
                                                        livrePanWin.titre.text().lower(),
                                                        livrePanWin.nomAut.text().lower(),
                                                        livrePanWin.anneeEdition.text().replace('\u200f', ''),
                                                        livrePanWin.nbExemp.text(),
                                                        livrePanWin.categorie.currentText(),
                                                        livrePanWin.coverUrl.text())
                                                    ),
                                                    interface.afficherLivres(livres, windows),
                                                    livrePanWin.close(),
                                                    windows.setEnabled(True)
                                                )
                                            )
    livrePanWin.buttonBox.rejected.connect(lambda: (livrePanWin.close(), windows.setEnabled(True)))


def loadTabEtudiants(windows):
    global etudiants
    global etudPanWin

    def setWindowBtnsState(win, state):
        win.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, state)
        win.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, state)
        win.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, state)

    def charger():
        global etudiants
        etudiants = dbManager.charger("etudiants")
        interface.afficherEtudiants(etudiants, windows)

    windows.clearBtn.clicked.connect(lambda: windows.searchBar.setText(""))
    windows.searchBar.textChanged.connect(lambda: interface.afficherEtudiants(etudiants, windows, windows.searchBar.text()))
    windows.delBtn.clicked.connect(lambda: (e.supprimer(windows.table.currentRow(), etudiants, windows),
                                            windows.table.setCurrentCell(-1, -1),
                                            interface.afficherEtudiants(etudiants, windows, ""),
                                            windows.searchBar.setText("")
                                            ))
    windows.addBtn.clicked.connect(lambda: openAddWindow(windows, etudPanWin))
    windows.table.itemSelectionChanged.connect(lambda: selectCurrentRow(windows))
    windows.table.doubleClicked.connect(lambda: openEditWindow(windows, etudPanWin))
    windows.loadBtn.clicked.connect(charger)
    windows.saveBtn.clicked.connect(lambda: dbManager.enregistrer(etudiants, "etudiants"))

    etudPanWin.setWindowFlags(etudPanWin.windowFlags() | QtCore.Qt.CustomizeWindowHint)
    setWindowBtnsState(etudPanWin, False)
    etudPanWin.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
    etudPanWin.dateN.setAlignment(QtCore.Qt.AlignRight)
    etudPanWin.buttonBox.accepted.connect(lambda: (etudiants.append(
                                                    e.ajouter(
                                                        etudPanWin.nce.text(),
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




def connectNavBar(windows):
    windows.action_Ajouter_tudiant_2.triggered.connect(lambda: openAddWindow(windows, etudPanWin))

aside.connectBtns(windows)
loadTabLivres(windows)
loadTabEtudiants(windows)

connectNavBar(windows)
windows.show()
app.exec_()