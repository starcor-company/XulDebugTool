#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
XulDebugTool

应用的第一个窗口,连接设备.

author: Kenshin
last edited: 2017.10.14
"""

from PyQt5.QtCore import pyqtSlot, Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QTextEdit, QComboBox, QHBoxLayout, QListWidget, QWidget

from XulDebugTool.ui.BaseWindow import BaseWindow
from XulDebugTool.ui.MainWindow import MainWindow, QListWidgetItem
from XulDebugTool.utils.IconTool import IconTool
from XulDebugTool.utils.CmdExecutor import CmdExecutor
from XulDebugTool.utils.XulDebugServerHelper import XulDebugServerHelper
import sqlite3


class ConnectWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        # 命令行执行器
        self.cmdExecutor = CmdExecutor()
        self.cmdExecutor.finishSignal.connect(self.onCmdExectued)

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
        self.ipLabel.setPixmap(IconTool.buildQPixmap('ip_icon.png'))
        self.ipLabel.move(40, 28)

        self.helpLabel = QLabel(self)
        self.helpLabel.setPixmap(IconTool.buildQPixmap('help.png'))
        self.helpLabel.move(380, 28)
        self.helpLabel.setToolTip('''格式: ip[:adb port][:xul port]
        default adb port is 5555
        default xul port is 55550
        ps: 192.168.200.2:5555:55550''')

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

        #combobox绘制子项完成，再向子项添加内容
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
        delede_button = QPushButton()
        delede_button.setStyleSheet("background:transparent;")
        icon = QIcon(IconTool.buildQIcon('delete.png'))
        delede_button.setIcon(icon)
        delede_button.clicked.connect(lambda :self.onDeleteComBoxItem(pos, ip_src))
        main_layout = QHBoxLayout()
        main_layout.addStretch()
        main_layout.addWidget(delede_button)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(5)
        qWidget.setLayout(main_layout)
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
        self.ip = comboBoxText.split(':')[0]
        if self.ip == '':
            self.detailEdit.append('ip非法,请输出正确的ip地址,格式:')
            self.detailEdit.append('ip[:adb port][:xul port]')
            self.detailEdit.append('default adb port:5555')
            self.detailEdit.append('default xul port:55550')
            return
        try:
            self.adbPort = comboBoxText.split(':')[1]
        except IndexError:
            self.adbPort = '5555'
        try:
            self.xulPort = comboBoxText.split(':')[2]
        except IndexError:
            self.xulPort = '55550'

        XulDebugServerHelper.HOST = 'http://' + self.ip + ':' + self.xulPort + '/api/'
        self.timer.start(500)
        self.currentCmd = 'adb connect ' + self.ip + ':' + self.adbPort
        self.detailEdit.append('# ' + self.currentCmd)
        self.connectButton.setEnabled(False)
        self.detailEdit.append('connecting...')
        self.cmdExecutor.exec(self.currentCmd)

    def onCmdExectued(self, result):
        for r in result:
            self.detailEdit.append(r)
            print(r)
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
        device = self.ip + ':' + self.adbPort + ':' + self.xulPort
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
