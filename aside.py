from cmath import pi
from PyQt5.QtWidgets import QPushButton


resets = []

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

def connectBtns(windows):
    for widget in windows.top_aside.children():
        if (isinstance(widget, QPushButton) and widget.property('current') != None):
            widget.clicked.connect(lambda _, w=widget: (resetNavigation(), flipState(windows, w, True)))
            resets.append((lambda state, w=widget: flipState(windows, w, state)))

"""
top_aside = list(filter(lambda widget: isinstance(widget, QPushButton) and widget.property('current') != None, windows.top_aside.children()))
for widget in top_aside:
        widget.clicked.connect(lambda _, w=widget: (resetNavigation(), flipState(windows, w, True)))
        resets.append((lambda state, w=widget: flipState(windows, w, state)))
"""