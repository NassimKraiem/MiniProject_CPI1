from PyQt5.QtWidgets import QTableWidgetItem
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





def afficherLivres(livres, windows):
    print('-'*30)
    print(*sorted(livres, key=lambda x:x.categorie), sep="\n")