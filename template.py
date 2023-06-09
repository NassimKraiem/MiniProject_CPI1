import dbManager
from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QSpacerItem, QSizePolicy
from objects import *
import interfaceFunctions as interface
import shared_data

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

def createButton(l: Livre, edit, window):
    livre = QPushButton()
    livre.setObjectName(l.reference)
    livre.setFixedHeight(100)
    livre.setFixedWidth(90)

    lb = QLabel()
    lb.setWordWrap(True)
    initPressSupport(livre, lb, window, lambda: edit(l))
    lb.setProperty("selected", False)
    lb.setProperty("outOfStock", (int(l.nombreExemplaires) <= 0))
    lb.setAlignment(QtCore.Qt.AlignCenter)
    #font-size: 12px
    #print("font-size:",str(12-((len(l.titre)-12)/2 if len(l.titre)>12 else 0)), l.titre)
    lb.setStyleSheet("""
        QLabel{
            color: black; background-color: #e1e1e2; font-size: 12px;
        }
        QLabel[selected=true]{
            border-style: solid;
            border-width: 4px;
            border-color: black;
        }
        QLabel[outOfStock=true]{
            color: white;
            background-color: #e33e33;
        }
        QLabel[outOfStock=false]{
            color: white;
            background-color: #97b85d; /* #a8b56b */
        }
    """)
    lb.setMinimumHeight(20)
    lb.setFixedWidth(90)
    if(window.critereRechLivre.currentText() == "Ref"):
        lb.setText(l.reference)
    else:
        lb.setText(l.titre[:16].title() + ("..." if len(l.titre)>16 else "")) #l.titre
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

def handleHover(windows, lb, delBtn, hidden):
    #print(f"{lb.text()[4:-5]}")
    delBtn.setHidden(hidden)

def handleDeleteByGroup(windows, lb, groupBy):
    if(groupBy=="Categorie"):
        shared_data.livres = list(filter(lambda x: x.categorie.title() != lb.text()[4:-5], shared_data.livres))
        for x in shared_data.livres:
            print(x.categorie, lb.text()[4:-5])
    elif(groupBy=="Auteur"):
        shared_data.livres = list(filter(lambda x: x.npAuteur.title() != lb.text()[4:-5], shared_data.livres))
    elif(groupBy=="Annee"):
        shared_data.livres = list(filter(lambda x: x.anneeEdition.title() != lb.text()[4:-5], shared_data.livres))
    else:
        raise Exception("Unknown Category!")
    
    interface.afficherLivres(shared_data.livres, windows, shared_data.editLivreFunc, groupBy,  query=windows.searchBar_2.text(), critere=windows.critereRechLivre.currentText())
    print("Afficher!")

def getBody(livres, windows, edit, groupBy="Categorie"):
    res = []
    livres = sorted(livres, key=lambda x:(x.categorie, x.reference))
    #cats = set([(i.categorie, *filter(lambda x: x.categorie == i.categorie, livres)) for i in livres])

    #print(groupBy, end='|\n')
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
        raise Exception("Unknown Category!")

    dict = zip(livresDesCats, cats)
    #print(cats)

    stylesheet = """
        QScrollArea{
            background-color: transparent;
            border-style: solid;
            border-width: 1px 0px 0px 0px;
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
        ligne.setObjectName(''.join(c.split()))
        ligne.setContentsMargins(0,20,0,0)

        titleLbLayout = QHBoxLayout() 
        titleLbLayout.setContentsMargins(0,0,0,0)
        titleLb = QWidget()

        catTitleLabel = QLabel()
        catTitleLabel.setText(f"<h2>{c.title()}</h2>")

        delBtn = QPushButton()
        delBtn.setObjectName("delBtn")
        delBtn.setText("X")
        delBtn.setFixedSize(20, 20)
        delBtn.clicked.connect(lambda _, lb=catTitleLabel: handleDeleteByGroup(windows, lb, groupBy))
        delBtn.setStyleSheet("""
            QPushButton{
                color: red;
            }
            QPushButton:pressed{
                color: white;
            }
        """)
        delBtn.setFlat(True)
        delBtn.setHidden(True)
        
        titleLb.enterEvent = lambda e, lb=catTitleLabel, btn=delBtn: handleHover(windows, lb, btn, False)
        titleLb.leaveEvent = lambda e, lb=catTitleLabel, btn=delBtn: handleHover(windows, lb, btn, True)

        # self.hover_widget = QLabel('Hovered!')
        # self.hover_widget.hide()

        # def enterEvent(self, event):
        #     self.hover_widget.show()

        # def leaveEvent(self, event):
        #     self.hover_widget.hide()

        scrollArea = QScrollArea()
        scrollArea.setObjectName(f'ligneLivres{c}')
        scrollArea.setMinimumHeight(175)
        scrollArea.setMaximumHeight(175)
        #scrollArea.setFixedHeight(175)
        scrollArea.setWidgetResizable(True)
        scrollArea.setStyleSheet(stylesheet)
        scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)


        titleLbLayout.addWidget(catTitleLabel)
        titleLbLayout.addWidget(delBtn)
        titleLbLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        titleLb.setLayout(titleLbLayout)

        ligne.addWidget(titleLb)
        

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