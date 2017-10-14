#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
XulDebugTool

窗口基类, 设置窗口图标, 标题, 居中等属性

author: Kenshin
last edited: 2017.10.14
"""

import os
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5.QtGui import QIcon


class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'XulDebugTool'
        self.initWindow()

    def initWindow(self):
        self.setWindowTitle(self.title)
        iconPath = os.path.join('..', 'resources', 'images', 'icon.png')
        self.setWindowIcon(QIcon(iconPath))
        self.center()

    # 设置窗口居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
