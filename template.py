import dbManager
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QSpacerItem, QSizePolicy

def btn(l):
    livre = QPushButton(l.reference)
    livre.setFixedHeight(100)
    livre.setFixedWidth(90)
    livre.setText(l.titre)
    stylesheet = "QPushButton { border-image: url('" + l.couverture + "') 0 0 0 0 stretch stretch;}"
    livre.setStyleSheet(stylesheet)
    return livre

def getBody(livres, windows):
    res = []
    livres = sorted(livres, key=lambda x:x.categorie)
    #cats = set([(i.categorie, *filter(lambda x: x.categorie == i.categorie, livres)) for i in livres])
    cats = sorted(set([i.categorie for i in livres]))
    livresDesCats = [list(filter(lambda x: x.categorie==cat, livres)) for cat in cats]
    dict = zip(livresDesCats, cats)
    #print(cats)

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
        scrollArea.setMinimumHeight(135)
        scrollArea.setMaximumHeight(135)
        #scrollArea.setFixedHeight(135)
        #scrollArea.setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff)
        scrollArea.setWidgetResizable(True)


        ligne.addWidget(catTitleLabel)
        #ligne.addWidget(btn(ls[0]))
        

        scrollAreaContent = QWidget()
        scrollAreaContentLayout = QHBoxLayout()
        for l in ls:
            scrollAreaContentLayout.addWidget(btn(l))
        scrollAreaContentLayout.addItem(QSpacerItem(40,20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        scrollAreaContent.setLayout(scrollAreaContentLayout)
        scrollArea.setWidget(scrollAreaContent)

        ligne.addWidget(scrollArea)
        
        ttt.setLayout(ligne)
        res.append(ttt)
        
    return res