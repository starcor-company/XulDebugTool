#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
XulDebugTool

应用的第一个窗口,连接设备.

author: Kenshin
last edited: 2017.10.14
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QTextEdit
from XulDebugTool.ui.BaseWindow import BaseWindow
from XulDebugTool.utils.CmdExecutor import CmdExecutor


class ConnectWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.cmdExecutor = CmdExecutor()
        self.cmdExecutor.finishSignal.connect(self.onCmdExectued)
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

        self.connect_button = QPushButton('connect', self)
        self.connect_button.move(180, 90)
        self.connect_button.clicked.connect(self.onConnectClick)

        self.detail_label = QPushButton(self)
        self.detail_label.setText('↓detail')
        self.detail_label.move(350, 110)
        self.detail_label.setFlat(True)
        self.detail_label.setStyleSheet("QPushButton{background: transparent;}");
        self.detail_label.clicked.connect(self.onDetailClick)

        self.detail_edit = QTextEdit(self)
        self.detail_edit.move(25, 150)
        self.detail_edit.resize(420, 180)

    @pyqtSlot()
    def onConnectClick(self):
        ip = self.ip_editbox.text()
        port = self.port_editbox.text()
        if ip == '' or port == '':
            self.detail_edit.append('请输出正确的地址or端口.')
            print('请输出正确的地址or端口.')
        else:
            self.currentCmd = 'adb connect ' + ip
            self.detail_edit.append(self.currentCmd)
            self.connect_button.setEnabled(False)
            self.connect_button.setText('connecting...')
            self.detail_edit.append('connecting...')
            self.cmdExecutor.exec(self.currentCmd)

    def onCmdExectued(self, result):
        for r in result:
            self.detail_edit.append(r)
            print(r)
        if self.currentCmd.startswith('adb connect'):
            self.connect_button.setEnabled(True)
            self.connect_button.setText('connect')
            self.checkDeviceStatus()
        elif self.currentCmd == 'adb devices':
            pass

    def checkDeviceStatus(self):
        self.currentCmd = 'adb devices'
        self.detail_edit.append(self.currentCmd)
        self.cmdExecutor.exec(self.currentCmd)

    @pyqtSlot()
    def onDetailClick(self):
        # show log
        if self.height() == 150:
            self.setFixedSize(460, 350)
            self.detail_label.setText('↑detail')
        # hide log
        else:
            self.setFixedSize(460, 150)
            self.detail_label.setText('↓detail')
