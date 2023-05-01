from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QInputDialog, QSpacerItem, QSizePolicy
import dbManager
import template
from objects import *
from helper import *

def afficherEtudiants(etudiants, windows, query=""):
    if(empty(query)):
        filtred = etudiants.copy()
    else:
        filtred = list(filter(lambda x: query in x.nom, etudiants))
    
    
    windows.table.setRowCount(len(filtred))
    for i, etudiant in enumerate(filtred):
        item = QTableWidgetItem(etudiant.nce)
        windows.table.setVerticalHeaderItem(i, item)
        windows.table.setItem(i, 0, QTableWidgetItem(etudiant.nom))
        windows.table.setItem(i, 1, QTableWidgetItem(etudiant.prenom))
        windows.table.setItem(i, 2, QTableWidgetItem(etudiant.dateN))
        windows.table.setItem(i, 3, QTableWidgetItem(etudiant.adresse))
        windows.table.setItem(i, 4, QTableWidgetItem(etudiant.mail))
        windows.table.setItem(i, 5, QTableWidgetItem(etudiant.telephone))
        windows.table.setItem(i, 6, QTableWidgetItem(etudiant.section))
        windows.table.setItem(i, 7, QTableWidgetItem(etudiant.niveau))


def afficherEmprunts(emprunts, windows, query=""):
    if(empty(query)):
        filtred = emprunts.copy()
    else:
        filtred = list(filter(lambda x: query.lower() in x.nce, emprunts))
    
    windows.table_3.setRowCount(len(filtred))
    for i, emprunt in enumerate(filtred):
        #item = QTableWidgetItem()
        #windows.table_3.setVerticalHeaderItem(i, item)
        windows.table_3.setItem(i, 0, QTableWidgetItem(emprunt.nce))
        windows.table_3.setItem(i, 1, QTableWidgetItem(emprunt.reference))
        windows.table_3.setItem(i, 2, QTableWidgetItem(emprunt.dateEmprunt))
        windows.table_3.setItem(i, 3, QTableWidgetItem(emprunt.dateRetour))
        windows.table_3.setItem(i, 4, QTableWidgetItem(emprunt.nombreExemplaires))

        
# def filterEtudiants(etudiants, windows):
#     query = windows.searchBar.text()
#     return etudiants.copy() if empty(query) else list(filter(lambda x: query in x.nom, etudiants))




# def clearLayout(layout):
#     while layout.count():
#         child = layout.takeAt(0).widget().deleteLater()

def clearLayout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()
        else:
            spacer_item = item.spacerItem()
            if spacer_item:
                layout.removeItem(spacer_item)

def afficherLivres(livres, windows, edit, groupBy="Categorie", query="", critere="Titre"):
    # print('-'*30)
    # print(*sorted(livres, key=lambda x:x.categorie), sep="\n")
    # print('-'*30)

    clearLayout(windows.scrollAreaContent.layout())

    if(empty(query)):
        filtred = livres.copy()
    else:
        if(critere=="Titre"):
            filtred = list(filter(lambda x: query.lower() in x.titre, livres))
        elif(critere=="Ref"):
            filtred = list(filter(lambda x: query.lower() in x.reference, livres))
        else:
            raise "Critere de recherce doit etre 'Titre' ou 'Ref'!"

    lignes = template.getBody(filtred, windows, edit, groupBy)
    for ligne in lignes:
        windows.scrollAreaContent.layout().addWidget(ligne)
    spacer = QSpacerItem(20, 1000, QSizePolicy.Minimum, QSizePolicy.Expanding)
    windows.scrollAreaContent.layout().addItem(spacer)











def setWindowBtnsState(win, state):
    win.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, state)
    win.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, state)
    win.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, state)

def previewEtudDBContent(window):
    window.show()
    etudiants = dbManager.charger("etudiants")
    afficherEtudiants(etudiants, window)














def error(msg="Critical", title="Error MessageBox"):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText(msg)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec_()

def alert(msg="Warning", title="Warning MessageBox"):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setText(msg)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec_()

def confirm(msg="Are you sure?", title="Question MessageBox", successFunc = lambda: None, failFunc = lambda: None):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Question)
    msgBox.setText(msg)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msgBox.setDefaultButton(QMessageBox.Ok)
    msgBox.accepted.connect(lambda: successFunc())
    msgBox.rejected.connect(failFunc)
    msgBox.exec_()

def askForInt(msg="Donner n:", title="Input Dialog"):
    input = QInputDialog()
    input.setWindowTitle("test")
    n, done = QInputDialog.getInt(input, title, msg)
    print(n, done)
    if done:
        return n
    else:
        return None

def askForItem(msg="Selectionner:", title="Input Dialog", items=["test"]):
    input = QInputDialog()
    item, done = QInputDialog.getItem(input, title, msg, items, -1, False)
    print(item, done)
    if done:
        return item
    else:
        return None