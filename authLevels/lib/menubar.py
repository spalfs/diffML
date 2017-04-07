from PyQt5.QtWidgets import QAction

class  menubar():
    def __init__(self, view):
        menubar = view.menuBar()

        fileMenu = menubar.addMenu('&File')

        openXMLButton = QAction('&Open', view)
        openXMLButton.triggered.connect(view.open)
        fileMenu.addAction(openXMLButton)

        saveButton = QAction('&Save',view)
        saveButton.triggered.connect(view.save)
        fileMenu.addAction(saveButton)

        saveAsButton = QAction('&Save As...',view)
        saveAsButton.triggered.connect(view.saveAs)
        fileMenu.addAction(saveAsButton)

        editMenu = menubar.addMenu('&Edit')

        undoButton = QAction('&Undo', view)
        undoButton.triggered.connect(view.undo)
        editMenu.addAction(undoButton)

        viewMenu = menubar.addMenu('&View')

        showButton = QAction('&Show incorrect formating', view)
        showButton.triggered.connect(view.toggleShow)
        viewMenu.addAction(showButton)

        csvButton = QAction('&Open CSV Language File', view)
        csvButton.triggered.connect(view.openCSV)
        viewMenu.addAction(csvButton)
