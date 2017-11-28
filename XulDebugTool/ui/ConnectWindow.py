#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
XulDebugTool

应用的第一个窗口,连接设备.

author: Kenshin
last edited: 2017.10.14
"""

import re
import sqlite3

from PyQt5.QtCore import pyqtSlot, Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QTextEdit, QComboBox, QHBoxLayout, QListWidget, QWidget, QMessageBox

from XulDebugTool.ui.BaseWindow import BaseWindow
from XulDebugTool.ui.MainWindow import MainWindow, QListWidgetItem
from XulDebugTool.utils.CmdExecutor import CmdExecutor
from XulDebugTool.utils.IconTool import IconTool
from XulDebugTool.utils.XulDebugServerHelper import XulDebugServerHelper


class ConnectWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        # 命令行执行器
        self.cmdExecutor = CmdExecutor()
        self.cmdExecutor.setFinishCallback(self.onCmdExectued)

        # 连接动画需要的timer, 1秒触发一次
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateButtonText)

        # 文字动画相关变量
        self.updateCount = 0
        self.connectState = ['.', '..', '...']

        # ip, adb port, xul port
        self.ip = ''
        self.adbPort = ''
        self.xulPort = ''

        self.initUI()
        self.show()

    def initUI(self):
        # 只显示关闭按钮, 不显示最大化, 最小化, 并且固定窗口大小
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setFixedSize(460, 150)

        self.ipLabel = QLabel(self)
        self.ipLabel.setPixmap(IconTool.buildQPixmap('ip.png'))
        self.ipLabel.move(40, 28)

        self.helpLabel = QLabel(self)
        self.helpLabel.setPixmap(IconTool.buildQPixmap('help.png'))
        self.helpLabel.move(380, 28)
        self.helpLabel.setToolTip('''格式: ip[:adb port][:xul port]
        default adb port is 5555
        default xul port is 55550
        EX: 192.168.200.2:5555:55550''')

        self.ipComboBox = QComboBox(self)
        self.ipComboBox.move(80, 30)
        self.ipComboBox.resize(290, 25)
        self.ipComboBox.setEditable(True)
        self.ipComboBox.setMaxVisibleItems(5)
        self.ipComboBox.setInsertPolicy(QComboBox.InsertAtTop)

        ipListWidget = QListWidget()
        self.ipComboBox.setView(ipListWidget)
        self.ipComboBox.setModel(ipListWidget.model())

        # self.ipComboBox.addItem('localhost')
        for pos, device in enumerate(self.getDevicesFromDB()):
            item = self.ComboBoxItem(pos, device[0])
            ipListItem = QListWidgetItem(ipListWidget)
            ipListWidget.setItemWidget(ipListItem, item)

        # combobox绘制子项完成，再向子项添加内容
        for pos, device in enumerate(self.getDevicesFromDB()):
            self.ipComboBox.setItemText(pos, device[0])

        self.connectButton = QPushButton('connect', self)
        self.connectButton.move(180, 90)
        self.connectButton.setGeometry(180, 90, 120, 25)
        self.connectButton.clicked.connect(self.onConnectClick)

        self.detailLabel = QPushButton(self)
        self.detailLabel.setText('↓detail')
        self.detailLabel.move(350, 110)
        self.detailLabel.setFlat(True)
        self.detailLabel.setStyleSheet("QPushButton{background: transparent;}")
        self.detailLabel.clicked.connect(self.onDetailClick)

        self.detailEdit = QTextEdit(self)
        self.detailEdit.move(25, 150)
        self.detailEdit.resize(420, 180)
        super().initWindow()

    def ComboBoxItem(self, pos, ip_src):
        qWidget = QWidget()
        deledeButton = QPushButton()
        deledeButton.setStyleSheet("background:transparent;")
        deledeButton.setIcon(QIcon(IconTool.buildQIcon('delete.png')))
        deledeButton.clicked.connect(lambda: self.onDeleteComBoxItem(pos, ip_src))
        boxLayout = QHBoxLayout()
        boxLayout.addStretch()
        boxLayout.addWidget(deledeButton)
        boxLayout.setContentsMargins(0, 0, 0, 0)
        boxLayout.setSpacing(5)
        qWidget.setLayout(boxLayout)
        return qWidget

    def onDeleteComBoxItem(self, pos, text):
        try:
            # 数据库文件数据类型文档需添加
            conn = sqlite3.connect('XulDebugTool.db')
            cursor = conn.cursor()
            cursor.execute("delete from device where name = \'" + text + "\'")
            conn.commit()
        except Exception:
            print('onDeleteComBoxItem error')
        finally:
            cursor.close()
            conn.close()
        self.ipComboBox.removeItem(pos)

    @pyqtSlot()
    def onConnectClick(self):
        comboBoxText = self.ipComboBox.currentText()
        devicePattern = re.compile(r"(.+?)(?:(?::(\d+)?)?(?::(\d+)))?$")
        m = devicePattern.match(comboBoxText)

        if m is None:
            self.detailEdit.append('ip非法,请输出正确的ip地址,格式:')
            self.detailEdit.append('ip[:adb port][:xul port]')
            self.detailEdit.append('default adb port:5555')
            self.detailEdit.append('default xul port:55550')
            return

        self.adbHost = m.group(1)
        self.adbPort = m.group(2)
        self.xulPort = m.group(3)

        if self.xulPort is None:
            self.xulPort = "55550"

        if self.adbPort is None:
            self.adbPort = ""

        if self.adbHost is None or self.adbHost == '':
            self.detailEdit.append('ip非法,请输出正确的ip地址,格式:')
            self.detailEdit.append('ip[:adb port][:xul port]')
            self.detailEdit.append('default adb port:5555')
            self.detailEdit.append('default xul port:55550')
            return

        def onForwardFinished(result):
            self.ip = "localhost"
            XulDebugServerHelper.HOST = \
                'http://' + self.ip + ':' + self.xulPort + '/api/'
            if XulDebugServerHelper.isXulDebugServerAlive():
                # 存入该设备到历史记录
                self.addDeviceToDB()
                self.startMainWindow()
            self.timer.stop()
            self.connectButton.setEnabled(True)
            self.connectButton.setText('connect')
            self.connectButton.setStyleSheet("QPushButton{text-align : middle;}")

        def makeForward(result):
            self.currentCmd = ("adb -s {0} forward tcp:{1} tcp:{2}".format(
                self.adbHost, self.xulPort, self.xulPort))
            self.detailEdit.append('# ' + self.currentCmd)
            self.detailEdit.append('create new forward port...')
            self.cmdExecutor.setFinishCallback(onForwardFinished)
            self.cmdExecutor.exec(self.currentCmd)

        def onDeviceListed(result):
            m = [r.split("\t", 2)[0] for r in result if r.split("\t", 2)[0] == self.adbHost]
            if (self.adbPort is None or self.adbPort == '') and \
                    self.adbHost in m:
                # host connected via USB
                self.currentCmd = "adb forward --remove-all"
                self.connectButton.setEnabled(False)
                self.detailEdit.append('# ' + self.currentCmd)
                self.detailEdit.append('remove all forward ports...')
                self.cmdExecutor.setFinishCallback(makeForward)
                self.cmdExecutor.exec(self.currentCmd)
            else:
                self.ip = self.adbHost
                XulDebugServerHelper.HOST = \
                    'http://' + self.ip + ':' + self.xulPort + '/api/'
                self.timer.start(500)
                if self.adbPort is None or self.adbPort == "":
                    self.currentCmd = 'adb connect ' + self.ip
                else:
                    self.currentCmd = 'adb connect ' + self.ip + ':' + self.adbPort
                self.connectButton.setEnabled(False)
                self.detailEdit.append('# ' + self.currentCmd)
                self.detailEdit.append('connecting...')
                self.cmdExecutor.setFinishCallback(self.onCmdExectued)
                self.cmdExecutor.exec(self.currentCmd)

        self.cmdExecutor.setFinishCallback(onDeviceListed)
        self.cmdExecutor.exec("adb devices")
        self.detailEdit.append('start adb services...')
        return

    def onCmdExectued(self, result):
        for r in result:
            self.detailEdit.append(r)
            print(r)
            if "cmdExectuedTimeout" in result:
                self.resetConnectButton()
                print("cmdExectuedTimeout")
                return
        if self.currentCmd.startswith('adb connect'):
            self.checkDeviceStatus()
        elif self.currentCmd == 'adb devices':
            for r in result:
                # 找到连接成功的设备
                if self.ip in r:
                    if XulDebugServerHelper.isXulDebugServerAlive():
                        # 存入该设备到历史记录
                        self.addDeviceToDB()
                        self.startMainWindow()
            # 重置connect button
            self.resetConnectButton()

    def resetConnectButton(self):
        self.timer.stop()
        self.connectButton.setEnabled(True)
        self.connectButton.setText('connect')
        self.connectButton.setStyleSheet("QPushButton{text-align : middle;}")

    def checkDeviceStatus(self):
        self.currentCmd = 'adb devices'
        self.detailEdit.append('# ' + self.currentCmd)
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

    def updateButtonText(self):
        self.connectButton.setStyleSheet("QPushButton{text-align : left;}")
        self.connectButton.setText(' connecting' + self.connectState[self.updateCount])
        self.updateCount += 1
        if self.updateCount == 3:
            self.updateCount = 0

    def getDevicesFromDB(self):
        try:
            conn = sqlite3.connect('XulDebugTool.db')
            cursor = conn.cursor()
            cursor.execute('select * from device')
            result = cursor.fetchall()
        except Exception:
            return []
        finally:
            cursor.close()
            conn.close()
        return result

    def addDeviceToDB(self):
        device = self.adbHost + ':' + self.adbPort + ':' + self.xulPort
        self.detailEdit.append('# add ' + device + ' to db.')
        print('add ' + device + ' to db.')
        try:
            conn = sqlite3.connect('XulDebugTool.db')
            cursor = conn.cursor()
            cursor.execute('create table if not exists device (name varchar(50) primary key)')
            if self.ip != '':
                cursor.execute('insert into device (name) values (\'' + device + '\')')
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def startMainWindow(self):
        print('Start main window.')
        self.detailEdit.append('# Start main window.')
        self.mainWindow = MainWindow()
        self.mainWindow.show()
        self.close()
