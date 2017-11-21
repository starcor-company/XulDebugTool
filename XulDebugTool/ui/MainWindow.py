#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
XulDebugTool

主页面

author: Kenshin
last edited: 2017.10.23
"""
import os

import pyperclip
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineScript
from PyQt5.QtWidgets import *
import json

from XulDebugTool.ui.BaseWindow import BaseWindow
from XulDebugTool.ui.widget.ConsoleView import ConsoleWindow
from XulDebugTool.ui.SettingWindow import SettingWindow
from XulDebugTool.ui.widget.BaseDialog import BaseDialog
from XulDebugTool.ui.widget.ButtomConsoleWindow import ButtomWindow
from XulDebugTool.ui.widget.DataQueryDialog import DataQueryDialog
from XulDebugTool.ui.widget.PropertyEditor import PropertyEditor
from XulDebugTool.ui.widget.SearchBarQLineEdit import SearchBarQLineEdit
from XulDebugTool.ui.widget.UpdateElement import UpdateElement
from XulDebugTool.utils.IconTool import IconTool
from XulDebugTool.utils.Utils import Utils
from XulDebugTool.utils.XulDebugServerHelper import XulDebugServerHelper
from XulDebugTool.webprocess.WebShareObject import WebShareObject

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

#获取元素详情的4个参数
SKIP_PROP = 'skip-prop'
WITH_CHILDREN = 'with-children'
WITH_BINDING_DATA = 'with-binding-data'
WITH_POSITION = 'with-position'

class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.qObject = QObject()
        self.initConsole()
        self.initUI()
        self.show()

    def initConsole(self):
        self.consoleWindow = ButtomWindow()

    def initUI(self):
        self.resize(1400, 800)
        self.initMenuBar()
        self.initLayout()
        super().initWindow()

    def initMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')
        disConnectAction = QAction(IconTool.buildQIcon('disconnect.png'), '&Disconnect', self)
        disConnectAction.setShortcut('Ctrl+D')
        disConnectAction.setShortcutContext(Qt.ApplicationShortcut)
        disConnectAction.triggered.connect(self.restartProgram)
        settingAction = QAction(IconTool.buildQIcon('setting.png'), '&Setting...', self)
        settingAction.setShortcut('Ctrl+Shift+S')
        settingAction.setShortcutContext(Qt.ApplicationShortcut)
        settingAction.triggered.connect(lambda :print('11111'))
        showLogAction = QAction('Show Log', self)
        fileMenu.addAction(disConnectAction)
        # fileMenu.addAction(settingAction)
        # fileMenu.addAction(showLogAction)

        # settingAction.triggered.connect(self.openSettingWindow)

        editMenu = menuBar.addMenu('Edit')
        findAction = QAction(IconTool.buildQIcon('find.png'), '&Find', self)
        findAction.setShortcut('Ctrl+F')
        findAction.setShortcutContext(Qt.ApplicationShortcut)
        findAction.triggered.connect(lambda :print('xxxx'))
        editMenu.addAction(findAction)

        helpMenu = menuBar.addMenu('Help')
        aboutAction = QAction(IconTool.buildQIcon('about.png'), '&About', self)
        helpMenu.addAction(aboutAction)

    def restartProgram(self):
        from XulDebugTool.ui.ConnectWindow import ConnectWindow #不应该在这里导入，但是放在前面会有问题
        print("新建连接页面")
        self.con = ConnectWindow()
        self.close()

    # def openSettingWindow(self):
    #     self.tableInfoModel = SettingWindow()
    #     self.tableInfoModel.show()

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
        self.treeView.doubleClicked.connect(self.onTreeItemDoubleClicked)
        self.treeView.clicked.connect(self.getDebugData)

        leftContainer = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 6, 0)  # left, top, right, bottom
        layout.addWidget(self.treeView)
        leftContainer.setLayout(layout)

        # ----------------------------middle layout---------------------------- #
        middleContainer = QWidget()

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
        layout.setStretchFactor(middleContainer.searchBar, 1)
        self.searchHolder.setLayout(layout)
        self.searchHolder.layout().setContentsMargins(6, 6, 6, 0)

        self.tabContentWidget = QWidget()
        self.browser = QWebEngineView()

        self.channel = QWebChannel()
        self.webObject = WebShareObject()
        self.channel.registerObject('bridge', self.webObject)
        self.browser.page().setWebChannel(self.channel)
        self.webObject.jsCallback.connect(lambda value:self.addUpdate(value))

        qwebchannel_js = QFile(':/qtwebchannel/qwebchannel.js')
        if not qwebchannel_js.open(QIODevice.ReadOnly):
            raise SystemExit(
                'Failed to load qwebchannel.js with error: %s' %
                qwebchannel_js.errorString())
        qwebchannel_js = bytes(qwebchannel_js.readAll()).decode('utf-8')

        script = QWebEngineScript()
        script.setSourceCode(qwebchannel_js)
        script.setInjectionPoint(QWebEngineScript.DocumentCreation)
        script.setName('qtwebchannel.js')
        script.setWorldId(QWebEngineScript.MainWorld)
        script.setRunsOnSubFrames(True)
        self.browser.page().scripts().insert(script)

        Utils.scriptCreator(os.path.join('..', 'resources', 'js', 'event.js'),'event.js',self.browser.page())
        self.browser.page().setWebChannel(self.channel)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.initQCheckBoxUI())
        layout.addWidget(self.browser)
        self.tabContentWidget.setLayout(layout)

        middleContainer.stackedWidget = QStackedWidget()
        self.url = XulDebugServerHelper.HOST + 'list-pages'
        self.showXulDebugData(self.url)
        middleContainer.stackedWidget.addWidget(self.tabContentWidget)
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
        self.rightSiderClickInfo = 'property'

        self.rightSiderTabWidget = QTabWidget()
        self.rightSiderTabBar = QTabBar()
        self.rightSiderTabWidget.setTabBar(self.rightSiderTabBar)
        self.rightSiderTabWidget.setTabPosition(QTabWidget.East)
        self.rightSiderTabWidget.setStyleSheet(('QTab::tab{height:60px;width:20px;color:black;padding:0px}'
                                                'QTabBar::tab:selected{background:lightgray}'))
        self.qtextEdit = QTextEdit()

        self.propertyEditor = PropertyEditor(['Key', 'Value'])
        self.inputWidget = UpdateElement()
        self.rightSiderTabWidget.addTab(self.inputWidget,IconTool.buildQIcon('property.png'),'property')

        self.rightSiderTabWidget.addTab(self.qtextEdit,IconTool.buildQIcon('favorites.png'),'favorites')
        self.rightSiderTabBar.tabBarClicked.connect(self.rightSiderClick)

        # ----------------------------entire layout---------------------------- #

        self.contentSplitter = QSplitter(Qt.Horizontal)
        self.contentSplitter.setHandleWidth(0)  # thing to grab the splitter

        self.contentSplitter.addWidget(leftContainer)
        self.contentSplitter.addWidget(middleContainer)
        self.contentSplitter.addWidget(self.rightSiderTabWidget)
        self.contentSplitter.setStretchFactor(0, 0)
        self.contentSplitter.setStretchFactor(1, 6)
        self.contentSplitter.setStretchFactor(2, 6)

        self.mainSplitter = QSplitter(Qt.Vertical)
        self.mainSplitter.setHandleWidth(0)

        self.mainSplitter.addWidget(self.contentSplitter)
        self.mainSplitter.addWidget(self.consoleWindow)
        self.mainSplitter.setStretchFactor(1, 0)
        self.mainSplitter.setStretchFactor(2,1)
        self.setCentralWidget(self.mainSplitter)
        #默认隐藏掉复选框
        self.groupBox.setHidden(True)

    def addUpdate(self, value=None):
        self.inputWidget.initData(value)
        self.inputWidget.updateAttrUI()
        self.inputWidget.updateStyleUI()

    def initQCheckBoxUI(self):
        self.groupBox = QGroupBox()
        self.skipPropCheckBox = QCheckBox('skip-prop', self)
        self.skipPropCheckBox.setChecked(False)
        self.skipPropCheckBox.stateChanged.connect(self.clickCheckBox)

        self.withChildrenCheckBox = QCheckBox('with-children', self)
        self.withChildrenCheckBox.setChecked(False)
        self.withChildrenCheckBox.stateChanged.connect(self.clickCheckBox)

        self.withBindingDataCheckBox = QCheckBox('with-binding-data', self)
        self.withBindingDataCheckBox.setChecked(False)
        self.withBindingDataCheckBox.stateChanged.connect(self.clickCheckBox)

        self.withPositionCheckBox = QCheckBox('with-position', self)
        self.withPositionCheckBox.setChecked(False)
        self.withPositionCheckBox.stateChanged.connect(self.clickCheckBox)

        checkGrouplayout = QHBoxLayout()
        checkGrouplayout.addWidget(self.skipPropCheckBox)
        checkGrouplayout.setSpacing(10)
        checkGrouplayout.addWidget(self.withChildrenCheckBox)
        checkGrouplayout.setSpacing(10)
        checkGrouplayout.addWidget(self.withBindingDataCheckBox)
        checkGrouplayout.setSpacing(10)
        checkGrouplayout.addWidget(self.withPositionCheckBox)
        checkGrouplayout.addStretch(10)
        self.groupBox.setLayout(checkGrouplayout)
        return self.groupBox

    def clickCheckBox(self):
        if self.skipPropCheckBox.isChecked():
            self.selectCheckBoxInfo(SKIP_PROP)
        else:
            self.cancelCheckBoxInfo(SKIP_PROP)

        if self.withChildrenCheckBox.isChecked():
            self.selectCheckBoxInfo(WITH_CHILDREN)
        else:
            self.cancelCheckBoxInfo(WITH_CHILDREN)

        if self.withBindingDataCheckBox.isChecked():
            self.selectCheckBoxInfo(WITH_BINDING_DATA)
        else:
            self.cancelCheckBoxInfo(WITH_BINDING_DATA)

        if self.withPositionCheckBox.isChecked():
            self.selectCheckBoxInfo(WITH_POSITION)
        else:
            self.cancelCheckBoxInfo(WITH_POSITION)

    def selectCheckBoxInfo(self,str):
        if None != self.url:
            checkedStr = str + '=' + 'true'
            unCheckedStr = str + '=' + 'false'
            if self.url.find('?') == -1:
                self.url += '?'
                self.url += checkedStr
            else:
                if self.url.find(str) == -1:
                    self.url += '&'
                    self.url += checkedStr
                elif self.url.find(unCheckedStr) != -1:
                    self.url=self.url.replace(unCheckedStr,checkedStr)
            self.showXulDebugData(self.url)

    def cancelCheckBoxInfo(self,str):
        if None != self.url:
            checkedStr = str + '=' + 'true'
            if self.url.find(checkedStr) >= -1:
                split = self.url.split(checkedStr)
                self.url=''.join(split)
                self.url = self.url.replace('&&','&')
                self.url = self.url.replace('?&', '?')
                if self.url.endswith('?'):
                    self.url = self.url[:-1]
                if self.url.endswith('&'):
                    self.url = self.url[:-1]
                self.showXulDebugData(self.url)

    def rightSiderClick(self,index):
        #两次单击同一个tabBar时显示隐藏内容区域
        if self.rightSiderTabBar.tabText(index) == self.rightSiderClickInfo:
            if self.rightSiderTabWidget.width() == 32:
                self.rightSiderTabWidget.setMaximumWidth(800)
            else:
                self.rightSiderTabWidget.setFixedWidth(32)
        else:
            if self.rightSiderTabWidget.width() == 32:
                self.rightSiderTabWidget.setMaximumWidth(800)
        self.rightSiderClickInfo = self.rightSiderTabBar.tabText(index)

    @pyqtSlot(QPoint)
    def openContextMenu(self, point):
        index = self.treeView.indexAt(point)
        if not index.isValid():
            return
        item = self.treeModel.itemFromIndex(index)
        menu = QMenu()

        if item.type == ITEM_TYPE_PROVIDER:
            queryAction = QAction(IconTool.buildQIcon('data.png'), '&Query Data...', self,
                                  triggered=lambda: self.showQueryDialog(item.data))
            queryAction.setShortcut('Alt+Q')
            menu.addAction(queryAction)

        copyAction = QAction(IconTool.buildQIcon('copy.png'), '&Copy', self,
                             triggered=lambda: pyperclip.copy('%s' % index.data()))
        copyAction.setShortcut(QKeySequence.Copy)
        menu.addAction(copyAction)
        menu.exec_(self.treeView.viewport().mapToGlobal(point))

    @pyqtSlot(QModelIndex)
    def getDebugData(self, index):
        item = self.treeModel.itemFromIndex(index)

        if item.type == ITEM_TYPE_PAGE_ROOT:  # 树第一层,page节点
            self.buildPageItem()
            self.url = XulDebugServerHelper.HOST + 'list-pages'
            self.showXulDebugData(self.url)
        elif item.type == ITEM_TYPE_USER_OBJECT_ROOT:  # 树第一层,userObject节点
            self.buildUserObjectItem()
            self.url = XulDebugServerHelper.HOST + 'list-user-objects'
            self.showXulDebugData(self.url)
        elif item.type == ITEM_TYPE_PLUGIN_ROOT:  # 树第一层,plugin节点
            pass
        elif item.type == ITEM_TYPE_PAGE:  # 树第二层,page下的子节点
            pageId = item.id
            self.url = XulDebugServerHelper.HOST + 'get-layout/' + pageId
            self.clickCheckBox()
            self.showXulDebugData(self.url)
        elif item.type == ITEM_TYPE_USER_OBJECT:  # 树第二层,userObject下的子节点
            objectId = item.id
            self.url = XulDebugServerHelper.HOST + 'get-user-object/' + objectId
            self.showXulDebugData(self.url)
        elif item.type == ITEM_TYPE_PROVIDER:  # 树第三层,userObject下的DataService下的子节点
            pass

        self.groupBox.setHidden(item.type != ITEM_TYPE_PAGE)
        self.fillPropertyEditor(item.data)

    @pyqtSlot(QModelIndex)
    def onTreeItemDoubleClicked(self, index):
        item = self.treeModel.itemFromIndex(index)
        if item.type == ITEM_TYPE_PROVIDER:
            self.showQueryDialog(item.data)

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
                            if isinstance(dataServiceNodes['object']['provider'], list):
                                for j, provider in enumerate(dataServiceNodes['object']['provider']):
                                    dsRow = QStandardItem(provider['ds']['@providerClass'])
                                    dsRow.id = provider['@name']
                                    dsRow.data = provider
                                    dsRow.type = ITEM_TYPE_PROVIDER
                                    row.appendRow(dsRow)
                            else:
                                provider = dataServiceNodes['object']['provider']
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
                self.convertProperty(k, v)
        self.propertyEditor.addProperty(self.qObject)

    def convertProperty(self, k, v):
        """递归的将多层属性字典转成单层的."""
        if isinstance(v, dict):
            for subk, subv in v.items():
                self.convertProperty(subk, subv)
        else:
            setattr(self.qObject, k, v)

    def showQueryDialog(self, data):
        print('show query dialog: ', data)
        self.dialog = DataQueryDialog(data)
        self.dialog.finishSignal.connect(self.onGetQueryUrl)
        self.dialog.show()

    def onGetQueryUrl(self, url):
        self.browser.load(QUrl(url))
        self.statusBar().showMessage(url)
