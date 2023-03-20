import aside
import dbManager
import etudiant as e
import interfaceFunctions as interface
from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication

app = QApplication([])
windows = loadUi("main.ui")

etudiants = dbManager.charger()
interface.afficherEtudiants(etudiants, windows)

def load(windows):
    global etudiants
    etudPanWin = loadUi("etudiantPanel.ui")

    def setWindowBtnsState(win, state):
        win.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, state)
        win.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, state)
        win.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, state)

    def charger():
        global etudiants
        etudiants = dbManager.charger()
        interface.afficherEtudiants(etudiants, windows)

    windows.clearBtn.clicked.connect(lambda: windows.searchBar.setText(""))
    windows.searchBar.textChanged.connect(lambda: interface.afficherEtudiants(etudiants, windows, windows.searchBar.text()))
    windows.delBtn.clicked.connect(lambda: (e.supprimer(windows.table.currentRow(), etudiants, windows),
                                            windows.table.setCurrentCell(-1, -1),
                                            interface.afficherEtudiants(etudiants, windows, ""),
                                            windows.searchBar.setText("")
                                            ))
    windows.addBtn.clicked.connect(lambda: (windows.setEnabled(False), etudPanWin.show()))
    windows.table.itemSelectionChanged.connect(lambda: windows.table.selectRow(windows.table.currentRow()))
    windows.table.doubleClicked.connect(lambda: print(windows.table.model().data(windows.table.model().index(windows.table.currentRow(), 0))))
    windows.loadBtn.clicked.connect(charger)
    windows.saveBtn.clicked.connect(lambda: dbManager.enregistrer(etudiants))

    #etudPanWin.  .triggered.connect(lambda: print("closed"))
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

aside.connectBtns(windows)
load(windows)
windows.show()
app.exec_()