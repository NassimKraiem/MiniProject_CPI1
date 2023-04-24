from tkinter.tix import Tree
import dbManager
from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QSpacerItem, QSizePolicy

def initPressSupport(btn: QPushButton, label, window, lamEdit):
    btn.setAutoRepeat(True)
    btn.setAutoRepeatDelay(1000)
    btn.setAutoRepeatInterval(1000)
    btn.clicked.connect(lambda: handleClicked(btn, label, window, lamEdit))
    btn._state = 0

def handleClicked(btn: QPushButton, label, window, lamEdit):
    if btn.isDown():
        if btn._state == 0:
            btn._state = 1
            btn.setAutoRepeatInterval(50)
            label.setProperty("selected", not (label.property("selected")))
            label.style().unpolish(label)
            label.style().polish(label)
            print('press')
        else:
            print('repeat')
    elif btn._state == 1:
        btn._state = 0
        btn.setAutoRepeatInterval(1000)
        print('release')
    else:
        print('click')
        lamEdit()

def createButton(l, edit, window):
    livre = QPushButton()
    livre.setObjectName(l.reference)
    livre.setFixedHeight(100)
    livre.setFixedWidth(90)



    lb = QLabel()
    initPressSupport(livre, lb, window, lambda: edit(l))
    lb.setProperty("selected", False)
    lb.setAlignment(QtCore.Qt.AlignCenter)
    lb.setStyleSheet("""
    QLabel{
        color: black; background-color: #e1e1e2; font-size: 12px;
    }
    QLabel[selected=true]{
        border-style: solid;
        border-width: 3px;
        border-color: #264653;
    }
    """)
    lb.setFixedHeight(20)
    lb.setFixedWidth(90)
    lb.setText(l.reference) #l.titre
    #lb.setWordWrap(True)

    stylesheet = """
        QPushButton{
            border-image: url('""" + l.couverture + """') 0 0 0 0 stretch stretch;
        }
        QPushButton:pressed{
            border-width: 3px;
        }
        /*QPushButton[selected=true]{
            border-width: 10px;
            background-color: #264653;
        }*/
    """
    livre.setStyleSheet(stylesheet)
    #livre.clicked.connect(lambda: edit(l))
    #livre.setCheckable(True)

    ll = QVBoxLayout()
    ll.addWidget(livre)
    ll.addWidget(lb)
    res = QWidget()
    res.setLayout(ll)

    return res

def getBody(livres, windows, edit, groupBy="Categorie"):
    res = []
    livres = sorted(livres, key=lambda x:(x.categorie, x.reference))
    #cats = set([(i.categorie, *filter(lambda x: x.categorie == i.categorie, livres)) for i in livres])

    print(groupBy, end='|\n')
    if(groupBy=="Categorie"):
        cats = sorted(set([i.categorie for i in livres]))
        livresDesCats = [list(filter(lambda x: x.categorie==cat, livres)) for cat in cats]
    elif(groupBy=="Auteur"):
        cats = sorted(set([i.npAuteur for i in livres]))
        livresDesCats = [list(filter(lambda x: x.npAuteur==cat, livres)) for cat in cats]
    elif(groupBy=="Annee"):
        cats = sorted(set([i.anneeEdition for i in livres]))
        livresDesCats = [list(filter(lambda x: x.anneeEdition==cat, livres)) for cat in cats]
    else:
        raise "Unknown Category!"

    dict = zip(livresDesCats, cats)
    #print(cats)

    stylesheet = """
        QScrollArea{
            background-color: transparent;
            border-style: solid;
            border-width: 1px 0px;
            border-color: #e1e1e1;
        }
        #livres{
            background-color: transparent;
        }
    """

    for ls, c in dict:
        #print(f'    {c}:', end='\n\t')
        #print(*ls, sep='\n\t')
        ttt = QWidget()
        ligne = QVBoxLayout()
        ligne.setObjectName(c)
        ligne.setContentsMargins(0,20,0,0)

        catTitleLabel = QLabel()
        catTitleLabel.setText(f"<h2>{c}</h2>")

        scrollArea = QScrollArea()
        scrollArea.setObjectName(f'ligneLivres{c}')
        scrollArea.setMinimumHeight(165)
        scrollArea.setMaximumHeight(165)
        #scrollArea.setFixedHeight(165)
        scrollArea.setWidgetResizable(True)
        scrollArea.setStyleSheet(stylesheet)
        scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)


        ligne.addWidget(catTitleLabel)
        

        scrollAreaContent = QWidget()
        scrollAreaContent.setObjectName("livres")
        scrollAreaContentLayout = QHBoxLayout()
        for l in ls:
            scrollAreaContentLayout.addWidget(createButton(l, edit, windows))
        scrollAreaContentLayout.addItem(QSpacerItem(40,20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        scrollAreaContent.setLayout(scrollAreaContentLayout)
        scrollArea.setWidget(scrollAreaContent)

        ligne.addWidget(scrollArea)
        
        ttt.setLayout(ligne)
        res.append(ttt)
        
    return res