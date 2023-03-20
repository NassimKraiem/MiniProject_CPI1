import aside
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication

app = QApplication([])
windows = loadUi("main.ui")


aside.connectBtns(windows)
windows.show()
app.exec_()