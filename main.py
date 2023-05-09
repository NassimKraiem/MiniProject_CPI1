from datetime import date, timedelta
import os
#from connects import openAddWindow
import aside
import dbManager
import etudiant as e
import emprunts as emp
import livre as l
import interfaceFunctions as interface
from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QFileDialog, QPushButton
from connects import *
from helper import *
from objects import Emprunt, Etudiant, Livre
import shared_data

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

groupLivreBy = "Categorie"

app = QApplication([])
windows = loadUi("ui/main.ui")
etudPanWin = loadUi("ui/etudiantPanel.ui")
# etudPanWin.setWindowFlags(QtCore.Qt.Window)
# etudPanWin.setAttribute(QtCore.Qt.WA_DeleteOnClose)
livrePanWin = loadUi("ui/livrePanel.ui")
# livrePanWin.setWindowFlags(QtCore.Qt.Window)
# livrePanWin.setAttribute(QtCore.Qt.WA_DeleteOnClose)
empPanWin = loadUi("ui/empruntPanel.ui")

tableWindow = loadUi("ui/showTable.ui")

shared_data.etudiants = dbManager.charger("etudiants")
interface.afficherEtudiants(shared_data.etudiants, windows)

shared_data.emprunts = dbManager.chargerEmp("emprunts")
interface.afficherEmprunts(shared_data.emprunts, windows)

# shared_data.livres = dbManager.chargerLivre("livres")
# interface.afficherLivres(livres, windows, edit, groupLivreBy, query=windows.searchBar_2.text(), critere=windows.critereRechLivre.currentText())

def loadTabLivres(windows):
    global livrePanWin
    global groupLivreBy
    def charger():
        shared_data.livres = dbManager.chargerLivre("livres")
        interface.afficherLivres(shared_data.livres, windows, edit, groupLivreBy, query=windows.searchBar_2.text(), critere=windows.critereRechLivre.currentText())

    def clicker():
        livrePanWin.hide()
        fname = QFileDialog.getOpenFileName(windows, "Select book Cover", "", "Image Files (*.png, *jpg)")
        if(fname):
            link = fname[0].replace(BASE_DIR, ".")
            livrePanWin.coverUrl.setText(link)
            livrePanWin.coverImg.setStyleSheet(f"border-image : url({link}) 0 0 0 0 stretch stretch;")
            livrePanWin.show()
    
    def edit(livre: Livre):
        livrePanWin.ref.setValue(int(livre.reference[1:]))
        livrePanWin.ref.setDisabled(True)
        livrePanWin.titre.setText(livre.titre.title())
        livrePanWin.titre.setDisabled(True)
        livrePanWin.nomAut.setText(livre.npAuteur.title())
        livrePanWin.nomAut.setDisabled(True)
        livrePanWin.anneeEdition.setValue(int(livre.anneeEdition))
        livrePanWin.anneeEdition.setDisabled(True)
        livrePanWin.nbExemp.setValue(int(livre.nombreExemplaires))
        index = livrePanWin.categorie.findText(livre.categorie, QtCore.Qt.MatchFixedString)
        livrePanWin.categorie.setCurrentIndex(index)
        livrePanWin.categorie.setDisabled(True)
        livrePanWin.coverUrl.setText(livre.couverture)
        livrePanWin.coverImg.setStyleSheet(f"border-image : url({livre.couverture}) 0 0 0 0 stretch stretch;")
        livrePanWin.show()

    shared_data.editLivreFunc = edit

    def resetLivrePan():
        livrePanWin.ref.setValue(0)
        livrePanWin.ref.setDisabled(False)
        livrePanWin.titre.setText('')
        livrePanWin.titre.setDisabled(False)
        livrePanWin.nomAut.setText('')
        livrePanWin.nomAut.setDisabled(False)
        livrePanWin.anneeEdition.setValue(2000)
        livrePanWin.anneeEdition.setDisabled(False)
        livrePanWin.nbExemp.setValue(1)
        livrePanWin.categorie.setCurrentIndex(-1)
        livrePanWin.categorie.setDisabled(False)
        livrePanWin.coverUrl.setText('')
        livrePanWin.coverImg.setStyleSheet('')
    
    def handleGroupLivreByChanged():
        global groupLivreBy
        groupLivreBy = windows.groupLivreByComboBox.currentText()
        interface.afficherLivres(shared_data.livres, windows, edit, groupLivreBy, query=windows.searchBar_2.text(), critere=windows.critereRechLivre.currentText())

    def handleAddEditLivre():
        if(livrePanWin.ref.isEnabled() and dbManager.existe(livrePanWin.ref.text(), shared_data.livres, l)):
            interface.alert("Livre existant!")
        elif(empty(livrePanWin.ref.text())):
            interface.alert("Remplir Ref!")
        elif(empty(livrePanWin.titre.text().strip())):
            interface.alert("Remplir le titre du livre!")
        elif(not "".join(livrePanWin.titre.text().strip().split()).isalpha()):
            interface.alert("Le titre ne doit contenir que des lettres!")
        elif(empty(livrePanWin.nomAut.text().strip())):
            interface.alert("Remplir le nom de l'auteur!")
        elif(not "".join(livrePanWin.nomAut.text().strip().split(maxsplit=2)).isalpha()):
            interface.alert("Le nom de l'auteur ne doit contenir que des lettres!")
        # elif(empty(livrePanWin.anneeEdition.text().replace('\u200f', ''))):
        #     interface.alert("Selectionner la date de naissance de l'etudiant!")
        elif(empty(livrePanWin.nbExemp.text())):
            interface.alert("Remplir le nombre d'exemplaires!")
        # elif(int(livrePanWin.nbExemp.text()) < 1):
        #     interface.alert("Le nombre d'exemplaires doit etre > 1!")
        elif(empty(livrePanWin.categorie.currentText())):
            interface.alert("Selectionner la categorie du livre!")
        elif(empty(livrePanWin.coverUrl.text())):
            interface.alert("Selectionner une image de couverture pour le livre!")
        else:
            if(not livrePanWin.ref.isEnabled()):
                shared_data.livres.pop(shared_data.livres.index(l.ajouter(livrePanWin.ref.text())))
            shared_data.livres.append(
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
            interface.afficherLivres(shared_data.livres, windows, edit, groupLivreBy, query=windows.searchBar_2.text(), critere=windows.critereRechLivre.currentText())
            livrePanWin.close()
            windows.setEnabled(True)

    def handleDeleteSelectedBooks():
        layout = windows.scrollAreaContent.layout()
        for i in range(layout.count()-1):
            items = layout.itemAt(i).widget().layout().itemAt(1).widget().widget().layout()
            for j in range(items.count()-1):
                ref = items.itemAt(j).widget().layout().itemAt(0).widget().objectName()
                widget = items.itemAt(j).widget().layout().itemAt(1).widget()
                if isinstance(widget, QtWidgets.QLabel):
                    #print("Label:", widget.text())
                    if(widget.property("selected")):
                        if(len(list(filter(lambda x: x.reference == ref, shared_data.emprunts))) > 0):
                            interface.alert(f"Impossible de supprimer le livre \"{shared_data.livres[shared_data.livres.index(l.ajouter(ref))].titre}\"! (emprunté)")
                        else:
                            shared_data.livres.pop(shared_data.livres.index(l.ajouter(ref)))
        interface.afficherLivres(shared_data.livres, windows, edit, groupLivreBy, query=windows.searchBar_2.text(), critere=windows.critereRechLivre.currentText())

    livrePanWin.setWindowFlags(livrePanWin.windowFlags() | QtCore.Qt.CustomizeWindowHint)
    interface.setWindowBtnsState(livrePanWin, False)
    #livrePanWin.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
    livrePanWin.buttonBox.accepted.connect(handleAddEditLivre)
    livrePanWin.buttonBox.rejected.connect(lambda: (livrePanWin.close(), windows.setEnabled(True)))
    livrePanWin.selectCoverBtn.clicked.connect(clicker)
    windows.groupLivreByComboBox.currentIndexChanged.connect(handleGroupLivreByChanged)
    windows.searchBar_2.textChanged.connect(lambda: interface.afficherLivres(shared_data.livres, windows, edit, groupLivreBy, query=windows.searchBar_2.text(), critere=windows.critereRechLivre.currentText()))
    windows.critereRechLivre.currentIndexChanged.connect(lambda: interface.afficherLivres(shared_data.livres, windows, edit, query=windows.searchBar_2.text(), critere=windows.critereRechLivre.currentText()))
    
    windows.ajouterLivreBtn.clicked.connect(lambda: (resetLivrePan(), openAddWindow(windows, livrePanWin)))
    windows.suppLivreBtn.clicked.connect(handleDeleteSelectedBooks)

    windows.tabWidget.currentChanged.connect(lambda index: (print(index), interface.afficherLivres(shared_data.livres, windows, edit, groupLivreBy, query=windows.searchBar_2.text(), critere=windows.critereRechLivre.currentText()) if index == 0 else None))
    
    windows.loadLivresBtn.clicked.connect(charger)
    windows.saveLivresBtn.clicked.connect(lambda: dbManager.enregistrer(shared_data.livres, "livres"))
    charger()


def loadTabEtudiants(windows):
    global etudPanWin

    niv = {
        "": [],
        "CPI": ["1ere", "2eme"],
        "INFO": ["1ere", "2eme", "3eme"],
        "EEA": ["1ere", "2eme", "3eme"],
        "TIC": ["1ere", "2eme", "3eme"],
        "Cycle Ingenieur": ["1ere", "2eme", "3eme"],
    }

    def charger():
        shared_data.etudiants = dbManager.charger("etudiants")
        interface.afficherEtudiants(shared_data.etudiants, windows)
    
    def handleAjouterModifierEtudiant():
        if(dbManager.existe(etudPanWin.nce.text(), shared_data.etudiants, e)):
            interface.alert("Etudiant existant!")
        elif(empty(etudPanWin.nce.text())):
            interface.alert("Remplir NCE!")
        elif(empty(etudPanWin.nom.text().strip())):
            interface.alert("Remplir le nom de l'etudiant!")
        elif(not "".join(etudPanWin.nom.text().strip().split(maxsplit=2)).isalpha()):
            interface.alert("Le nom ne doit contenir que des lettres!")
        elif(empty(etudPanWin.prenom.text().strip())):
            interface.alert("Remplir le prenom de l'etudiant!")
        elif(not "".join(etudPanWin.prenom.text().strip().split(maxsplit=2)).isalpha()):
            interface.alert("Le prenom ne doit contenir que des lettres!")
        # elif(empty(etudPanWin.dateN.text().replace('\u200f', ''))):
        #     interface.alert("Selectionner la date de naissance de l'etudiant!")
        elif(empty(etudPanWin.adresse.text())):
            interface.alert("Remplir l'adresse de l'etudiant!")
        elif(not "".join(etudPanWin.adresse.text().split()).isalnum()):
            interface.alert("L'adresse ne doit contenir que des chiffres, des lettres et des espaces!")
        elif(empty(etudPanWin.mail.text())):
            interface.alert("Remplir l'email de l'etudiant!")
        elif(not (etudPanWin.mail.text().isalnum())):
            interface.alert("email is not alnum! <--")
        # elif(empty(etudPanWin.telephone.text())):
        #     interface.alert("Remplir le numero de tel de l'etudiant!")
        elif(empty(etudPanWin.section.currentText())):
            interface.alert("Selectionner la section de l'etudiant!")
        elif(empty(etudPanWin.niveau.currentText())):
            interface.alert("Selectionner le niveau de l'etudiant!")
        else:
            if(not etudPanWin.nce.isEnabled()):
                shared_data.etudiants.pop(shared_data.etudiants.index(e.ajouter(etudPanWin.nce.text())))
            shared_data.etudiants.append(
                e.ajouter(
                    etudPanWin.nce.text().strip(),
                    etudPanWin.nom.text().lower().strip(),
                    etudPanWin.prenom.text().lower().strip(),
                    etudPanWin.dateN.text().replace('\u200f', ''),
                    etudPanWin.adresse.text().strip(),
                    etudPanWin.mail.text().strip(),
                    etudPanWin.telephone.text(),
                    etudPanWin.section.currentText(),
                    etudPanWin.niveau.currentText())
                )
            interface.afficherEtudiants(shared_data.etudiants, windows),
            etudPanWin.close(),
            windows.setEnabled(True)
    
    def edit(etudiant: Etudiant):
        etudPanWin.nce.setValue(int(etudiant.nce))
        etudPanWin.nce.setDisabled(True)
        etudPanWin.nom.setText(etudiant.nom.title())
        etudPanWin.nom.setDisabled(True)
        etudPanWin.prenom.setText(etudiant.prenom.title())
        etudPanWin.prenom.setDisabled(True)
        #print(QtCore.QDate.fromString(etudiant.dateN, "d/M/yyyy").getDate())
        etudPanWin.dateN.setDate(QtCore.QDate.fromString(etudiant.dateN, "d/M/yyyy"))
        etudPanWin.dateN.setDisabled(True)
        etudPanWin.mail.setText(etudiant.mail)
        etudPanWin.telephone.setValue(int(etudiant.telephone))
        sectionIndex = etudPanWin.section.findText(etudiant.section, QtCore.Qt.MatchFixedString)
        etudPanWin.section.setCurrentIndex(sectionIndex)
        niveauIndex = etudPanWin.niveau.findText(etudiant.niveau, QtCore.Qt.MatchFixedString)
        etudPanWin.niveau.setCurrentIndex(niveauIndex)
    
    def resetEtudPan():
        etudPanWin.nce.setValue(0)
        etudPanWin.nce.setDisabled(False)
        etudPanWin.nom.setText("")
        etudPanWin.nom.setDisabled(False)
        etudPanWin.prenom.setText("")
        etudPanWin.prenom.setDisabled(False)
        #print(QtCore.QDate.fromString(etudiant.dateN, "d/M/yyyy").getDate())
        etudPanWin.dateN.setDate(QtCore.QDate.fromString("1/1/2000", "d/M/yyyy"))
        etudPanWin.dateN.setDisabled(False)
        etudPanWin.mail.setText("")
        etudPanWin.telephone.setValue(51907415)
        etudPanWin.section.setCurrentIndex(-1)
        etudPanWin.niveau.setCurrentIndex(-1)
    
    def handleSectionChange():
        etudPanWin.niveau.clear()
        for i in niv[etudPanWin.section.currentText()]:
            etudPanWin.niveau.addItem(i)

    windows.clearBtn.clicked.connect(lambda: windows.searchBar.setText(""))
    windows.searchBar.textChanged.connect(lambda: interface.afficherEtudiants(shared_data.etudiants, windows, windows.searchBar.text()))
    windows.delBtn.clicked.connect(lambda: (e.supprimer(shared_data.etudiants, windows),
                                            windows.table.setCurrentCell(-1, -1),
                                            interface.afficherEtudiants(shared_data.etudiants, windows, ""),
                                            windows.searchBar.setText("")
                                            ))
    windows.addBtn.clicked.connect(lambda: (resetEtudPan(), openAddWindow(windows, etudPanWin)))
    windows.table.setSelectionMode(QtWidgets.QTableWidget.ContiguousSelection)
    windows.table.itemSelectionChanged.connect(lambda: selectCurrentRow(windows))
    windows.table.doubleClicked.connect(lambda: (openEditWindow(windows, etudPanWin), edit(shared_data.etudiants[windows.table.currentRow()])))
    windows.loadBtn.clicked.connect(charger)
    windows.saveBtn.clicked.connect(lambda: dbManager.enregistrer(shared_data.etudiants, "etudiants"))

    windows.comboBoxSection.setDisabled(True)
    windows.comboBoxNiveau.setDisabled(True)
    windows.checkBoxSection.stateChanged.connect(lambda state: windows.comboBoxSection.setDisabled(state != 2))
    windows.checkBoxNiveau.stateChanged.connect(lambda state: windows.comboBoxNiveau.setDisabled(state != 2))

    etudPanWin.setWindowFlags(etudPanWin.windowFlags() | QtCore.Qt.CustomizeWindowHint)
    interface.setWindowBtnsState(etudPanWin, False)
    #etudPanWin.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
    #etudPanWin.dateN.setAlignment(QtCore.Qt.AlignRight)
    etudPanWin.buttonBox.accepted.connect(handleAjouterModifierEtudiant)
    etudPanWin.buttonBox.rejected.connect(lambda: (etudPanWin.close(), windows.setEnabled(True)))

    etudPanWin.section.currentIndexChanged.connect(handleSectionChange)




def loadTabEmprunts(windows):
    global empPanWin

    def charger():
        shared_data.emprunts = dbManager.chargerEmp("emprunts")
        interface.afficherEmprunts(shared_data.emprunts, windows)
    
    def handleAjouterModifierEmprunt():
        if(empty(empPanWin.nce.currentText())):
            interface.alert("Selectionner NCE!")
        elif(empty(empPanWin.reference.currentText())):
            interface.alert("Selectionner reference du livre!")
        elif(empPanWin.nce.isEnabled() and emp.ajouter(empPanWin.nce.currentText(), empPanWin.reference.currentText()) in shared_data.emprunts):
            interface.alert("Cet étudiant a déja emprunté ce livre!")
        elif(e.ajouter(empPanWin.nce.currentText()) not in shared_data.etudiants):
            interface.alert("NCE n'existe pas!")
        elif(l.ajouter(empPanWin.reference.currentText()) not in shared_data.livres):
            interface.alert("Réference n'existe pas!")
        else:
            borrowedBook = list(filter(lambda x: x.reference == empPanWin.reference.currentText(), shared_data.livres))[0]

            if(not empPanWin.nce.isEnabled()):
                bookInstanceIndex = shared_data.emprunts.index(emp.ajouter(empPanWin.nce.currentText(), empPanWin.reference.currentText()))
                nouvNbrExemplaire = str(int(borrowedBook.nombreExemplaires) - int(empPanWin.nombreExemplaires.text()) + int(shared_data.emprunts[bookInstanceIndex].nombreExemplaires))
            else:
                nouvNbrExemplaire = str(int(borrowedBook.nombreExemplaires) - int(empPanWin.nombreExemplaires.text()))
            
            if(int(nouvNbrExemplaire) < 0):
                print(nouvNbrExemplaire)
                interface.alert("Nombre d'exemplaires insuffisant!")
            else:
                if (not empPanWin.nce.isEnabled()):
                    shared_data.emprunts.pop(bookInstanceIndex)
            
                borrowedBook.nombreExemplaires = nouvNbrExemplaire
                shared_data.emprunts.append(
                    emp.ajouter(
                        empPanWin.nce.currentText().strip(),
                        empPanWin.reference.currentText(),
                        empPanWin.dateEmprunt.text().replace('\u200f', ''),
                        "--/--/--",
                        empPanWin.nombreExemplaires.text()
                    )
                )
                interface.afficherEmprunts(shared_data.emprunts, windows),
                empPanWin.close(),
                windows.setEnabled(True)

                # dbManager.enregistrer(livres, "livres")
                # dbManager.enregistrer(etudiants, "etudiants")

    def fillComboBox(comboBox, elems):
        comboBox.clear()
        for i in elems:
            comboBox.addItem(i)
    
    def edit(emprunt: Emprunt):
        fillComboBox(empPanWin.nce, [x.nce for x in shared_data.etudiants])
        fillComboBox(empPanWin.reference, [x.reference for x in shared_data.livres])

        nceIndex = empPanWin.nce.findText(emprunt.nce, QtCore.Qt.MatchFixedString)
        empPanWin.nce.setCurrentIndex(nceIndex)
        empPanWin.nce.setDisabled(True)
        referenceIndex = empPanWin.reference.findText(emprunt.reference, QtCore.Qt.MatchFixedString)
        empPanWin.reference.setCurrentIndex(referenceIndex)
        empPanWin.reference.setDisabled(True)
        empPanWin.dateEmprunt.setDate(QtCore.QDate.fromString(emprunt.dateEmprunt, "d/M/yyyy"))
        empPanWin.dateEmprunt.setDisabled(True)
        #empPanWin.dateRetour.setDate(QtCore.QDate.fromString(emprunt.dateRetour, "d/M/yyyy"))
        #empPanWin.dateRetour.setDisabled(True)
        print("nnnn", emprunt.nombreExemplaires)
        empPanWin.nombreExemplaires.setValue(int(emprunt.nombreExemplaires))
    
    def resetEmpPan():
        empPanWin.nce.setCurrentIndex(-1)
        empPanWin.nce.setDisabled(False)
        empPanWin.reference.setCurrentIndex(-1)
        empPanWin.reference.setDisabled(False)
        current_dateEmprunt = date.today()
        formatted_dateEmprunt = current_dateEmprunt.strftime("%d/%m/%Y")
        empPanWin.dateEmprunt.setDate(QtCore.QDate.fromString(formatted_dateEmprunt, "d/M/yyyy"))
        empPanWin.dateEmprunt.setDisabled(True)
        #dateRetour = current_dateEmprunt + timedelta(weeks=1)
        #formatted_dateRetour = dateRetour.strftime("%d/%m/%Y")
        #empPanWin.dateRetour.setDate(QtCore.QDate.fromString(formatted_dateRetour, "d/M/yyyy"))
        #empPanWin.dateRetour.setMinimumDate(empPanWin.dateEmprunt.date())
        #empPanWin.dateRetour.setDisabled(False)
        empPanWin.nombreExemplaires.setValue(1)

    windows.clearBtn_3.clicked.connect(lambda: windows.searchBar_3.setText(""))
    windows.searchBar_3.textChanged.connect(lambda: interface.afficherEmprunts(shared_data.emprunts, windows, windows.searchBar_3.text()))
    windows.delBtn_3.clicked.connect(lambda: (emp.supprimer(shared_data.emprunts, windows, shared_data.livres),
                                            windows.table_3.setCurrentCell(-1, -1),
                                            interface.afficherEmprunts(shared_data.emprunts, windows, ""),
                                            windows.searchBar_3.setText("")
                                            ))
    windows.retourBtn.clicked.connect(lambda: (emp.retourner(shared_data.emprunts, windows, shared_data.livres),
                                            windows.table_3.setCurrentCell(-1, -1),
                                            interface.afficherEmprunts(shared_data.emprunts, windows, ""),
                                            windows.searchBar_3.setText("")
                                            ))
    windows.addBtn_3.clicked.connect(lambda: (resetEmpPan(), openAddWindow(windows, empPanWin), fillComboBox(empPanWin.nce, [x.nce for x in shared_data.etudiants]), fillComboBox(empPanWin.reference, [x.reference for x in shared_data.livres])))
    windows.table_3.setSelectionMode(QtWidgets.QTableWidget.ContiguousSelection)
    windows.table_3.itemSelectionChanged.connect(lambda: selectCurrentRowEmp(windows))
    windows.table_3.doubleClicked.connect(lambda: (openEditWindow(windows, empPanWin), edit(shared_data.emprunts[windows.table_3.currentRow()])))
    windows.loadBtn_3.clicked.connect(charger)
    windows.saveBtn_3.clicked.connect(lambda: (print(*shared_data.emprunts), dbManager.enregistrer(shared_data.emprunts, "emprunts")))

    empPanWin.setWindowFlags(empPanWin.windowFlags() | QtCore.Qt.CustomizeWindowHint)
    interface.setWindowBtnsState(empPanWin, False)
    #empPanWin.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
    #empPanWin.dateN.setAlignment(QtCore.Qt.AlignRight)
    empPanWin.buttonBox.accepted.connect(handleAjouterModifierEmprunt)
    empPanWin.buttonBox.rejected.connect(lambda: (empPanWin.close(), windows.setEnabled(True)))
    #empPanWin.nce.
    def nceBox():
        if(empPanWin.nce.currentText() in [empPanWin.nce.itemText(i) for i in range(empPanWin.nce.count())]):
            empPanWin.nce.setCurrentIndex(empPanWin.nce.currentIndex())
    #empPanWin.nce.currentTextChanged.connect(nceBox)






def connectNavBar(windows):
    def customDel(delFunction, critere: list):
        if(critere == []):
            interface.alert(msg="Il n'y a plus d'étudiants")
            return
        windows.top_aside.children()[3].click()
        selectedCritere = interface.askForItem(items=list(set(critere)))
        if(selectedCritere != None):
            shared_data.etudiants = delFunction(selectedCritere, shared_data.etudiants)
            windows.table.setCurrentCell(-1, -1)
            interface.afficherEtudiants(shared_data.etudiants, windows, "")
            windows.searchBar.setText("")

    windows.action_Ajouter_tudiant_2.triggered.connect(lambda: (windows.top_aside.children()[3].click(), openAddWindow(windows, etudPanWin)))
    windows.action_Suppression_tudiant_donn.triggered.connect(lambda: interface.alert(msg="Il n'y a plus d'étudiants") if shared_data.etudiants == [] else (
                                                    windows.top_aside.children()[3].click(),
                                                    e.supprimerParNce(interface.askForItem(items=[etud.nce for etud in shared_data.etudiants]), shared_data.etudiants),
                                                    windows.table.setCurrentCell(-1, -1),
                                                    interface.afficherEtudiants(shared_data.etudiants, windows, ""),
                                                    windows.searchBar.setText("")
                                                    ))
    windows.action_Suppression_des_tudiants_d_une_section_donn_e.triggered.connect(lambda: customDel(e.supprimerParSection, [etud.section for etud in shared_data.etudiants]))
    windows.action_Suppression_des_tudiants_d_un_niveau_donn_e.triggered.connect(lambda: customDel(e.supprimerParNiveau, [etud.niveau for etud in shared_data.etudiants]))
    #suppression etudiants par niveau et section .

    tableWindow.setWindowFlags(tableWindow.windowFlags() | QtCore.Qt.CustomizeWindowHint)
    interface.setWindowBtnsState(tableWindow, False)
    #tableWindow.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
    windows.action_Contenu_du_dictionnaire_tudiants.triggered.connect(
        lambda: (
            windows.setEnabled(False),
            interface.previewEtudDBContent(tableWindow)
        )
    #     lambda: (
    #     windows.top_aside.children()[3].click(),
    #     loadTabEtudiants(windows)
    # )
    )

loadTabLivres(windows)
loadTabEtudiants(windows)
loadTabEmprunts(windows)
aside.connectBtns(windows)


connectNavBar(windows)
windows.show()
app.exec_()