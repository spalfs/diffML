from PyQt5.QtWidgets import qApp, QAction, QActionGroup

from lib.CONSTANTS import NONE, HIERARCHY, CHANGED, FIELD, ORDER

class  menubar():
    def __init__(self, view):
        menubar = view.menuBar()

        fileMenu = menubar.addMenu('&File')

        openXMLButton = QAction('&Open', view)
        openXMLButton.triggered.connect(view.open)
        fileMenu.addAction(openXMLButton)

        exportButton = QAction('&Export as CSV', view)
        exportButton.triggered.connect(view.export)
        fileMenu.addAction(exportButton)

        saveButton = QAction('&Save',view)
        saveButton.triggered.connect(view.save)
        fileMenu.addAction(saveButton)

        saveAsButton = QAction('&Save As...',view)
        saveAsButton.triggered.connect(view.saveAs)
        fileMenu.addAction(saveAsButton)

        exitButton = QAction('&Exit',view)
        exitButton.triggered.connect(qApp.quit)
        fileMenu.addAction(exitButton)

        editMenu = menubar.addMenu('&Edit')

        matchingFieldButton = QAction('&Compare selected by matching fields', view)
        matchingFieldButton.triggered.connect(lambda : view.matching(FIELD))
        editMenu.addAction(matchingFieldButton)

        matchingOrderButton = QAction('&Compare selected by matching order', view)
        matchingOrderButton.triggered.connect(lambda : view.matching(ORDER))
        editMenu.addAction(matchingOrderButton)

        viewMenu = menubar.addMenu('&View')

        revealButton = QAction('&Reveal hidden elements',view)
        revealButton.triggered.connect(view.reveal)
        viewMenu.addAction(revealButton)

        addViewButton = QAction('&Enable Second Workspace',view)
        addViewButton.setCheckable(True)
        addViewButton.triggered.connect(view.toggleViewTwo)
        viewMenu.addAction(addViewButton)

        syncButton = QAction('&Enable Syncronized Scrolling',view)
        syncButton.setCheckable(True)
        syncButton.triggered.connect(view.toggleSync)
        viewMenu.addAction(syncButton)

        colorizeButton = viewMenu.addMenu('&Colorize')
        colorizeGroup = QActionGroup(view)

        noneButton = QAction('&None',view)
        noneButton.triggered.connect( lambda : view.setColor(NONE))
        noneButton.setCheckable(True)
        noneButton.setChecked(True)
        colorizeButton.addAction(noneButton)
        colorizeGroup.addAction(noneButton)

        hierarchyButton = QAction('&Hierarchy',view)
        hierarchyButton.triggered.connect( lambda : view.setColor(HIERARCHY))
        hierarchyButton.setCheckable(True)
        colorizeButton.addAction(hierarchyButton)
        colorizeGroup.addAction(hierarchyButton)

        changesButton = QAction('&Changes',view)
        changesButton.triggered.connect( lambda : view.setColor(CHANGED))
        changesButton.setCheckable(True)
        colorizeButton.addAction(changesButton)
        colorizeGroup.addAction(changesButton)

        colorizeGroup.setExclusive(True)

        helpMenu = menubar.addMenu('&Help')
