import dbManager

livres = dbManager.chargerLivre("livres")
etudiants = dbManager.charger("etudiants")
emprunts = dbManager.chargerEmp("emprunts")

editLivreFunc = lambda: None