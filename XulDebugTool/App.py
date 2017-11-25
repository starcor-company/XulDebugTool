#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
XulDebugTool

应用入口

author: Kenshin
last edited: 2017.10.14
"""

import sys

from PyQt5.QtWidgets import QApplication
from XulDebugTool.ui.ConnectWindow import ConnectWindow


class App(object):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConnectWindow()
    sys.exit(app.exec_())
