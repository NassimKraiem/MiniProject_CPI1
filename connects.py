from PyQt5 import QtGui, QtCore, QtWidgets

def openAddWindow(windows, addWindow):
    windows.setEnabled(False)
    addWindow.show()

def selectCurrentRow(windows):
    windows.table.blockSignals(True)
    windows.table.selectRow(windows.table.currentRow())
    windows.table.blockSignals(False)
    #print(set([i.row() for i in windows.table.selectedIndexes()]))

    #windows.table.setSelectionMode(QtWidgets.QTableWidget.ExtendedSelection)
    # print("-"*50)
    # print()
    # for i in windows.table.selectedIndexes():
    #     print(f"(col:{i.column()} row:{i.row()})")

def selectCurrentRowEmp(windows):
    windows.table_3.blockSignals(True)
    windows.table_3.selectRow(windows.table_3.currentRow())
    windows.table_3.blockSignals(False)

def openEditWindow(windows, editWindow):
    print(windows.table.model().data(windows.table.model().index(windows.table.currentRow(), 0)))
    #fill data in edit window with current row data
    windows.setEnabled(False)
    editWindow.show()