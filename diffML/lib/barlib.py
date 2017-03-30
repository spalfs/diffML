from PyQt5.QtWidgets import qApp, QAction

class  menubar():
    def __init__(self, view):
        menubar = view.menuBar()

        fileMenu = menubar.addMenu('&File')

        openXMLButton = QAction('&Open',view)
        openXMLButton.triggered.connect(view.openXML)
        fileMenu.addAction(openXMLButton)

        saveXMLButton = QAction('&Save',view)
        saveXMLButton.triggered.connect(view.saveXML)
        fileMenu.addAction(saveXMLButton)

        exitButton = QAction('&Exit',view)
        exitButton.triggered.connect(qApp.quit)
        fileMenu.addAction(exitButton)

        editMenu = menubar.addMenu('&Edit')

        viewMenu = menubar.addMenu('&View')

        colorizeButton = QAction('&Colorize',view)
        colorizeButton.triggered.connect(view.colorize)
        viewMenu.addAction(colorizeButton)

        compareButton = QAction('&Compare Selected Elements',view)
        compareButton.triggered.connect(view.compare)
        viewMenu.addAction(compareButton)

        helpMenu = menubar.addMenu('&Help')

