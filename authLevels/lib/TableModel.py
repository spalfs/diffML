from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime
from ast import literal_eval
import xml.etree.ElementTree as ET

class TableModel(QAbstractTableModel):
    def __init__(self, masterView, path, search, parent=None):
        super(TableModel, self).__init__(parent)

        self.path = path

        self.items = []

        self.masterView = masterView

        self.changes = []

        self.search = search

        self.setupModel()

def setupModel(self):
        self.XMLTree = ET.parse(self.path)
        root = self.XMLTree.getroot()

        for screen in root.iter("Picture"):
            if str(screen.attrib).find("Kopie") != -1 or str(screen.attrib).find("z_") != -1:
                continue
            for i in range(100):
                for element in screen.iter("Elements_"+str(i)):
                    item = {}
                    item['tag'] = False
                    item['changed'] = False
                    tmp = str(screen.attrib)
                    tmp = tmp[tmp.find(":")+3:-2]
                    item['screen'] = tmp
                    for text in self.search:
                        link = element.findall("LinkName")
                        if len(link) != 0:
                            if link[0].text == text:
                                for j in range(10):
                                    for prop in element.iter("ExpProps_"+str(j)):
                                        var = prop.findall("Name")[0].text
                                        find = var.find("Variable")
                                        if find != -1:
                                            tmp = prop.findall("ExpPropValue")[0].text
                                            tmp = tmp[tmp.find("<SymVarTagNr>")+len("<SymVarTagNr>"):tmp.find("</SymVarTagNr>")]
                                            item['tag'] = tmp

                                        var = prop.findall("Name")[0].text
                                        find = var.find("Passwordlevel")
                                        if find != -1:
                                            tmp = prop.findall("ExpPropValue")[0].text
                                            tmp = tmp[tmp.find("<Passwordlevel>")+len("<Passwordlevel>"):tmp.find("</Passwordlevel>")]
                                            item['plvl'] = tmp

                    item['element'] = element
                    if item['tag']:
                        self.items.append(item)

    def save(self,path=None):
        if path is None:
            path = self.path

        f = open('changelog.txt','a')
        f.write(str(datetime.now())+'\n')
        for change in self.changes:
            f.write(self.items[change['index'].row()]['tag'] + " from " + change['before'] + " to " + change['after'] + '\n')
        f.close()

        self.changes = []

        for item in self.items:
            item['changed'] = False

        self.XMLTree.write(path)

    def undo(self):
        try:
            change = self.changes.pop()
            self.setData(change['index'],change['before'],2,True)

        except:
            print("nothing to undo")

    def isChanges(self):
        if len(self.changes) > 0:
            return True
        else:
            return False

    def flipI(self, x):
        if x == '1':
            return 'A'
        if x == '2':
            return 'B'
        if x == '3':
            return 'C'
        if x == '4':
            return 'D'
        if x == '5':
            return 'E'
        return False

    def flipS(self, x):
        if x == 'A':
            return '1'
        if x == 'B':
            return '2'
        if x == 'C':
            return '3'
        if x == 'D':
            return '4'
        if x == 'E':
            return '5'
        return False

    def columnCount(self, parent):
        return 3

    def rowCount(self, parent):
        return len(self.items)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return "Tag"
            elif section == 1:
                return "Password Level"
            else:
                return "Screen"

        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        if index.column() == 1:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable

        return Qt.ItemIsEnabled

    def data(self, index, role):
        if not index.isValid():
            return None

        row = index.row()
        column = index.column()

        text = self.flipI(self.items[row]['plvl'])

        if role == Qt.BackgroundRole:
            if self.items[index.row()]['changed']:
                return QBrush(Qt.red)
            else:
                return QBrush(Qt.transparent)

        if role == Qt.EditRole:
            return QVariant(text)

        if role != Qt.DisplayRole:
            return None

        if column == 0:
            return QVariant(self.items[row]['tag'])
        elif column == 1:
            return QVariant(text)
        elif column == 2:
            return QVariant(self.items[row]['screen'])

        return QVariant()

    def setData(self, index, value, role, undo = False):

        value = self.flipS(value)

        if not value:
            QMessageBox.warning(self.masterView,"Error:","Only the values A, B, C, D or E are allowed.", QMessageBox.Ok)
            return False


        if index.column() == 1:
            if undo:
                self.items[index.row()]['changed'] = False
            elif self.items[index.row()]['plvl'] != value:
                self.items[index.row()]['changed'] = True
                self.changes.append({'index' : index, 'before' : self.flipI(self.items[index.row()]['plvl']), 'after' : self.flipI(value)})

            self.items[index.row()]['plvl'] = value
            for j in range(10):
                for prop in self.items[index.row()]['element'].iter("ExpProps_"+str(j)):
                    var = prop.findall("Name")[0].text
                    find = var.find("Passwordlevel")
                    if find != -1:
                        prop.findall("ExpPropValue")[0].text = "<Passwordlevel>"+value+"</Passwordlevel>"

        return True

    def sort(self, col, order):
        self.layoutAboutToBeChanged.emit()
        if col == 0:
            if order == 0:
                self.items = sorted(self.items, key = lambda k: k['tag'])
            else:
                self.items = sorted(self.items, key = lambda k: k['tag'], reverse = True)
        elif col == 1:
            if order == 0:
                self.items = sorted(self.items, key = lambda k: k['plvl'])
            else:
                self.items = sorted(self.items, key = lambda k: k['plvl'], reverse = True)
        elif col == 2:
            if order == 0:
                self.items = sorted(self.items, key = lambda k: k['screen'])
            else:
                self.items = sorted(self.items, key = lambda k: k['screen'], reverse = True)

        self.layoutChanged.emit()
