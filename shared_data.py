import dbManager

livres = dbManager.chargerLivre("livres")
etudiants = dbManager.charger("etudiants")
emprunts = dbManager.chargerEmp("emprunts")

tempDateRetour = ""

editLivreFunc = lambda: None