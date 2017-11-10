#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Web桥接对象
author: Allen
last edited: 2017.11.7

"""
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtWidgets import QWidget, QMessageBox


class WebShareObject(QWidget):
    def __init__(self):
        super(WebShareObject, self).__init__()

    def _getStrValue(self):
        return '100'

    def _setStrValue(self, str):
        print('receive %s' % str)

    strValue = pyqtProperty(str, fget=_getStrValue, fset=_setStrValue)
