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
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineScript, QWebEnginePage
from PyQt5.QtWidgets import *
import json

from XulDebugTool.logcatapi.Logcat import STCLogger
from XulDebugTool.ui.AboutWindow import AboutWindow
from XulDebugTool.ui.BaseWindow import BaseWindow
from XulDebugTool.ui.widget.ButtomConsoleWindow import ButtomWindow
from XulDebugTool.ui.widget.DataQueryDialog import DataQueryDialog
from XulDebugTool.ui.widget.FavoriteTreeView import FavoriteTreeView
from XulDebugTool.ui.widget.PropertyEditor import PropertyEditor
from XulDebugTool.ui.widget.UpdateProperty import UpdateProperty
from XulDebugTool.ui.widget.model.database.ConfigurationDB import ConfigurationDB
from XulDebugTool.utils.ConfigHelper import ConfigHelper
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

# 获取元素详情的4个参数
SKIP_PROP = 'skip-prop'
WITH_CHILDREN = 'with-children'
WITH_BINDING_DATA = 'with-binding-data'
WITH_POSITION = 'with-position'
WITH_SELECTOR = 'with-selector'

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
        self.resize(int(Utils.getWindowWidth()*0.8), int(Utils.getWindowHeight()*0.8))
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
        settingAction.triggered.connect(lambda: STCLogger().d('setting'))
        clearCacheAction = QAction(IconTool.buildQIcon('clearCache.png'),'&ClearCache',self);
        clearCacheAction.setShortcut('Ctrl+Alt+C');
        clearCacheAction.setShortcutContext(Qt.ApplicationShortcut)
        clearCacheAction.triggered.connect(self.clearCache)
        settingLogPathAction = QAction(IconTool.buildQIcon('path.png'),'&LogPath',self);
        settingLogPathAction.triggered.connect(self.setLogPath)
        fileMenu.addAction(disConnectAction)
        fileMenu.addAction(clearCacheAction)
        fileMenu.addAction(settingLogPathAction)
        # fileMenu.addAction(settingAction)
        # fileMenu.addAction(showLogAction)

        # settingAction.triggered.connect(self.openSettingWindow)

        editMenu = menuBar.addMenu('Edit')
        findAction = QAction(IconTool.buildQIcon('find.png'), '&Find', self)
        findAction.setShortcut('Ctrl+F')
        findAction.triggered.connect(self.findActionClick)
        editMenu.addAction(findAction)

        focusItemAction = QAction(IconTool.buildQIcon('focus.png'), '&Focus Item', self)
        focusItemAction.triggered.connect(self.focusChooseItem)
        editMenu.addAction(focusItemAction)
        self.chooseItemType = ''
        self.chooseItemId = ''

        settingMenu = menuBar.addMenu('Setting')
        autoLoginAction = QAction(IconTool.buildQIcon('setting.png'), '&Auto Login', self)
        autoLoginAction.setShortcutContext(Qt.ApplicationShortcut)
        autoLoginAction.triggered.connect(self.setAutoState)
        settingMenu.addAction(autoLoginAction)

        helpMenu = menuBar.addMenu('Help')
        aboutAction = QAction(IconTool.buildQIcon('about.png'), '&About', self)
        aboutAction.triggered.connect(self.openAboutWindow)
        helpMenu.addAction(aboutAction)

    def openAboutWindow(self):
        print('open about')
        self.aboutWindow = AboutWindow()
        self.aboutWindow.show()

    def setAutoState(self):
        reply = QMessageBox.question(self, "提示", "是否取消自动登录功能", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            Utils.setAutoLoginState(False)

    def restartProgram(self):
        from XulDebugTool.ui.ConnectWindow import ConnectWindow  # 不应该在这里导入，但是放在前面会有问题
        try:
            hasAbout = object.__getattribute__(self, "aboutWindow")
        except:
            hasAbout = None
        if hasAbout is not None:
            self.aboutWindow.close()
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

        # search shall start not before the user completed typing
        # filter_delay = DelayedExecutionTimer(self)
        # new_column.search_bar.textEdited[str].connect(filter_delay.trigger)
        # filter_delay.triggered[str].connect(self.search)

        self.tabBar = QTabBar()
        self.tabBar.setUsesScrollButtons(False)
        self.tabBar.setDrawBase(False)
        # self.tabBar.addTab('tab1')
        # self.tabBar.addTab('tab2')

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
        self.searchHolder.setLayout(layout)
        self.searchHolder.layout().setContentsMargins(6, 6, 6, 0)

        self.tabContentWidget = QWidget()
        self.browser = QWebEngineView()
        self.browser.setZoomFactor(1.3)
        self.channel = QWebChannel()
        self.webObject = WebShareObject()
        self.channel.registerObject('bridge', self.webObject)
        self.browser.page().setWebChannel(self.channel)
        self.webObject.jsCallback.connect(lambda value: self.addUpdate(value))

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

        Utils.scriptCreator(os.path.join('..', 'resources', 'js', 'event.js'), 'event.js',
                            self.browser.page())
        self.browser.page().setWebChannel(self.channel)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.initQCheckBoxUI())
        layout.addWidget(self.initSearchView())
        layout.addWidget(self.browser)
        self.tabContentWidget.setLayout(layout)
        self.searchWidget.hide()

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
        self.rightSiderClickInfo = 'Property'

        self.rightSiderTabWidget = QTabWidget()
        self.rightSiderTabBar = QTabBar()
        self.rightSiderTabWidget.setTabBar(self.rightSiderTabBar)
        self.rightSiderTabWidget.setTabPosition(QTabWidget.East)
        self.favoriteTreeView = FavoriteTreeView(self)

        # self.propertyEditor = PropertyEditor(['Key', 'Value'])
        self.inputWidget = UpdateProperty()
        self.rightSiderTabWidget.addTab(self.inputWidget, IconTool.buildQIcon('property.png'), 'Property')

        self.rightSiderTabWidget.setStyleSheet(('QTab::tab{height:60px;width:32px;color:black;padding:0px}'
                                                'QTabBar::tab:selected{background:lightgray}'))

        # self.rightSiderTabWidget.addTab(self.propertyEditor,IconTool.buildQIcon('property.png'),'property')
        self.rightSiderTabWidget.addTab(self.favoriteTreeView, IconTool.buildQIcon('favorites.png'), 'Favorites')
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
        self.mainSplitter.setStretchFactor(2, 1)
        self.setCentralWidget(self.mainSplitter)
        # 默认隐藏掉复选框
        self.groupBox.setHidden(True)

    def addUpdate(self, value=None):
        self.inputWidget.initData(self.pageId, value)
        self.inputWidget.updateItemUI()
        dict = json.loads(value)
        if dict['action'] == "click":
            self.chooseItemId = dict['Id']
            self.chooseItemType = Utils.findNodeById(dict['Id'], dict['xml']).tag

    def focusChooseItem(self):
        if self.chooseItemType in ('area', 'item'):
            XulDebugServerHelper.focusChooseItemUrl(self.chooseItemId)

    def initQCheckBoxUI(self):
        self.groupBox = QGroupBox()
        self.skipPropCheckBox = QCheckBox(SKIP_PROP, self)
        self.skipPropCheckBox.setChecked(False)
        self.skipPropCheckBox.stateChanged.connect(lambda: self.clickCheckBox(self.skipPropCheckBox, SKIP_PROP))

        self.withChildrenCheckBox = QCheckBox(WITH_CHILDREN, self)
        self.withChildrenCheckBox.setChecked(False)
        self.withChildrenCheckBox.stateChanged.connect(lambda: self.clickCheckBox(self.withChildrenCheckBox, WITH_CHILDREN))

        self.withBindingDataCheckBox = QCheckBox(WITH_BINDING_DATA, self)
        self.withBindingDataCheckBox.setChecked(False)
        self.withBindingDataCheckBox.stateChanged.connect(lambda: self.clickCheckBox(self.withBindingDataCheckBox, WITH_BINDING_DATA))

        self.withPositionCheckBox = QCheckBox(WITH_POSITION, self)
        self.withPositionCheckBox.setChecked(False)
        self.withPositionCheckBox.stateChanged.connect(lambda: self.clickCheckBox(self.withPositionCheckBox, WITH_POSITION))

        self.withSelectorCheckBox = QCheckBox(WITH_SELECTOR, self)
        self.withSelectorCheckBox.setChecked(False)
        self.withSelectorCheckBox.stateChanged.connect(lambda: self.clickCheckBox(self.withSelectorCheckBox, WITH_SELECTOR))

        checkGrouplayout = QHBoxLayout()
        checkGrouplayout.addWidget(self.skipPropCheckBox)
        checkGrouplayout.addWidget(self.withChildrenCheckBox)
        checkGrouplayout.addWidget(self.withBindingDataCheckBox)
        checkGrouplayout.addWidget(self.withPositionCheckBox)
        checkGrouplayout.addWidget(self.withSelectorCheckBox)
        self.groupBox.setLayout(checkGrouplayout)
        return self.groupBox

    def initSearchView(self):
        self.searchWidget = QWidget()
        self.searchWidget.setStyleSheet(".QWidget{border:1px solid rgb(220, 220, 220)}")
        searchPageLayout = QHBoxLayout()
        self.searchIcon = QAction(self)
        self.searchIcon.setIcon(IconTool.buildQIcon('find.png'))
        self.searchDelIcon = QAction(self)
        self.searchDelIcon.setIcon(IconTool.buildQIcon('del.png'))
        self.searchLineEdit = QLineEdit()
        self.searchLineEdit.addAction(self.searchIcon, QLineEdit.LeadingPosition)
        self.searchLineEdit.addAction(self.searchDelIcon, QLineEdit.TrailingPosition)
        self.searchDelIcon.setVisible(False)
        self.searchLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")
        searchPageLayout.addWidget(self.searchLineEdit)
        self.searchLineEdit.textChanged.connect(self.searchPage)
        self.searchDelIcon.triggered.connect(self.searchDelClick)
        self.previousBtn = QPushButton()
        self.previousBtn.setStyleSheet("background:transparent;")
        self.previousBtn.setIcon(IconTool.buildQIcon('up.png'))
        self.previousBtn.setFixedSize(15, 20)
        searchPageLayout.addWidget(self.previousBtn)
        self.previousBtn.clicked.connect(lambda: self.previousBtnClick(self.searchLineEdit.text()))
        self.nextBtn = QPushButton()
        self.nextBtn.setIcon(IconTool.buildQIcon('down.png'))
        self.nextBtn.setStyleSheet("background:transparent;")
        self.nextBtn.setFixedSize(15, 20)
        self.nextBtn.clicked.connect(lambda: self.nextBtnClick(self.searchLineEdit.text()))
        searchPageLayout.addWidget(self.nextBtn)
        self.matchCase = QCheckBox("Match Case")
        self.matchCase.setChecked(False)
        self.matchCase.stateChanged.connect(self.matchCaseChange)
        searchPageLayout.addWidget(self.matchCase)

        self.matchTips = QLabel()
        self.matchTips.setFixedWidth(100)
        self.searchClose = QPushButton("×")
        self.searchClose.setFixedWidth(10)
        self.searchClose.setStyleSheet("background:transparent;")
        self.searchClose.clicked.connect(self.searchCloseClick)
        searchPageLayout.addWidget(self.matchTips)
        searchPageLayout.addWidget(self.searchClose)
        self.searchWidget.setLayout(searchPageLayout)
        return self.searchWidget

    def clickCheckBox(self, checkBox, name):
        if checkBox.isChecked():
            STCLogger().i('select '+name)
            self.selectCheckBoxInfo(name)
        else:
            STCLogger().i('cancel '+name)
            self.cancelCheckBoxInfo(name)

    def selectCheckBoxInfo(self, str):
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
                    self.url = self.url.replace(unCheckedStr, checkedStr)
            self.showXulDebugData(self.url)

    def cancelCheckBoxInfo(self, str):
        if None != self.url:
            checkedStr = str + '=' + 'true'
            if self.url.find(checkedStr) >= -1:
                split = self.url.split(checkedStr)
                self.url = ''.join(split)
                self.url = self.url.replace('&&', '&')
                self.url = self.url.replace('?&', '?')
                if self.url.endswith('?'):
                    self.url = self.url[:-1]
                if self.url.endswith('&'):
                    self.url = self.url[:-1]
                self.showXulDebugData(self.url)

    def rightSiderClick(self, index):
        # 两次单击同一个tabBar时显示隐藏内容区域
        if self.rightSiderTabBar.tabText(index) == self.rightSiderClickInfo:
            if self.rightSiderTabWidget.width() == Utils.getItemHeight():
                self.rightSiderTabWidget.setMaximumWidth(Utils.getWindowWidth())
                self.rightSiderTabWidget.setMinimumWidth(Utils.getItemHeight())
            else:
                self.rightSiderTabWidget.setFixedWidth(Utils.getItemHeight())
        else:
            if self.rightSiderTabWidget.width() == Utils.getItemHeight():
                self.rightSiderTabWidget.setMaximumWidth(Utils.getWindowWidth())
                self.rightSiderTabWidget.setMinimumWidth(Utils.getItemHeight())
        self.rightSiderClickInfo = self.rightSiderTabBar.tabText(index)

    def clearCache(self):
        r = XulDebugServerHelper.clearAllCaches()
        if r.status == 200 :
            self.statusBar().showMessage('cache cleanup success')
        else:
            self.statusBar().showMessage('cache cleanup failed')

    def setLogPath(self):
        file_path = QFileDialog.getSaveFileName(self, 'save file', ConfigHelper.LOGCATPATH,"Txt files(*.txt)")
        if len(file_path[0]) > 0:
            ConfigurationDB.saveConfiguration(ConfigHelper.KEY_LOGCATPATH,file_path[0])


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
            self.showXulDebugData(self.url)
        elif item.type == ITEM_TYPE_USER_OBJECT:  # 树第二层,userObject下的子节点
            objectId = item.id
            self.url = XulDebugServerHelper.HOST + 'get-user-object/' + objectId
            self.showXulDebugData(self.url)
        elif item.type == ITEM_TYPE_PROVIDER:  # 树第三层,userObject下的DataService下的子节点
            pass

        self.groupBox.setHidden(item.type != ITEM_TYPE_PAGE)
        # self.fillPropertyEditor(item.data)

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
                    row.id = self.pageId = page['@id']
                    row.data = page
                    row.type = ITEM_TYPE_PAGE
                    self.pageItem.appendRow(row)
            else:
                page = pagesNodes['page']
                row = QStandardItem(page['@pageId'])
                row.id = self.pageId = page['@id']
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
            if userObjectNodes and isinstance(userObjectNodes['object'], list):
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
                                for j, provider in enumerate(
                                        dataServiceNodes['object']['provider']):
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
            self.userobjectItem.setText(
                '%s(%s)' % (ROOT_ITEM_USER_OBJECT, self.userobjectItem.rowCount()))

    def showXulDebugData(self, url):
        STCLogger().i('request url:' + url)
        self.browser.load(QUrl(url))
        self.statusBar().showMessage(url)

    def convertProperty(self, k, v):
        """递归的将多层属性字典转成单层的."""
        if isinstance(v, dict):
            for subk, subv in v.items():
                self.convertProperty(subk, subv)
        else:
            setattr(self.qObject, k, v)

    def showQueryDialog(self, data):
        STCLogger().i('show query dialog: ', data)
        self.dialog = DataQueryDialog(data)
        self.dialog.finishSignal.connect(self.onGetQueryUrl)
        self.dialog.show()

    def onGetQueryUrl(self, url):
        STCLogger().i('request url:' + url)
        self.favoriteTreeView.updateTree()
        self.browser.load(QUrl(url))
        self.statusBar().showMessage(url)

    def findActionClick(self):
        self.searchWidget.show()
        self.searchLineEdit.setFocus()
        self.searchLineEdit.setText(self.browser.selectedText())

    def searchPage(self, text):
        if not text.strip():
            self.searchDelIcon.setVisible(False)
        else:
            self.searchDelIcon.setVisible(True)
        check = self.matchCase.isChecked()
        if check:
            self.browser.findText(text, QWebEnginePage.FindFlags(2), lambda result: self.changeMatchTip(result))
        else:
            self.browser.findText(text, QWebEnginePage.FindFlags(0), lambda result: self.changeMatchTip(result))

    def previousBtnClick(self, text):
        check = self.matchCase.isChecked()
        if check:
            self.browser.findText(text, QWebEnginePage.FindFlags(1) | QWebEnginePage.FindFlags(2),
                                  lambda result: self.changeMatchTip(result))
        else:
            self.browser.findText(text, QWebEnginePage.FindFlags(1), lambda result: self.changeMatchTip(result))

    def nextBtnClick(self, text):
        check = self.matchCase.isChecked()
        if check:
            self.browser.findText(text, QWebEnginePage.FindFlags(2),
                                  lambda result: self.changeMatchTip(result))
        else:
            self.browser.findText(text, QWebEnginePage.FindFlags(0), lambda result: self.changeMatchTip(result))

    def matchCaseChange(self):
        self.browser.findText("")
        self.searchPage(self.searchLineEdit.text())

    def changeMatchTip(self, result):
        if result:
            self.matchTips.setText("Find matches")
        else:
            self.matchTips.setText("No matches")

    def searchDelClick(self):
        self.searchLineEdit.setText("")
        self.browser.findText("")
        self.matchTips.setText("")

    def searchCloseClick(self):
        self.searchLineEdit.setText("")
        self.browser.findText("")
        self.matchTips.setText("")
        self.searchWidget.hide()
