#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
XulDebugTool

主页面

author: Kenshin
last edited: 2017.10.23
"""

from XulDebugTool.ui.BaseWindow import BaseWindow
from XulDebugTool.utils.IconTool import IconTool
from PyQt5.QtWidgets import QAction

class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.resize(1400, 800)

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
        super().initWindow()
