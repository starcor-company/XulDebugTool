#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QAbstractItemModel, Qt, QModelIndex
from PyQt5.QtGui import QColor, QPixmap, QIcon

from XulDebugTool.ui.widget.model.Property import Property


class PropertyModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super(PropertyModel, self).__init__(parent)
        self.rootItem = Property('Root', None, None)
        self.items = []

    def getRootItem(self):
        return self.rootItem

    def rowCount(self, parent):
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.column() == 0:
                return item.getKey()
            else:
                return item.getValue()

        if role == Qt.DecorationRole and index.column == 1:
            if isinstance(item.value(), QColor):
                pixmap = QPixmap(26, 26)
                pixmap.fill(item.value())
                icon = QIcon(pixmap)
                return icon

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsUserCheckable

    def getItem(self, index):
        if index.isValid():
            return index.internalPointer()
        else:
            return self.rootItem


    def index(self, row, column, parent=None, *args, **kwargs):
        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)

        if childItem is not None:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        item = self.getItem(index)
        parentItem = item.parent

        if parentItem == self.rootItem:
            return QModelIndex()
        else:
            return self.createIndex(parentItem.row(), 0, parentItem)

    def addProperty(self, p):
        properties = vars(p)
        self.beginInsertRows(QModelIndex(), self.rowCount(self.rootItem), self.rowCount(self.rootItem))

        for k, v in properties.items():
            self.items.append(Property(k, p, self.rootItem))

        self.endInsertRows()

    def clear(self):
        self.beginInsertRows(QModelIndex(), 0, self.rowCount(self.rootItem))
        self.rootItem = Property('Root', None, None)
        self.items = []
        self.endInsertRows()
