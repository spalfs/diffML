from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime
import csv
import chardet

import xml.etree.ElementTree as ET

class TableModel(QAbstractTableModel):
    def __init__(self, masterView, path, search, parent=None):
        super(TableModel, self).__init__(parent)

        self.path = path

        self.items = []

        self.masterView = masterView

        self.changes = []

        self.search = search

        self.show = False

        self.setupModel()

    def setupModel(self):
        self.XMLTree = ET.parse(self.path)
        root = self.XMLTree.getroot()

        for screen in root.iter("Picture"):
            if str(screen.attrib).find("Kopie") != -1 or str(screen.attrib).find("z_") != -1:
                continue
            if str(screen.attrib).find("p_") != -1 or str(screen.attrib).find("_Popup") != -1:
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
                                item['type'] = text
                                for j in range(100):
                                    for prop in element.iter("ExpProps_"+str(j)):
                                        var = prop.findall("Name")[0].text
                                        find = var.find("Variable")
                                        if find != -1:
                                            sTag = "<SymVarTagNr>"
                                            eTag = sTag[0] + "/" + sTag[1:]
                                            nTag = sTag[:-1] + "/" + sTag[-1]

                                            tmp = prop.findall("ExpPropValue")[0].text

                                            if tmp.find(nTag) != -1:
                                                continue
                                            else:
                                                item['tag'] = tmp[tmp.find(sTag)+len(sTag) : tmp.find(eTag)]

                                        var = prop.findall("Name")[0].text
                                        find = var.find("Passwordlevel")
                                        if find != -1:
                                            sTag = "<Passwordlevel>"
                                            eTag = sTag[0] + "/" + sTag[1:]
                                            nTag = sTag[:-1] + "/" + sTag[-1]

                                            tmp = prop.findall("ExpPropValue")[0].text
                                            tmp = tmp[tmp.find(sTag)+len(sTag):tmp.find(eTag)]
                                            item['plvl'] = tmp

                    item['element'] = element
                    if item['tag']:
                        good = self.checkFormat(item)
                        if good:
                            item['format'] = True
                        else:
                            item['format'] = False
                        self.items.append(item)

    def giveCSV(self, path, language):
        if language[0] == "ZENONSTR.TXT":
            col = 1
        elif language[0] == "FR_FR.TXT":
            col = 2
        elif language[0] == "GB_EN.TXT":
            col = 3

        with open(path, 'rb') as f:
            result = chardet.detect(f.read())

        with open(path, encoding=result['encoding']) as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for item in self.items:
                if item['format']:
                    parts = item['tag'].split("@")
                    for line in reader:
                        if line[0] == parts[1]:
                            first = line[col]
                        if line[0] == parts[3]:
                            third = line[col]
                        if line[0] == parts[5]:
                            fifth = line[col]

                    item['tag'] = item['tag'].replace(parts[1], first)
                    item['tag'] = item['tag'].replace(parts[3], third)
                    item['tag'] = item['tag'].replace(parts[5], fifth)
                    item['tag'] = item['tag'].replace("@","")

    def toggleShow(self):
        self.show = not self.show

    def checkFormat(self, item):
        tmp = item['tag'].split("@")

        if tmp[1] != 'General_St.':
            return False

        if tmp[2].find(item['screen'][2:5]) == -1:
            if item['screen'][2:5] != "ner" and tmp[2].find("000") == -1:
                return False

        if tmp[2][-1] != ' ':
            return False

        if item['type'] == "z_Table_CellInput":
            if not self.checkFormatTable(item):
                return False



        return True


    def checkFormatTable(self, item):
        tmp = item['tag'].split("@")

        root = self.XMLTree.getroot()
        for screen in root.iter("Picture"):
            if str(screen.attrib).find(item['screen']) != -1:
                for i in range(25):
                    for element in screen.iter("Elements_"+str(i)):
                        link = element.findall("LinkName")
                        if len(link) == 1:
                            link = link[0]
                            if link.text == "z_Table_Label":
                                prop = element.findall("ExpProps_0")[0]
                                value = prop.findall("ExpPropValue")[0].text
                                if value.find(tmp[3]) == -1:
                                    return False
        return True

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
        if x == '0':
            return '0'
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
        if x == '0':
            return '0'
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
            elif not self.items[index.row()]['format'] and self.show:
                return QBrush(Qt.yellow)
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
            QMessageBox.warning(self.masterView,"Error:","Only the values A, B, C, D, E or 0 are allowed.", QMessageBox.Ok)
            return False


        if index.column() == 1:
            if undo:
                self.items[index.row()]['changed'] = False
            elif self.items[index.row()]['plvl'] != value:
                self.items[index.row()]['changed'] = True
                self.changes.append({'index' : index, 'before' : self.flipI(self.items[index.row()]['plvl']), 'after' : self.flipI(value)})

            self.items[index.row()]['plvl'] = value
            for j in range(100):
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
