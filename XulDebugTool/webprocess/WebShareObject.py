#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Web桥接对象
author: Allen
last edited: 2017.11.7

"""

from PyQt5.QtCore import pyqtProperty
from PyQt5.QtWidgets import QWidget

from XulDebugTool.webprocess.WebDataHandler import WebDataHandler


class WebShareObject(QWidget):
    def __init__(self):
        super(WebShareObject, self).__init__()

    def _getStrValue(self):
        return '100'

    def _setStrValue(self, str):
        WebDataHandler().readData(str)

    strValue = pyqtProperty(str, fget=_getStrValue, fset=_setStrValue)
