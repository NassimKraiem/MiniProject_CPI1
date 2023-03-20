import csv
import etudiant as e

def existe(nce, etudiants):
    return e.ajouter(nce) in etudiants


def charger():
    etudiants = []
    with open('test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        etudiants = [e.ajouter(*row) for row in csv_reader]
    return etudiants

print(*charger(), sep="\n")


def enregistrer(etudiants):
    with open('test.csv', 'w',newline='\n') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for etudiant in etudiants:
            writer.writerow(etudiant.locals)