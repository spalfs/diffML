from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout, QLineEdit, QTextEdit, QDialogButtonBox
from PyQt5 import QtGui
from ast import literal_eval

class editDialog(QDialog):
    def __init__(self,index):
        super(editDialog, self).__init__()

        self.resize(550,250)

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Tag", self), 0, 0)

        self.tag = QLineEdit(index[0].data(), self)
        layout.addWidget(self.tag, 0, 1, 1, 2)

        layout.addWidget(QLabel("Text",self), 1, 0)

        self.text = QTextEdit(index[1].data(),self)
        layout.addWidget(self.text, 1, 1, 1, 2)

        layout.addWidget(QLabel("Attributes", self), 2, 0)

        self.attribs = []
        attribs = literal_eval(index[2].data())
        i = 0
        for i, key in enumerate(attribs):
            left = QLineEdit(key, self)
            layout.addWidget(left, i+2, 1)

            right = QLineEdit(attribs[key], self)
            layout.addWidget(right, i+2, 2)

            self.attribs.append((left,right))

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)

        layout.addWidget(buttonBox, i+3, 0, 1, 3)

    @staticmethod
    def getInfo(index):
        dialog = editDialog(index)
        result = dialog.exec_()

        if result == 1:
            changes = {}

            changes['tag'] = dialog.tag.text()
            changes['text'] = dialog.text.toPlainText()

            attribs = {}
            for attrib in dialog.attribs:
                attribs[attrib[0].text()] = attrib[1].text()

            changes['attribs'] = attribs

            return changes

        else:
            return False
