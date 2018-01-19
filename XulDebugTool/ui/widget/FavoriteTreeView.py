import time

import pyperclip
from PyQt5.QtCore import Qt, pyqtSlot, QModelIndex, QPoint
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QCursor
from PyQt5.QtWidgets import QTreeView, QAbstractItemView, QMenu, QAction

from XulDebugTool.logcatapi.Logcat import STCLogger
from XulDebugTool.ui.widget.DataQueryDialog import DataQueryDialog
from XulDebugTool.ui.widget.model.database.FavoriteDB import FavoriteDB
from XulDebugTool.utils.IconTool import IconTool

ROOT_PROVIDERQUERYHISTORY = "History"
ROOT_FAVORITES = "Favorites"

ITEM_TYPE_FAVORITES = 'favorites_type'
ITEM_TYPE_HISTORY = 'history_type'
ITEM_TYPE_URL = 'url_type'

class FavoriteTreeView(QTreeView):
    def __init__(self,window, parent=None):
        self.mainWindow = window
        try:
            super(FavoriteTreeView,self).__init__(parent)
            self.treeModel = QStandardItemModel()
            self.favorites = QStandardItem(ROOT_FAVORITES)
            self.buildFavoritesTree()
            self.providerQueryHistory = QStandardItem(ROOT_PROVIDERQUERYHISTORY)
            self.buildQueryHistory()
            self.treeModel.appendColumn([self.favorites,self.providerQueryHistory])
            self.treeModel.setHeaderData(0, Qt.Horizontal, 'Record')

            self.setModel(self.treeModel)
            self.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.openContextMenu)
            self.doubleClicked.connect(self.onTreeItemDoubleClicked)
            self.setSelectionBehavior(QAbstractItemView.SelectItems)
            # 设置该控件可以多选
            self.setSelectionMode(QAbstractItemView.ExtendedSelection)
            # self.clicked.connect(self.clickState)
        except Exception as e:
            STCLogger().e(e)

    def buildFavoritesTree(self):
        self.favorites.removeRows(0,self.favorites.rowCount())
        rows = FavoriteDB.selectFavorites(" order by name asc")
        for row in rows:
            providerItem = QStandardItem(row[1] + "   " + row[3])
            providerItem.type = ITEM_TYPE_FAVORITES
            providerItem.id = row[0]
            providerItem.name = row[1]
            providerItem.url = row[2]
            providerItem.date = row[3]
            providerItem.historyId = row[4]
            urlItem = QStandardItem(row[2])
            urlItem.type = ITEM_TYPE_URL
            providerItem.appendRow(urlItem)
            self.favorites.appendRow(providerItem)

    def buildQueryHistory(self):
        self.providerQueryHistory.removeRows(0,self.providerQueryHistory.rowCount())
        rows = FavoriteDB.selectHistory('order by date desc')
        for row in rows:
            providerItem = QStandardItem(row[1]+"   "+row[3])
            providerItem.type = ITEM_TYPE_HISTORY
            providerItem.id = row[0]
            providerItem.name = row[1]
            providerItem.url = row[2]
            providerItem.date = row[3]
            providerItem.favorite = row[4]
            urlItem = QStandardItem(row[2])
            urlItem.type = ITEM_TYPE_URL
            providerItem.appendRow(urlItem)
            self.providerQueryHistory.appendRow(providerItem)


    @pyqtSlot(QModelIndex)
    def onTreeItemDoubleClicked(self, index):
        item = self.treeModel.itemFromIndex(index)
        dateTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(time.time()))
        if item.type == ITEM_TYPE_FAVORITES :#更新收藏记录的时候要先更新历史记录，在更新收藏记录时将最新的历史记录和收藏记录关联起来
            FavoriteDB.insertHistory(item.name, item.url,dateTime, 1)
            rows = FavoriteDB.selectBySQL('select max(id) from ' + FavoriteDB.TABLE_HISTORY)
            for row in rows:
                historyMaxId = row[0]

            FavoriteDB.updateFavorites('and id = '+ str(item.id), name = item.name,url = item.url,date = dateTime, history_id=historyMaxId)
            FavoriteDB.updateHistory('and id = ' + str(item.historyId), favorite=1)
            self.mainWindow.onGetQueryUrl(item.url)
        elif item.type == ITEM_TYPE_HISTORY:
            FavoriteDB.insertHistory(item.name, item.url, dateTime, 0)
            self.mainWindow.onGetQueryUrl(item.url)

    @pyqtSlot(QPoint)
    def openContextMenu(self,point):
        list = self.selectedIndexes()
        if len(list) > 1:
            self.menuBatchOperation(list)
        elif len(list) == 1:
            self.menuOperation(point)

    def menuOperation(self,point):
        index = self.indexAt(point)
        if not index.isValid():
            return
        item = self.treeModel.itemFromIndex(index)
        menu = QMenu()

        if item.type == ITEM_TYPE_HISTORY:
            queryAction = QAction(IconTool.buildQIcon('data.png'), '&Edit ...', self,triggered=lambda: self.showQueryDialog(item))
            queryAction.setShortcut('Alt+E')
            menu.addAction(queryAction)

            favoritesAction = QAction(IconTool.buildQIcon('star.png'), 'Add to &favorites', self,triggered=lambda: self.add2Favorites(item))
            favoritesAction.setShortcut('Alt+F')
            menu.addAction(favoritesAction)

            deleteAction = QAction(IconTool.buildQIcon('clear.png'), '&Delete', self,triggered=lambda: self.deleteHistory(item))
            deleteAction.setShortcut('Ctrl+D')
            menu.addAction(deleteAction)

        if item.type == ITEM_TYPE_FAVORITES:
            queryAction = QAction(IconTool.buildQIcon('data.png'), '&Edit ...', self,triggered=lambda: self.showQueryDialog(item))
            queryAction.setShortcut('Alt+E')
            menu.addAction(queryAction)

            disFavoritesAction = QAction(IconTool.buildQIcon('remove_favorites.png'), 'Remove from &favorites', self,triggered=lambda: self.remove2Favorites(item))
            disFavoritesAction.setShortcut('Alt+F')
            menu.addAction(disFavoritesAction)

            deleteAction = QAction(IconTool.buildQIcon('clear.png'), '&Delete', self,triggered=lambda: self.deleteFavorite(item))
            deleteAction.setShortcut('Ctrl+D')
            menu.addAction(deleteAction)

        if item.type == ITEM_TYPE_URL:
            copyAction = QAction(IconTool.buildQIcon('copy.png'), 'Copy', self,triggered=lambda: pyperclip.copy('%s' % index.data()))
            copyAction.setShortcut('Ctrl+C')
            menu.addAction(copyAction)

        menu.exec_(self.viewport().mapToGlobal(point))

    def menuBatchOperation(self,list):
        itemList = []
        #标记本次批量操作所有记录的类别是否一致，如果不一致就不进行右键批量操作
        itemTpye = None;
        for modelIndex in list:
            item = self.treeModel.itemFromIndex(modelIndex)
            if itemTpye != None:
                if itemTpye != item.type:
                    return
            itemTpye = item.type
            itemList.append(item)

        menu = QMenu()
        if itemTpye == ITEM_TYPE_HISTORY:
            deleteAction = QAction(IconTool.buildQIcon('clear.png'), '&Delete', self,triggered=lambda: self.deleteHistoryBatch(itemList))
            deleteAction.setShortcut('Ctrl+D')
            menu.addAction(deleteAction)

        if itemTpye == ITEM_TYPE_FAVORITES:
            deleteAction = QAction(IconTool.buildQIcon('clear.png'), '&Delete', self,triggered=lambda: self.deleteFavoritesBatch(itemList))
            deleteAction.setShortcut('Ctrl+D')
            menu.addAction(deleteAction)

        menu.exec_(QCursor.pos())

    def showQueryDialog(self,item):
        self.dialog = DataQueryDialog(item)
        self.dialog.finishSignal.connect(self.mainWindow.onGetQueryUrl)
        self.dialog.show()
        STCLogger().i('show queryDataDialog' )

    def add2Favorites(self,item):
        if item.type == ITEM_TYPE_HISTORY:
            dateTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(time.time()))
            FavoriteDB.insertFavorites(item.name,item.url,dateTime,item.id)
            STCLogger().i('the history record add to DataBase of favorites :' + item.url)
            self.updateTree()

    def deleteFavorite(self,item):
        if item.type == ITEM_TYPE_FAVORITES:
            FavoriteDB.deleteFavorites('and id = ' + str(item.id))
            FavoriteDB.deleteHistory(' and id = '+ str(item.historyId))
            STCLogger().i('this record delete from DataBase:' + item.url)
            self.updateTree()

    def deleteFavoritesBatch(self,list):
        FavoriteDB.deleteFavoritesBatch(list)
        STCLogger().i('A batch of favorite records was deleted')
        self.updateTree()

    def deleteHistory(self,item):
        if item.type == ITEM_TYPE_HISTORY:
            FavoriteDB.deleteHistory('and id = '+str(item.id))
            STCLogger().i('this record delete from DataBase:' + item.url)
            self.updateTree()

    def deleteHistoryBatch(self,list):
        FavoriteDB.deleteHistoryBatch(list)
        STCLogger().i('A batch of historical records was deleted')
        self.updateTree()

    def remove2Favorites(self,item):
        if item.type == ITEM_TYPE_FAVORITES:
            FavoriteDB.deleteFavorites('and id = '+str(item.id))
            STCLogger().i('this record remove from DataBase of favorites:' + item.url)
            self.updateTree()

    def updateTree(self):
        self.buildFavoritesTree()
        self.buildQueryHistory()




