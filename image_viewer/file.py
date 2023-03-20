from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QFileDialog

app = QApplication([])
windows = loadUi ("file.ui")


def clicker():
    fname = QFileDialog.getOpenFileName(windows, "Select book Image", "", "Image Files (*.png, *jpg)")
    if(fname):
        windows.urlLabel.setText(fname[0])
        windows.imgLabel.setStyleSheet(f"border-image : url({fname[0]}) 0 0 0 0 stretch stretch;")


windows.btn.clicked.connect(clicker)

windows.show()
app.exec_()