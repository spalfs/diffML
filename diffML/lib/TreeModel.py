from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex
from PyQt5.QtGui import QBrush, QColor
from ast import literal_eval
import xml.etree.ElementTree as ET

from lib.CONSTANTS import NONE, HIERARCHY, CHANGED
from lib.xmllib import find
from lib.TreeItem import TreeItem

class TreeModel(QAbstractItemModel):
    def __init__(self, path, parent=None):
        super(TreeModel, self).__init__(parent)

        self.rootItem = TreeItem(("Tag", "Text", "Attributes"))
        self.path = path

        self.setupModel()

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == Qt.BackgroundRole:
            if item.colorState == NONE:
                return QBrush(Qt.transparent)
            elif item.colorState == HIERARCHY:
                if item.depth == 0:
                    return QBrush(QColor(157,159,85))
                elif item.depth == 1:
                    return QBrush(QColor(85,157,159))
                elif item.depth == 2:
                    return QBrush(QColor(85,120,159))
                elif item.depth == 3:
                    return QBrush(QColor(159,87,85))
                elif item.depth == 4:
                    return QBrush(QColor(120,159,85))
                elif item.depth == 5:
                    return QBrush(QColor(159,85,120))
            elif item.colorState == CHANGED:
                if item.changed:
                    return QBrush(Qt.red)
                else:
                    return QBrush(Qt.transparent)

        if role == Qt.EditRole:
            return item.data(index.column())

        if role != Qt.DisplayRole:
            return None

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def setData(self, index, value, role):
        try:
            XMLRoot = self.XMLTree.getroot()
            item = index.internalPointer()

            element = find(XMLRoot, item.data(0), item.data(1), item.data(2))

            if index.column() == 0:
                element.tag = value
            elif index.column() == 1:
                element.text = value
            elif index.column() == 2:
                dValue = literal_eval(value)
                for key in dValue:
                    element.set(key,dValue[key])

            item.setData(value,index.column())
            return True

        except:
            return False

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def setupModel(self):
        self.XMLTree = ET.parse(self.path)
        XMLRoot = self.XMLTree.getroot()

        base = TreeItem((self.path,'',''),self.rootItem)
        self.rootItem.appendChild(base)

        self.setupModelRecursive(base,XMLRoot)

    def setupModelRecursive(self, node, XMLNode, depth=0):
        depth = depth + 1
        for element in XMLNode:
            child = TreeItem((str(element.tag),str(element.text),str(element.attrib)), node, depth)
            node.appendChild(child)
            self.setupModelRecursive(child,element,depth)

    def setColor(self, color, node=None):
        if node is None:
            node = self.rootItem
        for i in range(node.childCount()):
            node.child(i).setColorState(color)
            self.setColor(color, node.child(i))

    def getXMLTree(self):
        return self.XMLTree

    def save(self,path=None):
        if path is None:
            path = self.path

        self.resetChanged()
        try:
            self.XMLTree.write(path)
        except:
            print("save error")

    def resetChanged(self, node=None):
        if node is None:
            node = self.rootItem
        for i in range(node.childCount()):
            node.child(i).resetChanged()
            self.resetChanged(node.child(i))


