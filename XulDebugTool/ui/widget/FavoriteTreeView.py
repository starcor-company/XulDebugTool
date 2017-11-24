import pyperclip
import time
from PyQt5.QtCore import Qt, pyqtSlot, QModelIndex, QPoint
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView, QAbstractItemView, QMenu, QAction

from XulDebugTool.ui.widget.DataQueryDialog import DataQueryDialog
from XulDebugTool.ui.widget.model.FavoriteDB import FavoriteDB
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
            self.favoriteDB = FavoriteDB()
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
            # self.clicked.connect(self.clickState)
        except Exception as e:
            print(e)

    def buildFavoritesTree(self):
        self.favorites.removeRows(0,self.favorites.rowCount())
        rows = self.favoriteDB.selectFavorites(" order by name asc")
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
        rows = self.favoriteDB.selectHistory('order by date desc')
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
            self.favoriteDB.insertHistory(item.name, item.url,dateTime, 1)
            rows = self.favoriteDB.selectBySQL('select max(id) from ' + self.favoriteDB.TABLE_HISTORY)
            for row in rows:
                historyMaxId = row[0]

            self.favoriteDB.updateFavorites('and id = '+ str(item.id), name = item.name,url = item.url,date = dateTime, history_id=historyMaxId)
            self.favoriteDB.updateHistory('and id = ' + str(item.historyId), favorite=1)
            self.mainWindow.onGetQueryUrl(item.url)
        elif item.type == ITEM_TYPE_HISTORY:
            self.favoriteDB.insertHistory(item.name, item.url, dateTime, 0)
            self.mainWindow.onGetQueryUrl(item.url)

    @pyqtSlot(QPoint)
    def openContextMenu(self, point):
        index = self.indexAt(point)
        if not index.isValid():
            return
        item = self.treeModel.itemFromIndex(index)
        menu = QMenu()

        if item.type == ITEM_TYPE_HISTORY:
            queryAction = QAction(IconTool.buildQIcon('data.png'), '&Edit ...', self,triggered=lambda: self.showQueryDialog(item))
            queryAction.setShortcut('Alt+E')
            menu.addAction(queryAction)

            favoritesAction = QAction(IconTool.buildQIcon('star.png'),'Add to &favorites',self,triggered = lambda: self.add2Favorites(item))
            favoritesAction.setShortcut('Alt+F')
            menu.addAction(favoritesAction)

            deleteAction = QAction(IconTool.buildQIcon('clear.png'),'&Delete',self,triggered = lambda: self.deleteHistory(item))
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


    def showQueryDialog(self,item):
        self.dialog = DataQueryDialog(item)
        self.dialog.finishSignal.connect(self.mainWindow.onGetQueryUrl)
        self.dialog.show()

    def add2Favorites(self,item):
        if item.type == ITEM_TYPE_HISTORY:
            dateTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(time.time()))
            self.favoriteDB.insertFavorites(item.name,item.url,dateTime,item.id)
            self.updateTree()

    def deleteFavorite(self,item):
        if item.type == ITEM_TYPE_FAVORITES:
            self.favoriteDB.deleteFavorites('and id = ' + str(item.id))
            self.favoriteDB.deleteHistory(' and id = '+ str(item.historyId))
            self.updateTree()

    def deleteHistory(self,item):
        if item.type == ITEM_TYPE_HISTORY:
            self.favoriteDB.deleteHistory('and id = '+str(item.id))
            self.updateTree()

    def remove2Favorites(self,item):
        if item.type == ITEM_TYPE_FAVORITES:
            self.favoriteDB.deleteFavorites('and id = '+str(item.id))
            self.updateTree()

    def updateTree(self):
        self.buildFavoritesTree()
        self.buildQueryHistory()




