#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal

from XulDebugTool.ui.widget.BaseDialog import BaseDialog
from XulDebugTool.ui.widget.model.FavoriteDB import FavoriteDB
from XulDebugTool.utils.XulDebugServerHelper import XulDebugServerHelper

# 查询的model应该从项目支持的mode获取, 但是因为各个项目的provider写的不标准,统一固定这些方式,不是所有的provider都支持这6种
MODES = {'query': 'query-data', 'pull': 'pull-data', 'insert': 'insert-data',
         'delete': 'delete-data', 'update': 'update-data', 'invoke': 'invoke-data'}


class DataQueryDialog(BaseDialog):
    finishSignal = pyqtSignal(str)

    def __init__(self, data):
        self.modes = []
        self.currentRowCount = 0
        if isinstance(data,dict):
            self.data = data
            self.providerId = self.data['@name']
            self.url = ''
            self.providerName = self.data['ds']['@providerClass']
            super().__init__(self.providerName)
            self.initWindow()
            self.url = XulDebugServerHelper.HOST + MODES[
                self.modeComboBox.currentText().lower()] + '/' + self.providerId + '?'
            self.requestLineEdit.setText(self.url)
        else:
            self.data  = data
            self.providerId = ((data.url.rsplit('/',1))[1].split('?',1))[0]
            self.providerName = data.name
            self.url = data.url
            super().__init__(self.providerName)
            self.initWindow()
            self.requestLineEdit.setText(self.url)
        self.favoriteDB = FavoriteDB()

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

        # 查询的mode应该从项目支持的mode获取
        # 但是因为各个项目的provider写的不标准
        # 所以这里统一固定这些方式,不是所有的provider都支持这6种
        # self.modes = self.data['ds']['@mode'].split('|')
        self.modes = MODES
        for model in self.modes.keys():
            self.modeComboBox.addItem(model)

        self.parseUrl2Mode(self.url)
        self.modeComboBox.setMaxVisibleItems(5)
        self.modeComboBox.currentTextChanged.connect(self.onModeChanged)

        self.requestButton = QtWidgets.QPushButton(self)
        self.requestButton.move(350, 15)
        self.requestButton.resize(90, 24)
        self.requestButton.setText('Request')
        self.requestButton.clicked.connect(self.onBtnClicked)

        self.initTableView(self.url)

    def initTableView(self,url):
        row = 1;
        entrys = []
        if url != '' and url != None:
            entrys=url.split('?',1)[1].split('&')
            for element in entrys:
                if element != '' and element != None:
                    row += 1

        self.tableView = QtWidgets.QTableWidget(row,2,self)
        self.tableView.move(36, 80)
        self.tableView.resize(300, 24 * (row+1))
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

        for i, entry in enumerate(entrys):
            if entry != '' and entry != None:
                querylist = entry.split('=')
                self.tableView.setItem(i, 0, QtWidgets.QTableWidgetItem(querylist[0]))
                self.tableView.setItem(i, 1, QtWidgets.QTableWidgetItem(querylist[1]))

        # fill data
        # 初始化查询条件表,预留一行空数据
        for j in range(self.tableView.columnCount()):
            newItem = QtWidgets.QTableWidgetItem('')
            self.tableView.setItem(self.tableView.rowCount()-1, j, newItem)

        self.tableView.cellChanged.connect(self.onCellChanged)


    def parseUrl2Mode(self,url):
        if url != '' and url != None:
            mode = url.rsplit('/', 2)[1].split('-')[0]
            self.modeComboBox.setCurrentText(mode)
        else:
            self.modeComboBox.setCurrentText('query')


    def onModeChanged(self):
        self.url = XulDebugServerHelper.HOST + MODES[self.modeComboBox.currentText().lower()] \
                   + '/' + self.providerId + '?' + self.__getQueryParam()
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
        url = self.url + self.__getQueryParam()
        self.requestLineEdit.setText(url)

    def onBtnClicked(self):
        self.url = XulDebugServerHelper.HOST + MODES[self.modeComboBox.currentText().lower()] \
                   + '/' + self.providerId + '?' + self.__getQueryParam()
        print('data query url: ' + self.url)
        self.treeViewDataRefresh()
        self.finishSignal.emit(self.url)
        self.close()

    def treeViewDataRefresh(self):
        dateTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(time.time()))

        #用左侧的model树来查询的时候
        if isinstance(self.data, dict):
            self.favoriteDB.insertHistory(self.providerName,self.url,dateTime,0)
            # STCLogger.d('dataQuery record is insert to DataBase ' + self.url)
            return

        #用收藏功能里面的记录查询
        if self.data.type:
            if self.data.type == 'favorites_type':#更新收藏记录的时候要先更新历史记录，在更新收藏记录时将最新的历史记录和收藏记录关联起来

                self.favoriteDB.insertHistory(self.providerName, self.url,dateTime, 1)
                rows = self.favoriteDB.selectBySQL('select max(id) from '+ self.favoriteDB.TABLE_HISTORY)
                for row in rows:
                    historyMaxId = row[0]
                self.favoriteDB.updateFavorites('and id = '+ str(self.data.id), name = self.providerName,url = self.url,date = dateTime,history_id = historyMaxId)
                self.favoriteDB.updateHistory('and id = '+str(self.data.historyId), favorite = 0)
            elif self.data.type == 'history_type':
                self.favoriteDB.insertHistory(self.providerName, self.url,dateTime, 0)




    def __getQueryParam(self):
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
        param = param.rsplit('&',1)[0]
        return param

    def setData(self, data):
        self.modes = data['ds']['@mode'].split('|')
        for model in self.modes:
            self.modeComboBox.addItem(model)
        self.providerId = data['@name']
        self.url = XulDebugServerHelper.HOST + self.modeComboBox.currentText() + '/' + self.providerId + '?'
        self.requestLineEdit.setText(self.url)





