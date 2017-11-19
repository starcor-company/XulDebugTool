#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/13 17:10
# @Author  : Mrlsm -- starcor

import json

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

from XulDebugTool.utils.Utils import Utils

# 数据的整理，需要把数据填充至内显示
from XulDebugTool.utils.XulDebugServerHelper import XulDebugServerHelper

ITEM_ATTR = {}
ITEM_STYLE = {}


class UpdateElement(QTreeWidget):
    def __init__(self, parent=None):
        super(UpdateElement, self).__init__(parent)
        self.data = None
        self.viewId = ''
        self.sameFlag = True
        self.inputWidget = QTreeWidget(self)
        self.inputWidget.setFixedHeight(570)
        self.inputWidget.setFixedWidth(350)
        self.inputWidget.setHeaderLabels(['Key', 'Value'])

        self.inputAttr = QTreeWidgetItem()
        self.inputAttr.setText(0, 'Attr')
        self.inputAttr.setBackground(0, QColor(127, 255, 212))
        self.inputAttr.setBackground(1, QColor(127, 255, 212))
        self.inputAttr.setSelected(True)
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

    def updateUrl(self, type=None, data=None):
        num = 0
        for key, value in data.items():
            if type == 'set-attr':
                attr = self.inputAttr.child(num).text(1)
                print(attr)
                XulDebugServerHelper.updateUrl(type, self.viewId, key, attr)
            elif type == 'set-style':
                style = self.inputStyle.child(num).text(1)
                XulDebugServerHelper.updateUrl(type, self.viewId, key, style)
            num += 1

    def updateAttrUI(self):
        if self.sameFlag == True:
            return
        for key, value in ITEM_ATTR.items():
            item = QTreeWidgetItem()
            item.setText(0, key)
            item.setText(1, value)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsUserCheckable)
            self.inputAttr.addChild(item)

        self.inputWidget.itemChanged.connect(lambda: self.updateUrl('set-attr', ITEM_ATTR))

    def updateStyleUI(self):
        if self.sameFlag == True:
            return
        for key, value in ITEM_STYLE.items():
            item = QTreeWidgetItem()
            item.setText(0, key)
            item.setText(1, value)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsUserCheckable)
            self.inputStyle.addChild(item)

        self.inputWidget.itemChanged.connect(lambda: self.updateUrl('set-attr', ITEM_STYLE))

    def initData(self, data):
        dict = json.loads(data)
        action = dict['action']
        if action == "click":
            id = dict['Id']
            xml = dict['xml']
            if id == self.viewId:
                self.sameFlag = True
            else:
                self.sameFlag = False
                ITEM_STYLE.clear()
                ITEM_ATTR.clear()
                self.inputAttr.takeChildren()
                self.inputStyle.takeChildren()
                self.viewId = id
            element = Utils.findNodeById(id, xml)
            children = element.getchildren()
            for item in children:
                if (item.attrib != None):
                    if item.tag == 'attr':
                        ITEM_ATTR.setdefault(item.attrib['name'], item.text)
                    if item.tag == 'style':
                        ITEM_STYLE.setdefault(item.attrib['name'], item.text)

    def clearWidget(self):
        attrNum = 0
        for key, value in ITEM_ATTR.items():
            self.inputAttr.removeChild(self.inputAttr.child(attrNum))
            attrNum += 1

        styleNum = 0
        for key, value in ITEM_STYLE.items():
            self.inputStyle.removeChild(self.inputStyle.child(styleNum))
            styleNum += 1
