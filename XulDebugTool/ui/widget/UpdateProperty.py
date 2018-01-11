#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/13 17:10
# @Author  : Mrlsm -- starcor

import json

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

from XulDebugTool.logcatapi.Logcat import STCLogger
from XulDebugTool.utils.IconTool import IconTool
from XulDebugTool.utils.Utils import Utils
from XulDebugTool.utils.XulDebugServerHelper import XulDebugServerHelper

# 数据的整理，需要把数据填充至内显示
ITEM_ATTR = {}
ITEM_STYLE = {}

ITEM_TAG = ['area', 'item', 'layout']
ATTR_AREA = ["x", "y", "height", "width", "align", "max-layers", "enabled", "animation", "animation-speed",
             "animation-type", "animation-duration", "animation-mode", "switching-mode", "animation-sizing",
             "animation-moving", "direction", "loop", "lock-focus", "component", "text", "multi-line", "auto-wrap",
             "marquee", "ellipsis", "indicator", "indicator.style", "indicator.align", "indicator.gap",
             "indicator.left", "indicator.right", "indicator.top", "indicator.bottom", "scrollbar", "auto-scroll",
             "incremental", "arrangement", "minimum-item", "cache-pages", "checked-class", "group"]

STYLE_AREA = ["font-face", "font-size", "font-color", "font-weight", "font-scale-x", "font-shadow",
              "font-align", "font-style-underline", "font-style-strike", "font-style-italic",
              "font-resample", "font-render", "start-indent", "end-indent", "do-not-match-text",
              "background-image", "background-color", "border", "margin", "margin-left", "margin-right",
              "margin-bottom", "margin-top", "padding", "padding-left", "padding-right", "padding-bottom",
              "padding-top", "display", "z-index", "scale", "animation-scale", "position", "border-dash-pattern",
              "fix-half-char", "animation-text-change", "preferred-focus-padding", "hint-text-color", "line-height",
              "clip-children", "clip-focus", "layout-mode", "opacity", "translate", "translate-x", "translate-y",
              "rotate", "quiver", "quiver-mode", "rotate-x", "rotate-y", "rotate-z", "rotate-center", "rotate-center-x",
              "rotate-center-y", "rotate-center-z", "lighting-color-filter", "round-rect", "max-width", "max-height",
              "min-width", "min-height", "preload", "keep-focus-visible"]

item_color = QColor(255, 255, 255)
property_color_one = QColor(255, 255, 255)
property_color_two = QColor(255, 255, 255)
add_color = QColor(255, 255, 255)


class UpdateProperty(QTreeWidget):
    def __init__(self, parent=None):
        super(UpdateProperty, self).__init__(parent)
        self.data = None
        self.viewId = ''
        self.sameFlag = True
        self.viewTag = ''
        self.inputWidget = QTreeWidget(self)
        self.inputWidget.setFixedHeight(900)
        self.inputWidget.setFixedWidth(420)
        self.inputWidget.setHeaderLabels(['Key', 'Value'])

        self.inputAttr = QTreeWidgetItem()
        self.inputAttr.setText(0, 'Attr')
        self.inputAttr.setBackground(0, item_color)
        self.inputAttr.setBackground(1, item_color)
        self.inputAttr.setSelected(True)
        self.inputStyle = QTreeWidgetItem()
        self.inputStyle.setText(0, 'Style')
        self.inputStyle.setBackground(0, item_color)
        self.inputStyle.setBackground(1, item_color)
        # self.inputClass = QTreeWidgetItem()
        # self.inputClass.setText(0, 'Class')
        # self.inputClass.setBackground(0, item_color)
        # self.inputClass.setBackground(1, item_color)
        self.inputWidget.insertTopLevelItem(0, self.inputAttr)
        self.inputWidget.insertTopLevelItem(1, self.inputStyle)
        # self.inputWidget.insertTopLevelItem(2, self.inputClass)
        STCLogger().i('init UpdateProperty')

    def updateUrl(self, type=None, data=None):
        num = 0
        for key, value in data.items():
            if type == 'set-attr':
                attr = self.inputAttr.child(num).text(1)
                if attr != data[self.inputAttr.child(num).text(0)]:
                    XulDebugServerHelper.updateUrl(type, self.viewId, key, attr)
            elif type == 'set-style':
                style = self.inputStyle.child(num).text(1)
                if style != data[self.inputStyle.child(num).text(0)]:
                    XulDebugServerHelper.updateUrl(type, self.viewId, key, style)
            num += 1
        if num < 1:
            return

        if type == 'set-attr':
            self.updateAddProperty(type, num, self.inputAttr)
        elif type == 'set-style':
            self.updateAddProperty(type, num, self.inputStyle)

    def updateAddProperty(self, type, num, root):
        if root.child(num) is None:
            return
        item = root.child(num)
        if str(item.text(0)) == '' or str(item.text(1)) == '':
            return
        if type == 'set-attr':
            for key, value in ITEM_ATTR.items():
                if key == str(item.text(0)) or str(item.text(0)) not in ATTR_AREA:
                    item.setText(0, '')
                    item.setText(1, '')
                    return
            ITEM_ATTR.setdefault(str(item.text(0)), str(item.text(1)))
        elif type == 'set-style':
            for key, value in ITEM_STYLE.items():
                if key == str(item.text(0)) or str(item.text(0)) not in STYLE_AREA:
                    item.setText(0, '')
                    item.setText(1, '')
                    return
            ITEM_STYLE.setdefault(str(item.text(0)), str(item.text(1)))

        result = XulDebugServerHelper.updateUrl(type, self.viewId, item.text(0), item.text(1))
        if result is None or result.status != 200:
            return
        STCLogger().i('updateAddProperty:'+item.text(0)+','+item.text(1))
        self.addQTreeWidgetItem(root)

    def updateAttrUI(self):
        if self.sameFlag:
            return
        pos = 0
        for key, value in ITEM_ATTR.items():
            item = self.getQTreeWidgetItem(pos, key, value)
            self.inputAttr.addChild(item)
            pos += 1
        if self.viewTag in ITEM_TAG:
            self.addQTreeWidgetItem(self.inputAttr)
        self.inputWidget.itemChanged.connect(lambda: self.updateUrl('set-attr', ITEM_ATTR))

    def updateStyleUI(self):
        if self.sameFlag:
            return
        pos = 0
        for key, value in ITEM_STYLE.items():
            item = self.getQTreeWidgetItem(pos, key, value)
            self.inputStyle.addChild(item)
            pos += 1
        if self.viewTag in ITEM_TAG:
            self.addQTreeWidgetItem(self.inputStyle)
        self.inputWidget.itemChanged.connect(lambda: self.updateUrl('set-style', ITEM_STYLE))

    def getQTreeWidgetItem(self, pos, key, value):
        item = QTreeWidgetItem()
        item.setText(0, key)
        item.setText(1, value)
        if pos % 2 == 1:
            item.setBackground(0, property_color_one)
            item.setBackground(1, property_color_one)
        else:
            item.setBackground(0, property_color_two)
            item.setBackground(1, property_color_two)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsUserCheckable)
        return item

    def addQTreeWidgetItem(self, root):
        addItem = QTreeWidgetItem()
        addItem.setIcon(0, IconTool.buildQIcon('add.png'))
        addItem.setText(0, '')
        addItem.setText(1, '')
        addItem.setBackground(0, add_color)
        addItem.setBackground(1, add_color)
        addItem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
        root.addChild(addItem)

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
            self.viewTag = element.tag
            children = element.getchildren()
            for item in children:
                if item.attrib is not None:
                    if item.tag == 'attr':
                        ITEM_ATTR.setdefault(item.attrib['name'], item.text)
                    if item.tag == 'style':
                        ITEM_STYLE.setdefault(item.attrib['name'], item.text)
