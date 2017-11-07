#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSignal


class ConsoleEmittor(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))