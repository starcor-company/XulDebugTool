#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot

from XulDebugTool.ui.widget.BaseDialog import BaseDialog
from XulDebugTool.utils.XulDebugServerHelper import XulDebugServerHelper

# 查询的model应该从项目支持的mode获取, 但是因为各个项目的provider写的不标准,统一固定这些方式,不是所有的provider都支持这5种
MODES = ['query', 'pull', 'insert', 'delete', 'update']


class DataQueryDialog(BaseDialog):
    def __init__(self, data):
        self.data = data
        self.providerId = self.data['@name']
        self.url = ''
        self.modes = []
        self.currentRowCount = 0
        self.providerName = self.data['ds']['@providerClass']

        super().__init__(self.providerName)
        self.initWindow()

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
        self.modeComboBox.resize(150, 24)
        self.modeComboBox.setEditable(False)
        self.modeComboBox.setCurrentText('query')
        self.modeComboBox.setMaxVisibleItems(5)
        self.modeComboBox.currentTextChanged.connect(self.onModeChanged)

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

        # fill data
        # 初始化查询条件表, 一行,两列
        for i in range(self.tableView.rowCount()):
            for j in range(self.tableView.columnCount()):
                newItem = QtWidgets.QTableWidgetItem('')
                self.tableView.setItem(i, j, newItem)
        self.tableView.cellChanged.connect(self.onCellChanged)

        # 查询的mode应该从项目支持的mode获取
        # 但是因为各个项目的provider写的不标准
        # 所以这里统一固定这些方式,不是所有的provider都支持这5种
        # self.modes = self.data['ds']['@mode'].split('|')
        self.modes = MODES
        for model in self.modes:
            self.modeComboBox.addItem(model)
        self.url = XulDebugServerHelper.HOST + self.modeComboBox.currentText() + '/' + self.providerId + '?'
        self.requestLineEdit.setText(self.url)

    def onModeChanged(self):
        self.url = XulDebugServerHelper.HOST + self.modeComboBox.currentText() \
                   + '/' + self.providerId + '?' + self.getQueryParam()
        self.requestLineEdit.setText(self.url)

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
        url = self.url + self.getQueryParam()
        self.requestLineEdit.setText(url)

    def getQueryParam(self):
        # 获取所有查询条件,并组装成查询参数
        param = ''
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
        for k, v in queryClause.items():
            param += (k + '=' + v + '&')
        return param

    def setData(self, data):
        self.modes = data['ds']['@mode'].split('|')
        for model in self.modes:
            self.modeComboBox.addItem(model)
        self.providerId = data['@name']
        self.url = XulDebugServerHelper.HOST + self.modeComboBox.currentText() + '/' + self.providerId + '?'
        self.requestLineEdit.setText(self.url)
