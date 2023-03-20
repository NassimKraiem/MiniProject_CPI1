from PyQt5.QtWidgets import QTableWidgetItem
from objects import *
from helper import *

def afficherEtudiants(etudiants, windows, query=""):
    if(empty(query)):
        filtred = etudiants.copy();
    else:
        filtred = list(filter(lambda x: query in x.nom, etudiants));
    
    
    windows.table.setRowCount(len(filtred))
    for i, etudiant in enumerate(filtred):
        windows.table.setItem(i, 0, QTableWidgetItem(etudiant.nom))
        windows.table.setItem(i, 1, QTableWidgetItem(etudiant.prenom))
        windows.table.setItem(i, 2, QTableWidgetItem(etudiant.dateN))
        windows.table.setItem(i, 3, QTableWidgetItem(etudiant.adresse))
        windows.table.setItem(i, 4, QTableWidgetItem(etudiant.mail))
        windows.table.setItem(i, 5, QTableWidgetItem(etudiant.telephone))
        windows.table.setItem(i, 6, QTableWidgetItem(etudiant.section))
        windows.table.setItem(i, 7, QTableWidgetItem(etudiant.niveau))
        
def filterEtudiants():
    pass
