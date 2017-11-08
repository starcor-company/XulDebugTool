#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDesktopWidget, QDialog

from XulDebugTool.utils.IconTool import IconTool


class BaseDialog(QDialog):
    def __init__(self, title):
        super().__init__()
        self.title = title

    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(IconTool.buildQIcon('icon.png'))
        self.resize(500, 300)
        self.center()

    # 设置窗口居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
