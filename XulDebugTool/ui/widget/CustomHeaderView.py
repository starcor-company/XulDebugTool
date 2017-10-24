#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHeaderView, QStyleOptionHeader, QApplication, QStyle
from PyQt5.QtCore import Qt


class CustomHeaderView(QHeaderView):
    def __init__(self, text):
        super(CustomHeaderView, self).__init__(Qt.Horizontal)
        self.setSectionResizeMode(QHeaderView.Stretch)
        self.text = text

    def paintSection(self, painter, rect, logical_index):
        opt = QStyleOptionHeader()
        opt.rect = rect
        opt.text = self.text
        QApplication.style().drawControl(QStyle.CE_Header, opt, painter, self)
