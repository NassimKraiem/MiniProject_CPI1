from PyQt5.QtWidgets import QPushButton
import dbManager
import interfaceFunctions as interface
import shared_data

resets = []

def updateDB():
    # print(shared_data.livres)
    # print(shared_data.etudiants)
    # print(shared_data.emprunts)
    dbManager.enregistrer(shared_data.livres, "livres")
    dbManager.enregistrer(shared_data.etudiants, "etudiants")
    dbManager.enregistrer(shared_data.emprunts, "emprunts")

def resetNavigation():
    for reset in resets:
        reset(False)

def flipState(windows, w, state = None):
    w.setProperty('current', not w.property('current') if state == None else state)
    w.style().unpolish(w)
    w.style().polish(w)
    if(state==True):
        top_aside = list(filter(lambda widget: isinstance(widget, QPushButton) and widget.property('current') != None, windows.top_aside.children()))
        index = top_aside.index(w)
        windows.tabWidget.setCurrentIndex(index)

def completeHandleTabChange(windows, w):
    resetNavigation()
    flipState(windows, w, True)
    updateDB()

def handleTabChange(windows, w):
    completeHandleTabChange(windows, w)
    #interface.confirm(msg = "Changes will be saved when changing tab\nAre you sure?", successFunc = (lambda: completeHandleTabChange(windows, w)))
    #print(msgBox.clickedButton().text())


def connectBtns(windows):
    for widget in windows.top_aside.children():
        if (isinstance(widget, QPushButton) and widget.property('current') != None):
            widget.clicked.connect(lambda _, w=widget: handleTabChange(windows, w))
            resets.append((lambda state, w=widget: flipState(windows, w, state)))

"""
top_aside = list(filter(lambda widget: isinstance(widget, QPushButton) and widget.property('current') != None, windows.top_aside.children()))
for widget in top_aside:
        widget.clicked.connect(lambda _, w=widget: (resetNavigation(), flipState(windows, w, True)))
        resets.append((lambda state, w=widget: flipState(windows, w, state)))
"""