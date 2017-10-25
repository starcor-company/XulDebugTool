#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLineEdit, QApplication
from PyQt5.QtCore import Qt


class SearchBarQLineEdit(QLineEdit):
    def __init__(self, main):
        super(QLineEdit, self).__init__()
        self.main = main
        self.setClearButtonEnabled(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down or event.key() == Qt.Key_Up:
            self.main.focused_column().view.setFocus()
            if self.main.selected_indexes():  # if the selection remains valid after the search
                QApplication.sendEvent(self.main.focused_column().view, event)
            else:
                self.main.set_top_row_selected()
        else:
            QLineEdit.keyPressEvent(self, event)
