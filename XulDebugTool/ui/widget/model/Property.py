import weakref

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QComboBox


class Property(object):
    def __init__(self, key, obj=None, parent=None):
        self.key = key
        if obj is not None:
            self.ref = weakref.ref(obj)
        self.parent = parent
        self.children = []

        if parent is not None:
            parent.addChild(self)

    def isValid(self):
        return False

    def addChild(self, child):
        self.children.append(child)

    def key(self):
        return self.key

    def value(self):
        return getattr(self.ref(), self.key)

    def setValue(self, value):
        setattr(self.ref(), self.key, value)

    def childCount(self):
        return len(self.children)

    def child(self, row=None):
        if row is not None:
            return self.children[row]
        else:
            return self.children

    def parent(self):
        return self.parent

    def row(self):
        if self.parent is not None:
            return self.parent().child().index(self)

    def createEditor(self, parent, option, index):
        raise NotImplementedError

    def setEditorData(self, editor, data):
        raise NotImplementedError

    def editorData(self, editor):
        raise NotImplementedError


class ListProperty(Property):
    def __init__(self, name, propertyList, parent=None):
        super(ListProperty, self).__init__(name, None, parent)
        self._list = []
        for i, item in enumerate(propertyList):
            self._list.append(Property(str(i), item, self))


class ColorProperty(Property):
    def __init__(self, name, property, parent=None):
        super(ColorProperty, self).__init__(name, property, parent)

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.currentIndexChanged.connect(editor.clearFocus)

        colorNames = QColor().colorNames()

        for i in range(len(colorNames)):
            color = QColor(colorNames[i])
            editor.insertItem(i, colorNames[i])
            editor.setItemData(i, color, Qt.DecorationRole)

        return editor

    def setEditorData(self, editor, data):
        color = data.internalPointer().property()
        editor.setCurrentIndex(editor.findData(color, QtCore.Qt.DecorationRole))
        if editor.currentIndex() == -1:
            editor.addItem(color.name())
            editor.setItemData(editor.count() - 1, color, QtCore.Qt.DecorationRole)
            editor.setCurrentIndex(editor.count() - 1)

    def setModelData(self, editor, model, index):
        item = index.internalPointer()
        color = editor.itemData(editor.currentIndex(), QtCore.Qt.DecorationRole).toPyObject()

        item.setProperty(color)


class DictProperty(Property):
    def __init__(self, name, propertyDict, parent=None):
        super(DictProperty, self).__init__(name, None, parent)
        for i, j in propertyDict.items():
            parent = Property(str(i), j, self)
