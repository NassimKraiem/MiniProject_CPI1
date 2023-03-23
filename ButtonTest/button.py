from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QPushButton

app = QApplication([])
window = loadUi("button.ui")

def init(btn: QPushButton):
    btn.setAutoRepeat(True)
    btn.setAutoRepeatDelay(1000)
    btn.setAutoRepeatInterval(1000)
    btn.clicked.connect(lambda: handleClicked(btn))
    btn._state = 0

def handleClicked(btn: QPushButton):
    if btn.isDown():
        if btn._state == 0:
            btn._state = 1
            btn.setAutoRepeatInterval(50)
            print('press')
            window.stateLabel.setText('State: press')
        else:
            print('repeat')
            window.stateLabel.setText('State: repeat')
    elif btn._state == 1:
        btn._state = 0
        btn.setAutoRepeatInterval(1000)
        print('release')
        window.stateLabel.setText('State: release')
    else:
        print('click')
        window.stateLabel.setText('State: click')

init(window.btn)
window.show()
app.exec_()