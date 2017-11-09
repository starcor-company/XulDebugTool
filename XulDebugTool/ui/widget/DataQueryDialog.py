#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot

from XulDebugTool.ui.widget.BaseDialog import BaseDialog


class DataQueryDialog(BaseDialog):
    def __init__(self):
        super().__init__('Data Query')
        self.providerId = ''
        self.modes = []
        self.paramCount = 1
        self.initWindow1()

    def initWindow1(self):
        super().initWindow()
        self.setFixedSize(466, 256)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.requestLineEdit = QtWidgets.QLineEdit(self)
        self.requestLineEdit.move(36, 15)
        self.requestLineEdit.resize(300, 24)

        self.modeLable = QtWidgets.QLabel(self)
        self.modeLable.move(36, 44)
        self.modeLable.resize(130, 24)
        self.modeLable.setText('Mode:')

        self.modeComboBox = QtWidgets.QComboBox(self)
        self.modeComboBox.move(160, 44)
        self.modeComboBox.resize(130, 24)
        self.modeComboBox.setEditable(False)
        self.modeComboBox.setCurrentText('query')
        self.modeComboBox.setMaxVisibleItems(5)
        # self.modeComboBox.setFrame(True)

        self.execButton = QtWidgets.QPushButton(self)
        self.execButton.move(350, 15)
        self.execButton.resize(90, 24)
        self.execButton.setText('Request')

        self.tableView = QtWidgets.QTableWidget(self)
        self.tableView.move(36, 80)
        self.tableView.resize(300, 24 * 2)
        self.tableView.setColumnCount(2)
        self.tableView.setColumnWidth(0, 150)
        self.tableView.setColumnWidth(1, 150)
        self.tableView.setRowCount(1)
        self.tableView.horizontalHeader().setFixedHeight(24)
        self.tableView.horizontalHeader().setStyleSheet("QHeaderView::section{background:lightblue;}");
        self.tableView.verticalHeader().setDefaultSectionSize(24)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setHorizontalHeaderLabels(['where', 'is'])
        self.tableView.setFrameStyle(QtWidgets.QTableWidget.NoFrame)
        self.tableView.setShowGrid(True)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.cellChanged.connect(self.onCellChanged)

        self.currentRowCount = 0

    def onCellChanged(self):
        item = self.tableView.currentItem()
        brother = QtWidgets.QTableWidgetItem()
        if item.text():
            if item.column() == 0:
                brother = self.tableView.itemAt(self.currentRowCount, 1)
            else:
                brother = self.tableView.itemAt(self.currentRowCount, 0)
            if brother.text():
                self.currentRowCount += 1
                self.tableView.insertRow(self.currentRowCount)
                # if ((self.currentRowCount + 2) <= 5):
                self.tableView.resize(300, 24 * (self.currentRowCount + 2))

        print(item.text(), item.row(), item.column())
        print(brother.text(), brother.row(), brother.column())

    def initWindow(self):
        super().initWindow()
        self.setFixedSize(466, 256)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.widget = QtWidgets.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(330, 40, 95, 81))

        self.addParamButton = QtWidgets.QPushButton(self.widget)
        self.addParamButton.setText("Add Param")
        self.addParamButton.clicked.connect(self.onAddParamClick)
        self.execButton = QtWidgets.QPushButton(self.widget)
        self.execButton.setText("Execute")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.addWidget(self.addParamButton)
        self.verticalLayout.addWidget(self.execButton)

        self.widget1 = QtWidgets.QWidget(self)
        self.widget1.setGeometry(QtCore.QRect(30, 40, 251, 51))
        self.modeLabel = QtWidgets.QLabel(self.widget1)
        self.modeLabel.setText("Mode:")
        self.modeComboBox = QtWidgets.QComboBox(self.widget1)
        self.modeComboBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.modeComboBox.setEditable(False)
        self.modeComboBox.setCurrentText("")
        self.modeComboBox.setMaxVisibleItems(5)
        self.modeComboBox.setFrame(True)
        self.modeComboBox.setObjectName("modeComboBox")
        self.whereLabel = QtWidgets.QLabel(self.widget1)
        self.whereLabel.setText("where")
        self.isLabel = QtWidgets.QLabel(self.widget1)
        self.isLabel.setText("is")

        self.gridLayout = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.addWidget(self.modeLabel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.modeComboBox, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.whereLabel, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.isLabel, 1, 1, 1, 1)
        self.gridLayout.setGeometry(QtCore.QRect(30, 41, 251, 51))

        self.widget2 = QtWidgets.QWidget(self)
        self.widget2.setGeometry(QtCore.QRect(30, 90, 251, 23))

        self.whereLineEdit0 = QtWidgets.QLineEdit(self.widget2)
        self.whereLineEdit0.setFixedSize(120, 20)
        self.isLneEdit0 = QtWidgets.QLineEdit(self.widget2)
        self.isLneEdit0.setFixedSize(120, 20)
        self.paramGridLayout = QtWidgets.QGridLayout(self.widget2)
        self.paramGridLayout.setContentsMargins(0, 0, 0, 0)
        self.paramGridLayout.addWidget(self.whereLineEdit0, 0, 0, QtCore.Qt.AlignTop)
        self.paramGridLayout.addWidget(self.isLneEdit0, 0, 1, QtCore.Qt.AlignTop)

    def setData(self, data):
        self.modes = data['ds']['@mode'].split('|')
        for model in self.modes:
            self.modeComboBox.addItem(model)
        self.providerId = data['@name']

    @pyqtSlot()
    def onAddParamClick(self):
        whereLineEdit = QtWidgets.QLineEdit(self.widget2)
        whereLineEdit.setFixedSize(120, 20)
        isLneEdit = QtWidgets.QLineEdit(self.widget2)
        isLneEdit.setFixedSize(120, 20)
        self.paramGridLayout.addWidget(whereLineEdit, self.paramCount, 0, QtCore.Qt.AlignTop)
        self.paramGridLayout.addWidget(isLneEdit, self.paramCount, 1, QtCore.Qt.AlignTop)
        self.paramCount += 1
        self.widget2.setGeometry(QtCore.QRect(30, 90, 251, 30 * self.paramCount))
