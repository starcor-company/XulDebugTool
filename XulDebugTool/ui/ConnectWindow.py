#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
XulDebugTool

应用的第一个窗口,连接设备.

author: Kenshin
last edited: 2017.10.14
"""

import os
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from XulDebugTool.ui.BaseWindow import BaseWindow


class ConnectWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        # 只显示关闭按钮, 不显示最大化, 最小化, 并且固定窗口大小
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setFixedSize(460, 150)

        ip_label = QLabel(self)
        ip_label.setText('ip:')
        ip_label.move(45, 15)

        port_label = QLabel(self)
        port_label.setText('port:')
        port_label.move(28, 45)

        self.ip_editbox = QLineEdit(self)
        self.ip_editbox.move(80, 20)
        self.ip_editbox.resize(280, 25)
        self.ip_editbox.setText('172.31.11.144')

        self.port_editbox = QLineEdit(self)
        self.port_editbox.move(80, 50)
        self.port_editbox.resize(100, 25)
        self.port_editbox.setText('55550')

        button = QPushButton('connect', self)
        button.move(180, 90)
        button.clicked.connect(self.onClick)

    @pyqtSlot()
    def onClick(self):
        ip = self.ip_editbox.text()
        port = self.port_editbox.text()
        if ip == '' or port == '':
            self.statusBar().showMessage('请输出正确的地址or端口.')
        else:
            from subprocess import Popen, PIPE
            p = Popen('adb connect ' + ip, stdout=PIPE, bufsize=1)
            for line in iter(p.stdout.readline, b''):
                print(line.decode('utf-8'))
                self.statusBar().showMessage(line.decode('utf-8'))
            p.stdout.close()
            p.wait()
