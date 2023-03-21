def openAddWindow(windows, addWindow):
    windows.setEnabled(False)
    addWindow.show()

def selectCurrentRow(windows):
    windows.table.selectRow(windows.table.currentRow())

def openEditWindow(windows, editWindow):
    print(windows.table.model().data(windows.table.model().index(windows.table.currentRow(), 0)))
    #fill data in edit window with current row data
    windows.setEnabled(False)
    editWindow.show()