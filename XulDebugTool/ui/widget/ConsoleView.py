#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import QMainWindow, QAction, \
    QSplitter, QApplication, QWidget, QHBoxLayout, QComboBox, QPushButton, \
    QLineEdit, QSizePolicy, QVBoxLayout, QTextBrowser

from XulDebugTool.utils.ConsoleStreamEmittor import ConsoleEmittor
from XulDebugTool.utils.IconTool import IconTool


class ConsoleWindow(QMainWindow):
    global textEdit

    def __init__(self, parent=None):
        super(ConsoleWindow, self).__init__(parent)
        self.isConUrl = False

        # 上
        self.searchButton = QLineEdit()
        self.searchButton.setPlaceholderText("搜索")
        self.searchButton.setMaximumWidth(300)
        self.searchButton.setMaximumHeight(32)
        self.searchButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.combo = QComboBox(self);
        self.combo.insertItem(0, 'Error');
        self.combo.insertItem(1, 'Debug');
        self.combo.insertItem(2, 'Verbose');
        self.combo.insertItem(3, 'Warning');
        self.combo.setCurrentIndex(0)

        layout_top = QHBoxLayout()
        layout_top.setAlignment(Qt.AlignRight)
        layout_top.setSpacing(20)
        # layout_top.addWidget(self.combo)
        # layout_top.addWidget(self.searchButton)

        self.functionTabWiget = QWidget()
        self.functionTabWiget.setAutoFillBackground(True)
        self.functionTabWiget.setFixedHeight(20)
        self.functionTabWiget.setLayout(layout_top)

        # 左
        self.clearButton = QPushButton(self)
        icon = QIcon(IconTool.buildQIcon('clear.png'))
        self.clearButton.setIcon(icon)
        self.clearButton.setFixedWidth(18)
        self.clearButton.setFixedHeight(20)
        self.clearButton.clicked.connect(self.clear)
        self.clearButton.setToolTip("Clear the logcat")
        self.setStyleSheet('''
            QPushButton{
                border: none;
                background-color: #0000 ;
            }
            
            QPushButton:hover {
            border: 1px solid #C0C0C0;
            background-color: yellow;
            border-style: inset;
            border-radius:2px;
            background-color:#C0C0C0;  
            border-style: solid;
            }
            ''')

        self.layoutLeft = QVBoxLayout()
        self.layoutLeft.setAlignment(Qt.AlignTop)
        self.layoutLeft.setSpacing(1)
        self.layoutLeft.addWidget(self.clearButton)
        self.layoutLeft.setContentsMargins(4, 0, 0, 0)
        self.leftWiget = QWidget()
        self.leftWiget.setAutoFillBackground(True)
        self.leftWiget.setLayout(self.layoutLeft)
        self.leftWiget.setFixedWidth(22)

        # 右
        self.textEdit = QTextBrowser()
        self.textEdit.setOpenLinks(True)
        self.textEdit.setOpenExternalLinks(True)
        self.textEdit.setReadOnly(True)

        self.rightWiget = QWidget()
        self.rightWiget.setAutoFillBackground(True)
        self.rightWiget.setFixedWidth(15)

        self.messageSplitter = QSplitter(Qt.Horizontal)
        self.messageSplitter.addWidget(self.leftWiget)
        self.messageSplitter.addWidget(self.textEdit)
        self.messageSplitter.addWidget(self.rightWiget)

        self.mainSplitter = QSplitter(Qt.Vertical)
        self.mainSplitter.addWidget(self.functionTabWiget)
        self.mainSplitter.addWidget(self.messageSplitter)
        self.setCentralWidget(self.mainSplitter)

        # 重定向输出
        # sys.stdout = ConsoleEmittor(textWritten=self.normalOutputWritten)
        # sys.stderr = ConsoleEmittor(textWritten=self.normalOutputWritten)



    def normalOutputWritten(self, text):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertHtml(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()


    def initMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('Logcat')
        showLogAction = QAction('Show Log', self)
        fileMenu.addAction(showLogAction)

        helpMenu = menuBar.addMenu('Setting')
        aboutAction = QAction(IconTool.buildQIcon('setting.png'), 'About', self)
        helpMenu.addAction(aboutAction)

    def clear(self):
        self.textEdit.clear()
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = ConsoleWindow()
    sys.exit(app.exec_())




