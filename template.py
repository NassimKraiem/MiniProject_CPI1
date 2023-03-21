import dbManager
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QSpacerItem, QSizePolicy

def btn(l):
    livre = QPushButton(l.reference)
    livre.setFixedHeight(100)
    livre.setFixedWidth(90)
    livre.setText(l.titre)
    return livre
    f"""
        <item>
            <widget class="QPushButton" name="{l.reference}">
                <property name="minimumSize">
                    <size>
                        <width>0</width>
                        <height>100</height>
                    </size>
                </property>
                <property name="maximumSize">
                    <size>
                        <width>90</width>
                        <height>16777215</height>
                    </size>
                </property>
                <property name="text">
                    <string>PushButton</string>
                </property>
            </widget>
        </item>
    """

def getBody(livres, windows):
    res = []
    livres = sorted(livres, key=lambda x:x.categorie)
    #cats = set([(i.categorie, *filter(lambda x: x.categorie == i.categorie, livres)) for i in livres])
    cats = set([i.categorie for i in livres])
    livresDesCats = [list(filter(lambda x: x.categorie==cat, livres)) for cat in cats]
    dict = zip(livresDesCats, cats)
    print(cats)

    for ls, c in dict:
        print(f'    {c}:', end='\n\t')
        print(*ls, sep='\n\t')
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
        continue
        res.append("""
            <item>
                <layout class="QVBoxLayout" name="classique">
                    <property name="topMargin">
                        <number>20</number>
                    </property>
                    <item>
                        <widget class="QLabel" name="label">
                            <property name="text">
                                <string>&lt;h2&gt;{c}&lt;/h2&gt;</string>
                            </property>
                        </widget>
                    </item>
                    <item>
                        <widget class="QScrollArea" name="{f'ligneLivres{c}'}">
                            <property name="minimumSize">
                                <size>
                                    <width>0</width>
                                    <height>135</height>
                                </size>
                            </property>
                            <property name="maximumSize">
                                <size>
                                    <width>16777215</width>
                                    <height>135</height>
                                </size>
                            </property>
                            <property name="verticalScrollBarPolicy">
                                <enum>Qt::ScrollBarAlwaysOff</enum>
                            </property>
                            <property name="widgetResizable">
                                <bool>true</bool>
                            </property>
                            <widget class="QWidget" name="livres">
                                <property name="geometry">
                                    <rect>
                                        <x>0</x>
                                        <y>0</y>
                                        <width>488</width>
                                        <height>133</height>
                                    </rect>
                                </property>
                                <layout class="QHBoxLayout" name="horizontalLayout_4">
                                    <property name="bottomMargin">
                                        <number>9</number>
                                    </property>
                                    
                                    {'\n'.join([btn(l) for l in ls])}

                                    <item>
                                        <spacer name="horizontalSpacer_3">
                                            <property name="orientation">
                                                <enum>Qt::Horizontal</enum>
                                            </property>
                                            <property name="sizeHint" stdset="0">
                                                <size>
                                                    <width>40</width>
                                                    <height>20</height>
                                                </size>
                                            </property>
                                        </spacer>
                                    </item>
                                </layout>
                            </widget>
                        </widget>
                    </item>
                </layout>
            </item>
        """)
    return res