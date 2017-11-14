#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Web桥接对象
author: Allen
last edited: 2017.11.7

"""
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtWidgets import QWidget, QMessageBox

from XulDebugTool.utils.Utils import Utils


class WebShareObject(QWidget):
    def __init__(self):
        super(WebShareObject, self).__init__()

    def _getStrValue(self):
        return '100'

    def _setStrValue(self, str):
        list = Utils.findNodeById(str)
        print('receive %s' % list[0].tag)
        print('receive %s' % list[0].text)
        print('receive %s' % list[0].attrib)
        # for element in list:
        #     children = element.getchildren()
        #     if len(children):
        #         print(element.text + " " + children[0].text)
        #     else:
        #         print(element.text)

    strValue = pyqtProperty(str, fget=_getStrValue, fset=_setStrValue)



