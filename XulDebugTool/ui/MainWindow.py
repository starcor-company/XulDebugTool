#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
XulDebugTool

主页面

author: Kenshin
last edited: 2017.10.23
"""

from XulDebugTool.ui.BaseWindow import BaseWindow
from XulDebugTool.ui.widget.PropertyEditor import PropertyEditor
from XulDebugTool.ui.widget.SearchBarQLineEdit import SearchBarQLineEdit
from XulDebugTool.utils.IconTool import IconTool
from XulDebugTool.utils.Utils import Utils
from XulDebugTool.utils.XulDebugServerHelper import XulDebugServerHelper
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

import pyperclip

ROOT_ITEM_PAGE = 'Page'
ROOT_ITEM_USER_OBJECT = 'User-Object'
ROOT_ITEM_PLUGIN = 'Plugin'
CHILD_ITEM_DATA_SERVICE = 'DataService'

# Model树第一层的节点类型
ITEM_TYPE_PAGE_ROOT = 'pageRoot'
ITEM_TYPE_USER_OBJECT_ROOT = 'userObjectRoot'
ITEM_TYPE_PLUGIN_ROOT = 'pluginRoot'

# Model树第二层的节点类型
ITEM_TYPE_PAGE = 'page'
ITEM_TYPE_USER_OBJECT = 'userObject'

# Model树第二层的节点类型
ITEM_TYPE_PROVIDER = 'provider'


class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.qObject = QObject()
        self.initUI()
        self.show()

    def initUI(self):
        self.resize(1400, 800)
        self.initMenuBar()
        self.initLayout()
        super().initWindow()

    def initMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')
        disConnectAction = QAction(IconTool.buildQIcon('disconnect.png'), 'Disconnect', self)
        disConnectAction.setShortcut('Ctrl+D')
        settingAction = QAction(IconTool.buildQIcon('setting.png'), 'Setting...', self)
        settingAction.setShortcut('Ctrl+Shift+S')
        showLogAction = QAction('Show Log', self)
        fileMenu.addAction(disConnectAction)
        fileMenu.addAction(settingAction)
        fileMenu.addAction(showLogAction)

        editMenu = menuBar.addMenu('Edit')
        findAction = QAction(IconTool.buildQIcon('find.png'), 'Find', self)
        findAction.setShortcut('Ctrl+F')
        editMenu.addAction(findAction)

        helpMenu = menuBar.addMenu('Help')
        aboutAction = QAction(IconTool.buildQIcon('about.png'), 'About', self)
        helpMenu.addAction(aboutAction)

    def initLayout(self):
        # ----------------------------left layout---------------------------- #
        self.treeModel = QStandardItemModel()
        self.pageItem = QStandardItem(ROOT_ITEM_PAGE)
        self.pageItem.type = ITEM_TYPE_PAGE_ROOT
        self.buildPageItem()
        self.userobjectItem = QStandardItem(ROOT_ITEM_USER_OBJECT)
        self.userobjectItem.type = ITEM_TYPE_USER_OBJECT_ROOT
        self.buildUserObjectItem()
        self.pluginItem = QStandardItem(ROOT_ITEM_PLUGIN)
        self.pluginItem.type = ITEM_TYPE_PLUGIN_ROOT
        self.treeModel.appendColumn([self.pageItem, self.userobjectItem, self.pluginItem])
        self.treeModel.setHeaderData(0, Qt.Horizontal, 'Model')

        self.treeView = QTreeView()
        self.treeView.setModel(self.treeModel)
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openContextMenu)
        self.treeView.clicked.connect(self.getDebugData)

        leftContainer = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 6, 0)  # left, top, right, bottom
        layout.addWidget(self.treeView)
        leftContainer.setLayout(layout)

        # ----------------------------middle layout---------------------------- #
        middleContainer = QWidget()
        middleContainer.toggleSidebarsButton = QPushButton()
        middleContainer.toggleSidebarsButton.setToolTip('Hide / show the sidebars')
        middleContainer.toggleSidebarsButton.setIcon(IconTool.buildQIcon('toggle_sidebars.png'))
        middleContainer.toggleSidebarsButton.setStyleSheet('QPushButton {\
            width: 22px;\
            height: 22px;\
            padding: 5px; }')
        # middleContainer.toggle_sidebars_button.clicked.connect(self.toggle_sidebars)

        middleContainer.searchBar = SearchBarQLineEdit(self)
        middleContainer.searchBar.setPlaceholderText('Search')
        middleContainer.searchBar.setMaximumWidth(300)
        middleContainer.searchBar.setMaximumHeight(32)
        middleContainer.searchBar.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)

        # search shall start not before the user completed typing
        # filter_delay = DelayedExecutionTimer(self)
        # new_column.search_bar.textEdited[str].connect(filter_delay.trigger)
        # filter_delay.triggered[str].connect(self.search)

        self.tabBar = QTabBar()
        self.tabBar.setUsesScrollButtons(False)
        self.tabBar.setDrawBase(False)
        self.tabBar.addTab('tab1')
        self.tabBar.addTab('tab2')

        self.pathBar = QWidget()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        self.pathBar.setLayout(layout)

        self.searchHolder = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.tabBar)
        layout.addWidget(self.pathBar)
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding))
        layout.addWidget(middleContainer.searchBar)
        layout.addWidget(middleContainer.toggleSidebarsButton)
        layout.setStretchFactor(middleContainer.searchBar, 1)
        self.searchHolder.setLayout(layout)
        self.searchHolder.layout().setContentsMargins(6, 6, 6, 0)

        middleContainer.stackedWidget = QStackedWidget()
        self.browser = QWebEngineView()
        self.showXulDebugData(XulDebugServerHelper.HOST + 'list-pages')
        middleContainer.stackedWidget.addWidget(self.browser)
        middleContainer.stackedWidget.addWidget(QLabel('tab2 content'))

        self.tabBar.currentChanged.connect(lambda: middleContainer.stackedWidget.setCurrentIndex(
            self.tabBar.currentIndex()
        ))

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.searchHolder)
        layout.addWidget(middleContainer.stackedWidget)
        middleContainer.setLayout(layout)

        # ----------------------------right layout---------------------------- #

        self.propertyEditor = PropertyEditor(['Key', 'Value'])

        rightContainer = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.propertyEditor)
        rightContainer.setLayout(layout)

        # ----------------------------entire layout---------------------------- #

        self.mainSplitter = QSplitter(Qt.Horizontal)
        self.mainSplitter.setHandleWidth(0)  # thing to grab the splitter

        self.mainSplitter.addWidget(leftContainer)
        self.mainSplitter.addWidget(middleContainer)
        self.mainSplitter.addWidget(rightContainer)
        self.mainSplitter.setStretchFactor(0, 0)
        self.mainSplitter.setStretchFactor(1, 6)
        self.mainSplitter.setStretchFactor(2, 6)

        self.setCentralWidget(self.mainSplitter)

    @pyqtSlot(QPoint)
    def openContextMenu(self, point):
        index = self.treeView.indexAt(point)
        if not index.isValid():
            return
        menu = QMenu()
        copyAction = QAction(IconTool.buildQIcon('copy.png'), 'Copy to Clipboard', self,
                             triggered=lambda: pyperclip.copy('%s' % index.data()))
        menu.addAction(copyAction)
        menu.exec_(self.treeView.viewport().mapToGlobal(point))

    @pyqtSlot(QModelIndex)
    def getDebugData(self, index):
        item = self.treeModel.itemFromIndex(index)

        if item.type == ITEM_TYPE_PAGE_ROOT:  # 树第一层,page节点
            self.buildPageItem()
            self.showXulDebugData(XulDebugServerHelper.HOST + 'list-pages')
        elif item.type == ITEM_TYPE_USER_OBJECT_ROOT:  # 树第一层,userObject节点
            self.buildUserObjectItem()
            self.showXulDebugData(XulDebugServerHelper.HOST + 'list-user-objects')
        elif item.type == ITEM_TYPE_PLUGIN_ROOT:  # 树第一层,plugin节点
            pass
        elif item.type == ITEM_TYPE_PAGE:  # 树第二层,page下的子节点
            pageId = item.id
            self.showXulDebugData(XulDebugServerHelper.HOST + 'get-layout/' + pageId)
        elif item.type == ITEM_TYPE_USER_OBJECT:  # 树第二层,userObject下的子节点
            objectId = item.id
            self.showXulDebugData(XulDebugServerHelper.HOST + 'get-user-object/' + objectId)
        elif item.type == ITEM_TYPE_PROVIDER:  # 树第三层,userObject下的DataService下的子节点
            print(item.id, item.type, item.data)
            pass
        self.fillPropertyEditor(item.data)

    def buildPageItem(self):
        self.pageItem.removeRows(0, self.pageItem.rowCount())
        r = XulDebugServerHelper.listPages()
        if r:
            pagesNodes = Utils.xml2json(r.data, 'pages')
            if pagesNodes == '':
                return
            # 如果只有一个page,转化出来的json不是数据.分开处理
            if isinstance(pagesNodes['page'], list):
                for i, page in enumerate(pagesNodes['page']):
                    # 把page解析了以后放page节点下
                    row = QStandardItem(page['@pageId'])
                    row.id = page['@id']
                    row.data = page
                    row.type = ITEM_TYPE_PAGE
                    self.pageItem.appendRow(row)
            else:
                page = pagesNodes['page']
                row = QStandardItem(page['@pageId'])
                row.id = page['@id']
                row.data = page
                row.type = ITEM_TYPE_PAGE
                self.pageItem.appendRow(row)
            if self.pageItem.rowCount() > 0:
                self.pageItem.setText('%s(%s)' % (ROOT_ITEM_PAGE, self.pageItem.rowCount()))

    def buildUserObjectItem(self):
        self.userobjectItem.removeRows(0, self.userobjectItem.rowCount())
        r = XulDebugServerHelper.listUserObject()
        if r:
            userObjectNodes = Utils.xml2json(r.data, 'objects')
            # 如果只有一个userObject,转化出来的json不是数据.分开处理
            if isinstance(userObjectNodes['object'], list):
                for i, o in enumerate(userObjectNodes['object']):
                    # 把userObject加到User-Object节点下
                    row = QStandardItem(o['@name'])
                    row.id = o['@id']
                    row.data = o
                    row.type = ITEM_TYPE_USER_OBJECT
                    self.userobjectItem.appendRow(row)
                    # 如果是DataServcie, 填充所有的Provider到该节点下
                    if o['@name'] == CHILD_ITEM_DATA_SERVICE:
                        r = XulDebugServerHelper.getUserObject(o['@id'])
                        if r:
                            dataServiceNodes = Utils.xml2json(r.data, 'object')
                            for j, provider in enumerate(dataServiceNodes['object']['provider']):
                                dsRow = QStandardItem(provider['ds']['@providerClass'])
                                dsRow.id = provider['@name']
                                dsRow.data = provider
                                dsRow.type = ITEM_TYPE_PROVIDER
                                row.appendRow(dsRow)
                            # 对Provider按升序排序
                            row.sortChildren(0)
                    if row.rowCount() > 0:
                        row.setText('%s(%s)' % (row.text(), row.rowCount()))
            else:
                # 没有只有一个userObject的情况, 暂不处理
                pass
        if self.userobjectItem.rowCount() > 0:
            self.userobjectItem.setText('%s(%s)' % (ROOT_ITEM_USER_OBJECT, self.userobjectItem.rowCount()))

    def showXulDebugData(self, url):
        self.browser.load(QUrl(url))
        self.statusBar().showMessage(url)

    def fillPropertyEditor(self, data):
        self.propertyEditor.clearProperty()
        self.qObject = QObject()
        if isinstance(data, dict):
            for k, v in data.items():
                setattr(self.qObject, k, v)
        self.propertyEditor.addProperty(self.qObject)
