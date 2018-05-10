#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/13 17:10
# @Author  : Mrlsm -- starcor

import json

from PyQt5.QtCore import Qt, QStringListModel, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

from XulDebugTool.logcatapi.Logcat import STCLogger
from XulDebugTool.utils.IconTool import IconTool
from XulDebugTool.utils.Utils import Utils
from XulDebugTool.utils.XulDebugServerHelper import XulDebugServerHelper

# 数据的整理，需要把数据填充至内显示
ITEM_ATTR = {}
ITEM_STYLE = {}
ITEM_CLASS = []
ITEM_EVENT = []

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

item_color = QColor(233, 233, 233)
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
        self.pageId = ''
        self.inputWidget = QTreeWidget(self)
        self.inputWidget.setFixedHeight(Utils.getWindowHeight())
        self.inputWidget.setFixedWidth(Utils.getWindowWidth())
        self.inputWidget.setStyleSheet("QTreeWidget::item{height:"+str(Utils.getItemHeight())+"px}")

        self.inputWidget.setHeaderLabels(['Key', 'Value'])

        self.inputAttr = QTreeWidgetItem()
        self.inputAttr.setText(0, 'Attr')
        self.inputAttr.setBackground(0, item_color)
        self.inputAttr.setBackground(1, item_color)
        self.inputStyle = QTreeWidgetItem()
        self.inputStyle.setText(0, 'Style')
        self.inputStyle.setBackground(0, item_color)
        self.inputStyle.setBackground(1, item_color)
        self.inputWidget.insertTopLevelItem(0, self.inputAttr)
        self.inputWidget.insertTopLevelItem(1, self.inputStyle)
        self.inputAttr.setExpanded(True)
        self.inputWidget.expanded.connect(self.changeExpand)
        self.inputWidget.collapsed.connect(self.changeExpand)
        self.initClassBox()

        self.listView = QListView(self)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.slm = QStringListModel()
        self.slm.setStringList(ITEM_EVENT)
        self.listView.setModel(self.slm)
        self.listView.move(30, 150)
        self.listView.resize(300, len(ITEM_EVENT)*Utils.getItemHeight())
        self.listView.clicked.connect(self.itemClickedEvent)
        STCLogger().i('init UpdateProperty')

    def changeExpand(self):
        classHeight = int(3.25*Utils.getItemHeight())
        if self.inputAttr.isExpanded() and self.inputAttr.child(0):
            classHeight = classHeight + (ITEM_ATTR.__len__() + 1) * Utils.getItemHeight()
        if self.inputStyle.isExpanded() and self.inputAttr.child(0):
            classHeight = classHeight + (ITEM_STYLE.__len__() + 1) * Utils.getItemHeight()
        self.ClassBox_1.move(30, classHeight)
        self.ClassBox_2.move(150, classHeight)
        self.listView.move(30, classHeight+Utils.getItemHeight())

    def updateAttrUrl(self):
        num = 0
        for key, value in ITEM_ATTR.items():
            attr = self.inputAttr.child(num).text(1)
            if attr != ITEM_ATTR[self.inputAttr.child(num).text(0)]:
                ITEM_ATTR[key] = attr
                XulDebugServerHelper.updateUrl('set-attr', self.viewId, key, attr)
            num += 1
        self.updateAddProperty('set-attr', num, self.inputAttr)

    def updateStyleUrl(self):
        num2 = 0
        for key, value in ITEM_STYLE.items():
            style = self.inputStyle.child(num2).text(1)
            if style != ITEM_STYLE[self.inputStyle.child(num2).text(0)]:
                ITEM_STYLE[key] = style
                XulDebugServerHelper.updateUrl('set-style', self.viewId, key, style)
            num2 += 1
        self.updateAddProperty('set-style', num2, self.inputStyle)

    def updateAddProperty(self, type, num, root):
        if root.child(num) is None:
            return
        item = root.child(num)
        if str(item.text(0)) == '' or str(item.text(1)) == '':
            return
        if type == 'set-attr':
            for key, value in ITEM_ATTR.items():
                if (key == str(item.text(0)) or str(item.text(0)) not in ATTR_AREA) and not str(item.text(0)).startswith("img"):
                    if str(item.text(0)) in STYLE_AREA:
                        QMessageBox.critical(self, "提示", self.tr("您输入的为style属性，请在style栏内输入。"))
                    item.setText(0, '')
                    item.setText(1, '')
                    return
            ITEM_ATTR.setdefault(str(item.text(0)), str(item.text(1)))
        elif type == 'set-style':
            for key, value in ITEM_STYLE.items():
                if key == str(item.text(0)) or str(item.text(0)) not in STYLE_AREA:
                    if str(item.text(0)) in ATTR_AREA:
                        QMessageBox.critical(self, "提示", self.tr("您输入的为attr属性，请在attr栏内输入。"))
                    item.setText(0, '')
                    item.setText(1, '')
                    return
            ITEM_STYLE.setdefault(str(item.text(0)), str(item.text(1)))

        result = XulDebugServerHelper.updateUrl(type, self.viewId, item.text(0), item.text(1))
        if result is None or result.status != 200:
            return
        STCLogger().i('updateAddProperty:'+item.text(0)+','+item.text(1))
        self.addQTreeWidgetItem(root)

    def updateItemUI(self):
        if self.sameFlag:
            return
        for pos1, item1 in enumerate(ITEM_ATTR.items()):
            item = self.getQTreeWidgetItem(pos1, item1[0], item1[1])
            self.inputAttr.addChild(item)
        for pos2, item2 in enumerate(ITEM_STYLE.items()):
            item = self.getQTreeWidgetItem(pos2, item2[0], item2[1])
            self.inputStyle.addChild(item)
        if self.viewTag in ITEM_TAG:
            self.addQTreeWidgetItem(self.inputAttr)
            self.addQTreeWidgetItem(self.inputStyle)

        self.inputWidget.itemChanged.connect(self.updateAttrUrl)
        self.inputWidget.itemChanged.connect(self.updateStyleUrl)
        self.changeExpand()

        self.slm.setStringList(ITEM_EVENT)
        self.listView.setModel(self.slm)
        self.listView.resize(300, len(ITEM_EVENT)*30)

    def itemClickedEvent(self, qModelIndex):
        print("click " + ITEM_EVENT[qModelIndex.row()])
        XulDebugServerHelper.fireItemEvent(ITEM_EVENT[qModelIndex.row()], self.viewId)

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
        self.changeExpand()

    def initData(self, pageId, data):
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
            ITEM_EVENT.clear()
            for item in children:
                if item.attrib is not None:
                    if item.tag == 'attr':
                        ITEM_ATTR.setdefault(item.attrib['name'], item.text)
                    if item.tag == 'style':
                        ITEM_STYLE.setdefault(item.attrib['name'], item.text)
                    if item.tag == 'action':
                        ITEM_EVENT.append(item.attrib['action'])
        self.initPageClassData(pageId)

    def initClassBox(self):
        self.ClassBox_1 = QComboBox(self)
        self.ClassBox_1.setEditable(False)
        self.ClassBox_1.setMaxVisibleItems(2)
        self.ClassBox_1.setInsertPolicy(QComboBox.InsertAtTop)
        self.ClassBox_1.addItem("add-class")
        self.ClassBox_1.addItem("remove-class")
        self.ClassBox_1.move(30, int(3.25*Utils.getItemHeight()))
        self.ClassBox_1.resize(150, 30)

        self.ClassBox_2 = QComboBox(self)
        self.ClassBox_2.setEditable(False)
        self.ClassBox_2.move(150, int(3.25*Utils.getItemHeight()))
        self.ClassBox_2.resize(200, 30)
        self.ClassBox_2.activated.connect(self.updateClass)
        ITEM_CLASS.clear()
        self.initAllClassData()

    def initAllClassData(self):
        all = XulDebugServerHelper.getAllSelector()
        if all.data:
            selector = Utils.xml2json(all.data, 'selector')
            if selector == '':
                return
            for select in selector['select']:
                if '@class' in select.keys() and select['@class'] not in ITEM_CLASS:
                    ITEM_CLASS.append(select['@class'])

    def initPageClassData(self, pageId):
        if self.pageId == pageId:
            return
        all = XulDebugServerHelper.getPageSelector(pageId)
        if all.data:
            page = Utils.xml2json(all.data, 'page')
            if page == '':
                return
            for item in page:
                if item == 'selector':
                    selector = page['selector']
                    if selector is None or 'select' not in selector.keys():
                        return
                    for select in selector['select']:
                        if '@class' in select.keys() and select['@class'] not in ITEM_CLASS:
                            ITEM_CLASS.append(select['@class'])

        for name in ITEM_CLASS:
            self.ClassBox_2.addItem(name)

    def updateClass(self):
        XulDebugServerHelper.updateClassUrl(self.ClassBox_1.currentText(), self.viewId, self.ClassBox_2.currentText())
