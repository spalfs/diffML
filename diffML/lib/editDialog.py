from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout, QLineEdit, QTextEdit, QDialogButtonBox
from PyQt5 import QtGui
from ast import literal_eval

class editDialog(QDialog):
    def __init__(self,index):
        super(editDialog, self).__init__()

        self.resize(550,250)

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Tag",self),0,0)
        layout.addWidget(QLineEdit(index[0].data(),self),0,1,1,2)

        layout.addWidget(QLabel("Text",self),1,0)
        layout.addWidget(QTextEdit(index[1].data(),self),1,1,1,2)

        layout.addWidget(QLabel("Attributes",self),2,0)

        attribs = literal_eval(index[2].data())
        for i, key in enumerate(attribs):
            layout.addWidget(QLineEdit(key,self),i+2,1)
            layout.addWidget(QLineEdit(attribs[key],self),i+2,2)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.ok)
        buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.cancel)

        layout.addWidget(buttonBox, i+3, 0, 1, 3)

        self.exec_()

    def cancel(self):
        self.accept()

    def ok(self):
        print("ok")
        self.accept()
