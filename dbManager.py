import csv
import os
import etudiant as e
import emprunts as emp
import livre as l

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# def existe(nce, etudiants):
#     return e.ajouter(nce) in etudiants

def existe(id, array, module):
    return module.ajouter(id) in array


def charger(fname):
    if(not os.path.isfile(f"{BASE_DIR}/DB/{fname}.csv")):
        print(f"{fname}.csv does not exist in {BASE_DIR}/DB/")
        return []

    etudiants = []
    with open(f"DB/{fname}.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        etudiants = [e.ajouter(*row) for row in csv_reader]
    return etudiants

def chargerLivre(fname):
    if(not os.path.isfile(f"{BASE_DIR}/DB/{fname}.csv")):
        print(f"{fname}.csv does not exist in {BASE_DIR}/DB/")
        return []

    livres = []
    with open(f"DB/{fname}.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        livres = [l.ajouter(*row) for row in csv_reader]
    return livres

#print(*charger('test.csv'), sep="\n")

def chargerEmp(fname):
    if(not os.path.isfile(f"{BASE_DIR}/DB/{fname}.csv")):
        print(f"{fname}.csv does not exist in {BASE_DIR}/DB/")
        return []

    emprunts = []
    with open(f"DB/{fname}.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        emprunts = [emp.ajouter(*row) for row in csv_reader]
    return emprunts


def enregistrer(classList, fname):
    with open(f"DB/{fname}.csv", 'w',newline='\n') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for cls in classList:
            writer.writerow(cls.locals)