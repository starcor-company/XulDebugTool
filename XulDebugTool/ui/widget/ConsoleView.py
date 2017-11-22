#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
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
        layout_top.addWidget(self.combo)
        layout_top.addWidget(self.searchButton)

        self.functionTabWiget = QWidget()
        self.functionTabWiget.setAutoFillBackground(True)
        self.functionTabWiget.setFixedHeight(40)
        self.functionTabWiget.setLayout(layout_top)

        # 左
        self.clearButton = QPushButton(self)
        icon = QIcon(IconTool.buildQIcon('clear.png'))
        self.clearButton.setIcon(icon)
        self.clearButton.setStyleSheet("background:transparent;")
        self.clearButton.clicked.connect(self.clear)
        self.clearButton.setToolTip("Clear the logcat")
        self.clearButton.move(20,10)

        layout_left = QVBoxLayout()
        layout_left.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout_left.setSpacing(1)
        layout_left.addWidget(self.clearButton)
        self.leftWiget = QWidget()
        self.leftWiget.setAutoFillBackground(True)
        self.leftWiget.setLayout(layout_left)
        self.leftWiget.setFixedWidth(30)

        # 右
        self.textEdit = QTextBrowser()
        self.textEdit.setOpenLinks(True)
        self.textEdit.setOpenExternalLinks(True)
        self.textEdit.setReadOnly(True)
        self.messageSplitter = QSplitter(Qt.Horizontal)
        self.messageSplitter.addWidget(self.leftWiget)
        self.messageSplitter.addWidget(self.textEdit)
        self.messageSplitter.setHandleWidth(0)

        self.mainSplitter = QSplitter(Qt.Vertical)
        self.mainSplitter.addWidget(self.functionTabWiget)
        self.mainSplitter.addWidget(self.messageSplitter)
        self.mainSplitter.setHandleWidth(0)
        self.setCentralWidget(self.mainSplitter)

        self.mainSplitter.setStretchFactor(0, 1)
        self.mainSplitter.setStretchFactor(1, 20)

        self.messageSplitter.setStretchFactor(0, 1)
        self.messageSplitter.setStretchFactor(1, 40)

        # 重定向输出
        sys.stdout = ConsoleEmittor(textWritten=self.normalOutputWritten)
        sys.stderr = ConsoleEmittor(textWritten=self.normalOutputWritten)



    def normalOutputWritten(self, text):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        logContent = self.getLogContent(text)
        if self.isConUrl:
            cursor.insertHtml(logContent)
        else:
            cursor.insertText(logContent)
        self.isConUrl = False
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

    def getLogContent(self,text):
        regexUrl = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                           re.IGNORECASE)
        urls = regexUrl.findall(text)
        for url in urls:
            preS = "<a href=\"" + url + "\">" + url + "</a>"
            text = text.replace(url, preS) + "<br/>"
            self.isConUrl = True

        return text

    def clear(self):
        self.textEdit.clear()
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = ConsoleWindow()
    sys.exit(app.exec_())




