#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTreeView
from XulDebugTool.ui.widget.model.PropertyModel import PropertyModel


class PropertyEditor(QTreeView):
    def __init__(self, parent=None):
        super(PropertyEditor, self).__init__(parent)
        self.model = PropertyModel(self)
        self.setModel(self.model)

    def addProperty(self, p):
        self.model.addProperty(p)
        self.expandToDepth(0)

    def setProperty(self, p):
        self.model.clear()
        if p:
            self.model.addItem(p)
        self.expandToDepth(0)
