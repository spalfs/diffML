from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout, QLineEdit, QTextEdit, QDialogButtonBox
from PyQt5 import QtGui
from ast import literal_eval

class searchDialog(QDialog):
    def __init__(self):
        super(searchDialog, self).__init__()

        self.resize(550,250)

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("What Linknames to search from? (seperated by commas) ", self), 0, 0)

        try:
            f = open('.savedata', 'r')
            text = f.read()
            f.close()
        except:
            text = "z_Input_NumericalValue,z_Table_CellInput,z_Input_StringValue,z_Table_CellInputCheckBox,z_Table_CellInputCheckBoxSmall,"
            text += "z_Table_CellInputString,z_Button_SwitchIconText_Light,z_Switch_IconText_Light,z_Table_CellButtonSwitch,"
            text += "z_Table_CellSwitch,z_Table_CellButton,z_Table_CellButtonSwitch,z_Button_Icon_Light,z_Button_IconText_Light"

        self.text = QTextEdit(text, self)
        layout.addWidget(self.text, 1, 0)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)

        layout.addWidget(buttonBox, 2, 0)

    @staticmethod
    def getInfo():
        dialog = searchDialog()
        result = dialog.exec_()

        if result == 1:
            f = open('.savedata','w')
            f.write(dialog.text.toPlainText())
            f.close()
            return dialog.text.toPlainText().split(',')
        else:
            return False
