#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib3
from PyQt5.QtCore import Qt, QAbstractItemModel, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

from XulDebugTool.utils.XulDebugServerHelper import XulDebugServerHelper

# 数据的整理，需要把数据填充至内显示
LABEL_ATTR = {'x': '', 'y': '', 'width': '', 'height': '', 'text': '', 'img.0': ''}
LABEL_STYLE = {'font-size': '', 'font-color': '', 'font-align': '', 'border': '', 'background-color': ''}


class UpdateElement(QTreeWidget):
    updateSignal = pyqtSignal(str)
    def __init__(self, parent=None):
        super(UpdateElement, self).__init__(parent)
        self.data = None
        self.viewId = ''
        self.viewType = 'label'

        self.inputWidget = QTreeWidget(self)
        self.inputWidget.setFixedHeight(570)
        self.inputWidget.setFixedWidth(350)
        self.inputWidget.setHeaderLabels(['Key', 'Value'])

        self.inputAttr = QTreeWidgetItem()
        self.inputAttr.setText(0, 'Attr')
        self.inputAttr.setBackground(0, QColor(127, 255, 212))
        self.inputAttr.setBackground(1, QColor(127, 255, 212))
        self.inputStyle = QTreeWidgetItem()
        self.inputStyle.setText(0, 'Style')
        self.inputStyle.setBackground(0, QColor(150, 255, 200))
        self.inputStyle.setBackground(1, QColor(150, 255, 200))
        self.inputClass = QTreeWidgetItem()
        self.inputClass.setText(0, 'Class')
        self.inputClass.setBackground(0, QColor(180, 255, 180))
        self.inputClass.setBackground(1, QColor(180, 255, 180))
        self.inputWidget.insertTopLevelItem(0, self.inputAttr)
        self.inputWidget.insertTopLevelItem(1, self.inputStyle)
        self.inputWidget.insertTopLevelItem(2, self.inputClass)

    def updateUrl(self, key=None, value=None):
        r = XulDebugServerHelper.updateUrl(self.viewType, self.viewId, key, value)

    def updateUI(self, idStr=None, type=None):
        self.viewId = idStr
        self.viewType = type

        for key, value in LABEL_ATTR.items():
            item = QTreeWidgetItem()
            item.setText(0, key)
            item.setText(1, value)
            self.inputWidget.itemChanged.connect(lambda: self.updateUrl(key, value))
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsUserCheckable)
            self.inputAttr.addChild(item)

        for key, value in LABEL_STYLE.items():
            item = QTreeWidgetItem()
            item.setText(0, key)
            item.setText(1, value)
            self.inputWidget.itemChanged.connect(lambda: self.updateUrl(key, value))
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsUserCheckable)
            self.inputStyle.addChild(item)

        self.updateSignal.emit(self.viewId)
