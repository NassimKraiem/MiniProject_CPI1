from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QInputDialog
import dbManager
import template
from objects import *
from helper import *

def afficherEtudiants(etudiants, windows, query=""):
    if(empty(query)):
        filtred = etudiants.copy();
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
        
# def filterEtudiants(etudiants, windows):
#     query = windows.searchBar.text()
#     return etudiants.copy() if empty(query) else list(filter(lambda x: query in x.nom, etudiants))




def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0).widget().deleteLater()

def afficherLivres(livres, windows, edit, groupBy="Categorie"):
    # print('-'*30)
    # print(*sorted(livres, key=lambda x:x.categorie), sep="\n")
    # print('-'*30)

    clearLayout(windows.scrollAreaContent.layout())

    lignes = template.getBody(livres, windows, edit, groupBy)
    for ligne in lignes:
        windows.scrollAreaContent.layout().addWidget(ligne)











def setWindowBtnsState(win, state):
    win.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, state)
    win.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, state)
    win.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, state)

def previewEtudDBContent(window):
    window.show()
    etudiants = dbManager.charger("etudiants")
    afficherEtudiants(etudiants, window)
    print("nnnnnnnnnn")














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