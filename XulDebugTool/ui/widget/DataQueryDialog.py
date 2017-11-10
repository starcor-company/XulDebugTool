#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot

from XulDebugTool.ui.widget.BaseDialog import BaseDialog
from XulDebugTool.utils.XulDebugServerHelper import XulDebugServerHelper


class DataQueryDialog(BaseDialog):
    def __init__(self):
        super().__init__('Data Query')
        self.providerId = ''
        self.modes = []
        self.initWindow()
        self.url = ''

    def initWindow(self):
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
        self.modeComboBox.move(187, 44)
        self.modeComboBox.resize(130, 24)
        self.modeComboBox.setEditable(False)
        self.modeComboBox.setCurrentText('query')
        self.modeComboBox.setMaxVisibleItems(5)
        # self.modeComboBox.setFrame(True)

        self.execButton = QtWidgets.QPushButton(self)
        self.execButton.move(350, 15)
        self.execButton.resize(90, 24)
        self.execButton.setText('Request')

        self.tableView = QtWidgets.QTableWidget(1, 2, self)
        self.tableView.move(36, 80)
        self.tableView.resize(300, 24 * 2)
        self.tableView.setColumnWidth(0, 150)
        self.tableView.setColumnWidth(1, 150)
        self.tableView.horizontalHeader().setFixedHeight(24)
        self.tableView.horizontalHeader().setStyleSheet("QHeaderView::section{background:lightblue;}");
        self.tableView.verticalHeader().setDefaultSectionSize(24)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setHorizontalHeaderLabels(['where', 'is'])
        self.tableView.setFrameStyle(QtWidgets.QTableWidget.NoFrame)
        self.tableView.setShowGrid(True)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # 初始化查询条件表, 一行,两列
        for i in range(self.tableView.rowCount()):
            for j in range(self.tableView.columnCount()):
                newItem = QtWidgets.QTableWidgetItem('')
                self.tableView.setItem(i, j, newItem)
        self.tableView.cellChanged.connect(self.onCellChanged)

        self.currentRowCount = 0

    def onCellChanged(self):
        # 当单元格变化的时候检测需不需要新增一行
        item = self.tableView.currentItem()
        if item.text():
            if item.column() == 0:
                brother = self.tableView.item(self.currentRowCount, 1)
            else:
                brother = self.tableView.item(self.currentRowCount, 0)
            # 当前节点和兄弟节点都有值的时候新增一行
            if brother and brother.text():
                self.currentRowCount += 1
                row = self.tableView.rowCount()
                self.tableView.insertRow(row)
                self.tableView.setItem(row, 0, QtWidgets.QTableWidgetItem())
                self.tableView.setItem(row, 1, QtWidgets.QTableWidgetItem())
                # 加上表头,不超过7行,超过滚动条显示
                if (self.currentRowCount + 2) <= 7:
                    self.tableView.resize(300, 24 * (self.currentRowCount + 2))
                else:
                    self.tableView.resize(322, 24 * 7)

        # 获取所有行的数据,组成查询条件
        queryClause = {}
        for i in range(self.tableView.rowCount()):
            for j in range(self.tableView.columnCount()):
                item = self.tableView.item(i, j)
                if item:
                    if j == 0:
                        whereClause = item.text()
                    else:
                        isClause = item.text()
            if whereClause and isClause:
                queryClause[whereClause] = isClause
        param = ''
        for k, v in queryClause.items():
            param += (k + '=' + v + '&')
        url = self.url + param
        self.requestLineEdit.setText(url)

    def setData(self, data):
        self.modes = data['ds']['@mode'].split('|')
        for model in self.modes:
            self.modeComboBox.addItem(model)
        self.providerId = data['@name']
        self.url = XulDebugServerHelper.HOST + self.modeComboBox.currentText() + '/' + self.providerId + '?'
        self.requestLineEdit.setText(self.url)
