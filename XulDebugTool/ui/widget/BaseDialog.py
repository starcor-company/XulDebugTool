#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
XulDebugTool

窗口基类, 设置窗口图标, 标题, 居中等属性

author: Kenshin
last edited: 2017.10.14
"""

from PyQt5.QtWidgets import QDesktopWidget, QDialog

from XulDebugTool.utils.IconTool import IconTool


class BaseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.title = 'XulDebugTool'

    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(IconTool.buildQIcon('icon.png'))
        self.resize(500,300)
        self.center()

    # 设置窗口居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
