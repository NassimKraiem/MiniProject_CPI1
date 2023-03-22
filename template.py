import dbManager
from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QSpacerItem, QSizePolicy

def btn(l, edit):
    livre = QPushButton()
    livre.setObjectName(l.reference)
    livre.setFixedHeight(100)
    livre.setFixedWidth(90)

    lb = QLabel()
    lb.setAlignment(QtCore.Qt.AlignCenter)
    lb.setStyleSheet("color: black; background-color: #e1e1e2; font-size: 12px;")
    lb.setFixedHeight(20)
    lb.setFixedWidth(90)
    lb.setText(l.reference) #l.titre
    #lb.setWordWrap(True)

    stylesheet = """
        QPushButton{
            border-image: url('""" + l.couverture + """') 0 0 0 0 stretch stretch;
        }
        QPushButton:pressed{
            border-width: 4px
        }
    """
    livre.setStyleSheet(stylesheet)
    livre.clicked.connect(lambda: edit(l))
    #livre.setCheckable(True)

    ll = QVBoxLayout()
    ll.addWidget(livre)
    ll.addWidget(lb)
    res = QWidget()
    res.setLayout(ll)

    return res

def getBody(livres, windows, edit):
    res = []
    livres = sorted(livres, key=lambda x:x.categorie)
    #cats = set([(i.categorie, *filter(lambda x: x.categorie == i.categorie, livres)) for i in livres])
    cats = sorted(set([i.categorie for i in livres]))
    livresDesCats = [list(filter(lambda x: x.categorie==cat, livres)) for cat in cats]
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
            scrollAreaContentLayout.addWidget(btn(l, edit))
        scrollAreaContentLayout.addItem(QSpacerItem(40,20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        scrollAreaContent.setLayout(scrollAreaContentLayout)
        scrollArea.setWidget(scrollAreaContent)

        ligne.addWidget(scrollArea)
        
        ttt.setLayout(ligne)
        res.append(ttt)
        
    return res