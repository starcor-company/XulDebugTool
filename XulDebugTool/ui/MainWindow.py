#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
XulDebugTool

主页面

author: Kenshin
last edited: 2017.10.23
"""

from XulDebugTool.ui.BaseWindow import BaseWindow
from XulDebugTool.ui.widget.ExpandTreeView import ExpandTreeView
from XulDebugTool.ui.widget.CustomHeaderView import CustomHeaderView
from XulDebugTool.ui.widget.SearchBarQLineEdit import SearchBarQLineEdit
from XulDebugTool.utils.IconTool import IconTool
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView

import XulDebugTool.model.model as model
import pyperclip


class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()
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
        self.treeHeader = ['Model']
        self.itemModel = model.TreeModel(self, header_list=self.treeHeader)

        self.treeView = ExpandTreeView(self.itemModel)
        self.treeView.setItemDelegate(model.BookmarkDelegate(self, self.itemModel))
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openContextMenu)
        self.treeView.clicked.connect(self.getDebugData)
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeView.setHeader(CustomHeaderView('Model'))
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.setUniformRowHeights(True)
        self.treeView.setAnimated(True)
        self.treeView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

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
        browser = QWebEngineView()
        browser.load(QUrl('https://github.com/starcor-company/XulDebugTool'))
        middleContainer.stackedWidget.addWidget(browser)
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
        #
        #
        # ----------------------------right layout---------------------------- #


        self.mainSplitter = QSplitter(Qt.Horizontal)
        self.mainSplitter.setHandleWidth(0)  # thing to grab the splitter

        self.mainSplitter.addWidget(leftContainer)
        self.mainSplitter.addWidget(middleContainer)
        self.mainSplitter.addWidget(QLabel('3333'))
        self.mainSplitter.setStretchFactor(0, 0)
        self.mainSplitter.setStretchFactor(1, 6)
        self.mainSplitter.setStretchFactor(2, 3)

        self.setCentralWidget(self.mainSplitter)

    @pyqtSlot(QPoint)
    def openContextMenu(self, point):
        index = self.treeView.indexAt(point)
        if not index.isValid():
            return
        item = index.internalPointer()
        menu = QMenu()
        copyAction = QAction(IconTool.buildQIcon('copy.png'), 'Copy to Clipboard', self,
                             triggered=lambda: pyperclip.copy('%s' % item.text))
        menu.addAction(copyAction)
        menu.exec_(self.treeView.viewport().mapToGlobal(point))

    def getDebugData(self):
        pass