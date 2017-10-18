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

        ipLabel = QLabel(self)
        ipLabel.setText('ip:')
        ipLabel.move(45, 15)

        portLabel = QLabel(self)
        portLabel.setText('port:')
        portLabel.move(28, 45)

        self.ipEditbox = QLineEdit(self)
        self.ipEditbox.move(80, 20)
        self.ipEditbox.resize(280, 25)
        self.ipEditbox.setText('172.31.11.144')

        self.portEditbox = QLineEdit(self)
        self.portEditbox.move(80, 50)
        self.portEditbox.resize(100, 25)
        self.portEditbox.setText('55550')

        self.connectButton = QPushButton('connect', self)
        self.connectButton.move(180, 90)
        self.connectButton.clicked.connect(self.onConnectClick)

        self.detailLabel = QPushButton(self)
        self.detailLabel.setText('↓detail')
        self.detailLabel.move(350, 110)
        self.detailLabel.setFlat(True)
        self.detailLabel.setStyleSheet("QPushButton{background: transparent;}");
        self.detailLabel.clicked.connect(self.onDetailClick)

        self.detailEdit = QTextEdit(self)
        self.detailEdit.move(25, 150)
        self.detailEdit.resize(420, 180)

    @pyqtSlot()
    def onConnectClick(self):
        ip = self.ipEditbox.text()
        port = self.portEditbox.text()
        if ip == '' or port == '':
            self.detailEdit.append('请输出正确的地址or端口.')
            print('请输出正确的地址or端口.')
        else:
            self.currentCmd = 'adb connect ' + ip
            self.detailEdit.append(self.currentCmd)
            self.connectButton.setEnabled(False)
            self.connectButton.setText('connecting...')
            self.detailEdit.append('connecting...')
            self.cmdExecutor.exec(self.currentCmd)

    def onCmdExectued(self, result):
        for r in result:
            self.detailEdit.append(r)
            print(r)
        if self.currentCmd.startswith('adb connect'):
            self.connectButton.setEnabled(True)
            self.connectButton.setText('connect')
            self.checkDeviceStatus()
        elif self.currentCmd == 'adb devices':
            pass

    def checkDeviceStatus(self):
        self.currentCmd = 'adb devices'
        self.detailEdit.append(self.currentCmd)
        self.cmdExecutor.exec(self.currentCmd)

    @pyqtSlot()
    def onDetailClick(self):
        # show log
        if self.height() == 150:
            self.setFixedSize(460, 350)
            self.detailLabel.setText('↑detail')
        # hide log
        else:
            self.setFixedSize(460, 150)
            self.detailLabel.setText('↓detail')
