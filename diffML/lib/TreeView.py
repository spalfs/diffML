from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeView

class TreeView(QTreeView):
    def __init__(self, view):
        super(TreeView, self).__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda : view.rightClickMenu(self))
