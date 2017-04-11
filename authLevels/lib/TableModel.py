from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QMessageBox, QProgressDialog, QApplication
from datetime import datetime
from math import sqrt
import csv
import chardet

import xml.etree.ElementTree as ET

MAX_ELEMENTS = 150
MAX_EXPPROPS = 20

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

            badScreens = ["Kopie", "z_", "p_", "_Popup"]
            bad = False
            for bS in badScreens:
                if str(screen.attrib).find(bS) != -1:
                    bad = True
            if bad:
                continue

            for i in range(MAX_ELEMENTS):
                for element in screen.iter("Elements_"+str(i)):

                    item = {}

                    item['tag'] = self.searchElement(element, "Variable")

                    if item['tag']:
                        item['plvl'] = self.searchElement(element, "Passwordlevel")
                        item['type'] = self.searchElement(element, "Type")
                        item['changed'] = False
                        item['name'] = element.findall("Name")[0].text
                        item['element'] = element
                        tmp = str(screen.attrib)
                        item['screen'] = tmp[tmp.find(":")+3:-2]
                        item['screenElement'] =  screen
                        item['desired'] = ''

                        self.items.append(item)

    def searchElement(self, element, tag):
        if tag == "Text":
            for j in range(MAX_EXPPROPS):
                for prop in element.iter("ExpProps_"+str(j)):
                    var = prop.findall("Name")[0].text
                    find = var.find(tag)

                    if find != -1:
                        xmlTag = "<Text>"

                        sTag = xmlTag
                        nTag = sTag[:-1] + "/" + sTag[-1]

                        tmp = prop.findall("ExpPropValue")[0].text

                        if tmp.find(nTag) != -1:
                            continue
                        else:
                            eTag = sTag[0] + "/" + sTag[1:]
                            tmp = tmp[tmp.find(sTag)+len(sTag):tmp.find(eTag)]
                            return tmp

        elif tag == "VariableLink":
            for j in range(MAX_EXPPROPS):
                for prop in element.iter("ExpProps_"+str(j)):
                    var = prop.findall("Name")[0].text
                    tag = "Variable"
                    find = var.find(tag)

                    if find != -1:
                        xmlTag = "0..TmpHmi"

                        tmp = prop.findall("ExpPropValue")[0].text

                        if tmp.find(xmlTag) == -1:
                            continue
                        else:
                            s = tmp.find(">") + 1
                            e = tmp.find("<")
                            n = 2
                            while e >= 0 and n > 1:
                                e = tmp.find("<", e+len("<"))
                                n -= 1
                            tmp = tmp[s:e]
                            return tmp

        else:
            for text in self.search:
                link = element.findall("LinkName")
                if len(link) != 0:
                    if link[0].text == text:
                        if tag == "Type":
                            return text
                        for j in range(MAX_EXPPROPS):
                            for prop in element.iter("ExpProps_"+str(j)):
                                var = prop.findall("Name")[0].text
                                find = var.find(tag)

                                if find != -1:
                                    if tag == "Passwordlevel":
                                        xmlTag = "<Passwordlevel>"
                                    else:
                                        xmlTag = "<SymVarTagNr>"

                                    sTag = xmlTag
                                    nTag = sTag[:-1] + "/" + sTag[-1]

                                    tmp = prop.findall("ExpPropValue")[0].text

                                    if tmp.find(nTag) != -1:
                                        continue
                                    else:
                                        eTag = sTag[0] + "/" + sTag[1:]
                                        tmp = tmp[tmp.find(sTag)+len(sTag):tmp.find(eTag)]
                                        return tmp


        return False

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
                if item['desired'] == item['tag']:
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

    def generateFormat(self):

        pb = QProgressDialog("Generating...", "Cancel", 0, len(self.items), self.masterView)
        i = 0
        pb.setValue(i)
        for item in self.items:

            item['desired'] = "@General_St.@"

            item['desired'] += item['screen'][2:5]

            item['desired'] += " "

            tableTypes = ["z_Table_CellInput", "z_Table_CellButtonSwitch", "z_Table_CellSwitch", "z_Table_CellSwitch", "z_Table_CellInputString"]

            if item['type'] in tableTypes:
                item = self.checkFormatTable(item)
            else:
                item = self.checkFormatGroup(item)

            i += 1
            pb.setValue(i)
            QApplication.processEvents()

    def checkFormatGroup(self, item):
        groupBoxes = self.getGroupBoxes(item)

        myxy = self.getXY(item['element'])

        if len(groupBoxes) != 0:
            myGroupBox = groupBoxes[0]

            for groupBox in groupBoxes:
                xy = self.getXY(groupBox)
                if xy[1] < myxy[1] and self.distance(myxy, xy) < self.distance(myxy, self.getXY(myGroupBox)):
                    myGroupBox = groupBox

            text = self.searchElement(myGroupBox, "Text")
            if text[0] == '@' and text[-1] != '@':
                text += '@'

            item['desired'] += text + ': '

            link = self.searchElement(item['element'], "VariableLink")

            item['desired'] += self.findLinkedVar(link)

        return item


    def findLinkedVar(self, link):
        root = self.XMLTree.getroot()

        for variable in root.iter("Variable"):
            if str(variable.attrib).find(str(link)) != -1:
                return variable.findall("Recourceslabel")[0].text

        return "not found"

    def distance(self, xy1, xy2):
        return sqrt((xy2[0] - xy1[0])**2 + (xy2[1] - xy1[1])**2)

    def getXY(self, element):
        x = int(element.findall("StartX")[0].text)
        y = int(element.findall("StartY")[0].text)
        return (x,y)

    def getGroupBoxes(self, item):
        groupBoxes = []
        for i in range(MAX_ELEMENTS):
            for element in item['screenElement'].iter("Elements_"+str(i)):
                link = element.findall("LinkName")
                if len(link) != 0:
                    link = link[0]
                    if link.text == "z_GroupBox":
                        groupBoxes.append(element)

        return groupBoxes

    def checkFormatTable(self, item):

        desired = [' ',' ',' ']

        for i in range(MAX_ELEMENTS):
            for element in item['screenElement'].iter("Elements_"+str(i)):
                link = element.findall("LinkName")
                if len(link) != 0:
                    link = link[0]
                    if link.text == "z_Table_Label":
                        name = element.findall("Name")[0].text.split("_")
                        itemName = item['name'].split("_")

                        if len(itemName) == 3 and len(name) == 2:
                            if itemName[0] == name[0]:
                                desired[0] = self.getValue(element)

                        if len(itemName) == 4 and len(name) == 3:
                            if itemName[0] == name[0] and itemName[-1] == name[-1]:
                                desired[0] = self.getValue(element)

                    elif link.text == "z_Table_RowHeader":
                        name = element.findall("Name")[0].text.split("_")
                        itemName = item['name'].split("_")

                        if len(itemName) == 3 and len(name) == 3:
                            if itemName[0] == name[0] and itemName[1] == name[1]:
                                desired[1] = self.getValue(element)

                        if len(itemName) == 4 and len(name) == 4:
                            if itemName[0] == name[0] and itemName[-1] == name[-1] and itemName[1] == name[1]:
                                desired[1] = self.getValue(element)

                    elif link.text == "z_Table_ColumnHeader":
                        name = element.findall("Name")[0].text.split("_")
                        itemName = item['name'].split("_")

                        if len(itemName) == 3 and len(name) == 2:
                            if itemName[0] == name[0] and itemName[2][-1] == name[1][-1]:
                                desired[2] = self.getValue(element)

                        if len(itemName) == 4 and len(name) == 3:
                            if itemName[0] == name[0] and itemName[-1] == name[-1] and itemName[2][-1] == name[1][-1]:
                                desired[2] = self.getValue(element)

        for i in range(len(desired)-1):
            if desired[i][0] != '@' and desired[i][-1] != '@':
                desired[i] = '@' + desired[i] + '@'
            if desired[i][0] == '@' and desired[i][-1] != '@':
                desired[i] += '@'

        desired[0] += ": "
        desired[1] += " "

        item['desired'] += ''.join(desired)

        return item

    def getValue(self, element):
        prop = element.findall("ExpProps_0")[0]
        value = prop.findall("ExpPropValue")[0].text
        value = value.replace("<Text>","")
        value = value.replace("</Text>","")
        return value

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
        return 4

    def rowCount(self, parent):
        return len(self.items)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return "Tag"
            elif section == 1:
                return "Password Level"
            elif section == 2:
                return "Screen"
            else:
                return "Standard"

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
            if self.items[row]['changed']:
                return QBrush(Qt.red)
            elif self.items[row]['desired'] != self.items[row]['tag'] and self.show:
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
        elif column == 3:
            return QVariant(self.items[row]['desired'])

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
