from curses import window
import aside
from connects import openAddWindow
import dbManager
import etudiant as e
import livre as l
import interfaceFunctions as interface
from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QFileDialog
from connects import *

groupLivreBy = "Categorie"

app = QApplication([])
windows = loadUi("ui/main.ui")
etudPanWin = loadUi("ui/etudiantPanel.ui")
# etudPanWin.setWindowFlags(QtCore.Qt.Window)
# etudPanWin.setAttribute(QtCore.Qt.WA_DeleteOnClose)
livrePanWin = loadUi("ui/livrePanel.ui")
# livrePanWin.setWindowFlags(QtCore.Qt.Window)
# livrePanWin.setAttribute(QtCore.Qt.WA_DeleteOnClose)


etudiants = dbManager.charger("etudiants")
interface.afficherEtudiants(etudiants, windows)

# livres = dbManager.chargerLivre("livres")
# interface.afficherLivres(livres, windows, edit, groupLivreBy)
livres = []

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
        interface.afficherLivres(livres, windows, edit, groupLivreBy)

    def clicker():
        livrePanWin.hide()
        fname = QFileDialog.getOpenFileName(windows, "Select book Cover", "", "Image Files (*.png, *jpg)")
        if(fname):
            livrePanWin.coverUrl.setText(fname[0])
            livrePanWin.coverImg.setStyleSheet(f"border-image : url({fname[0]}) 0 0 0 0 stretch stretch;")
            livrePanWin.show()
    
    def edit(livre):
        livrePanWin.ref.setValue(int(livre.reference[1:]))
        livrePanWin.ref.setDisabled(True)
        livrePanWin.titre.setText(livre.titre)
        livrePanWin.nomAut.setText(livre.npAuteur)
        livrePanWin.anneeEdition.setValue(int(livre.anneeEdition))
        livrePanWin.nbExemp.setValue(int(livre.nombreExemplaires))
        index = livrePanWin.categorie.findText(livre.categorie, QtCore.Qt.MatchFixedString)
        livrePanWin.categorie.setCurrentIndex(index)
        livrePanWin.coverUrl.setText(livre.couverture)
        livrePanWin.coverImg.setStyleSheet(f"border-image : url({livre.couverture}) 0 0 0 0 stretch stretch;")
        livrePanWin.show()

    def resetLivrePan():
        livrePanWin.ref.setValue(0)
        livrePanWin.ref.setDisabled(False)
        livrePanWin.titre.setText('')
        livrePanWin.nomAut.setText('')
        livrePanWin.anneeEdition.setValue(2000)
        livrePanWin.nbExemp.setValue(1)
        livrePanWin.categorie.setCurrentIndex(-1)
        livrePanWin.coverUrl.setText('')
        livrePanWin.coverImg.setStyleSheet('')
    
    def handleGroupLivreByChanged():
        global groupLivreBy
        groupLivreBy = windows.groupLivreByComboBox.currentText()
        interface.afficherLivres(livres, windows, edit, groupLivreBy)

    def handleAddEditLivre():
        if(not livrePanWin.ref.isEnabled()):
            livres.pop(livres.index(l.ajouter(livrePanWin.ref.text())))
        livres.append(
            l.ajouter(
                livrePanWin.ref.text(),
                livrePanWin.titre.text().lower(),
                livrePanWin.nomAut.text().lower(),
                livrePanWin.anneeEdition.text().replace('\u200f', ''),
                livrePanWin.nbExemp.text(),
                livrePanWin.categorie.currentText(),
                livrePanWin.coverUrl.text()
            )
        )
        interface.afficherLivres(livres, windows, edit, groupLivreBy)
        livrePanWin.close()
        windows.setEnabled(True)

    livrePanWin.setWindowFlags(livrePanWin.windowFlags() | QtCore.Qt.CustomizeWindowHint)
    setWindowBtnsState(livrePanWin, False)
    livrePanWin.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
    livrePanWin.buttonBox.accepted.connect(handleAddEditLivre)
    livrePanWin.buttonBox.rejected.connect(lambda: (livrePanWin.close(), windows.setEnabled(True)))
    livrePanWin.selectCoverBtn.clicked.connect(clicker)
    windows.groupLivreByComboBox.currentIndexChanged.connect(handleGroupLivreByChanged)
    
    windows.ajouterLivreBtn.clicked.connect(lambda: (resetLivrePan(), openAddWindow(windows, livrePanWin)))

    
    windows.loadLivresBtn.clicked.connect(charger)
    windows.saveLivresBtn.clicked.connect(lambda: dbManager.enregistrer(livres, "livres"))
    charger()


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
    windows.delBtn.clicked.connect(lambda: (e.supprimer(etudiants, windows),
                                            windows.table.setCurrentCell(-1, -1),
                                            interface.afficherEtudiants(etudiants, windows, ""),
                                            windows.searchBar.setText("")
                                            ))
    windows.addBtn.clicked.connect(lambda: openAddWindow(windows, etudPanWin))
    windows.table.setSelectionMode(QtWidgets.QTableWidget.ContiguousSelection)
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
                                                ) if(not dbManager.existe(etudPanWin.nce.text(), etudiants)) else interface.alert("Etudiant existant!")
                                            )
    etudPanWin.buttonBox.rejected.connect(lambda: (etudPanWin.close(), windows.setEnabled(True)))




def connectNavBar(windows):
    def customDel(delFunction, critere: list):
        global etudiants
        if(critere == []):
            interface.alert(msg="Il n'y a plus d'étudiants")
            return
        windows.top_aside.children()[3].click()
        etudiants = delFunction(interface.askForItem(items=list(set(critere))), etudiants)
        windows.table.setCurrentCell(-1, -1)
        interface.afficherEtudiants(etudiants, windows, "")
        windows.searchBar.setText("")
    windows.action_Ajouter_tudiant_2.triggered.connect(lambda: (windows.top_aside.children()[3].click(), openAddWindow(windows, etudPanWin)))
    windows.action_Suppression_tudiant_donn.triggered.connect(lambda: interface.alert(msg="Il n'y a plus d'étudiants") if etudiants == [] else (
                                                    windows.top_aside.children()[3].click(),
                                                    e.supprimerParNce(interface.askForItem(items=[etud.nce for etud in etudiants]), etudiants),
                                                    windows.table.setCurrentCell(-1, -1),
                                                    interface.afficherEtudiants(etudiants, windows, ""),
                                                    windows.searchBar.setText("")
                                                    ))
    windows.action_Suppression_des_tudiants_d_une_section_donn_e.triggered.connect(lambda: customDel(e.supprimerParSection, [etud.section for etud in etudiants]))
    windows.action_Suppression_des_tudiants_d_un_niveau_donn_e.triggered.connect(lambda: customDel(e.supprimerParNiveau, [etud.niveau for etud in etudiants]))

aside.connectBtns(windows)
loadTabLivres(windows)
loadTabEtudiants(windows)


connectNavBar(windows)
windows.show()
interface.test(etudiants)
app.exec_()