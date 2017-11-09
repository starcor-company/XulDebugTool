#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/8 11:17
# @Author  : Mrlsm -- starcor

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from XulDebugTool.ui.BaseWindow import BaseWindow

class SettingWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.qObject = QObject()
        self.initUI()
        self.show()

    def initUI(self):
        self.resize(1000, 650)
        self.initLayout()
        super().initWindow()

    def initLayout(self):
        self.menuList = QListWidget()
        self.infoList = QListWidget()
        self.infoLabel = QLabel()
        self.bottomBtn = QWidget()

        self.infoSplitter = QSplitter(Qt.Vertical)
        self.infoSplitter.addWidget(self.infoLabel)
        self.infoSplitter.addWidget(self.infoList)

        self.mainSplitter = QSplitter(Qt.Horizontal)
        self.mainSplitter.addWidget(self.menuList)
        self.mainSplitter.addWidget(self.infoSplitter)

        self.settingSplitter = QSplitter(Qt.Vertical)
        self.settingSplitter.addWidget(self.mainSplitter)
        self.settingSplitter.addWidget(self.bottomBtn)

        self.setCentralWidget(self.settingSplitter)
        self.mainSplitter.setStretchFactor(1, 3)

        self.infoLabel.setText("Main -> Detail")
        self.infoLabel.setFixedHeight(20)
        self.bottomBtn.setFixedHeight(30)

        self.okBtn = QPushButton(self.tr("OK"))
        self.okBtn.setFixedSize(100, 25)
        self.cancleBtn = QPushButton(self.tr("Cancel"))
        self.cancleBtn.setFixedSize(100, 25)
        self.applyBtn = QPushButton(self.tr("Apply"))
        self.applyBtn.setFixedSize(100, 25)
        hLayout = QHBoxLayout()
        hLayout.addStretch()
        hLayout.addWidget(self.okBtn)
        hLayout.addWidget(self.cancleBtn)
        hLayout.addWidget(self.applyBtn)
        hLayout.setContentsMargins(5, 2, 5, 5)
        self.bottomBtn.setLayout(hLayout)

