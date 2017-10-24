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
from XulDebugTool.utils.IconTool import IconTool
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import XulDebugTool.model.model as model


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
        # left layout
        self.tree_header = [self.tr('Text'), self.tr('Estimate'), self.tr('Start date')]
        self.item_model = model.TreeModel(self, header_list=self.tree_header)

        self.treeView = ExpandTreeView(self.item_model)
        self.treeView.setItemDelegate(model.BookmarkDelegate(self, self.item_model))
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.treeView.customContextMenuRequested.connect(self.open_edit_shortcut_contextmenu)
        # self.treeView.clicked.connect(lambda i: self.focus_index(self.filter_proxy_index_from_model_index(i)))
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeView.setHeader(CustomHeaderView(self.tr('Model')))
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.setUniformRowHeights(True)
        self.treeView.setAnimated(True)
        self.treeView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        leftContainer = QWidget()
        leftContainer.setMaximumWidth(255)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 6, 0)  # left, top, right, bottom
        layout.addWidget(self.treeView)
        leftContainer.setLayout(layout)

        self.mainSplitter = QSplitter(Qt.Horizontal)
        self.mainSplitter.setHandleWidth(0)  # thing to grab the splitter

        self.mainSplitter.addWidget(leftContainer)
        self.mainSplitter.addWidget(QLabel('111'))
        self.mainSplitter.addWidget(QLabel('222'))

        self.setCentralWidget(self.mainSplitter)
