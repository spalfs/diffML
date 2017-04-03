from lib.CONSTANTS import NONE

class TreeItem(object):
    def __init__(self, data, parent=None, depth=0):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []
        self.depth = depth
        self.colorState = NONE
        self.changed = False

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def setData(self, data, column):
        tmp = list(self.itemData)
        if tmp[column] != data:
            self.changed = True
            tmp[column] = data
            self.itemData = tuple(tmp)

    def resetChanged(self):
        self.changed = False

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

    def setColorState(self,state):
        self.colorState = state
