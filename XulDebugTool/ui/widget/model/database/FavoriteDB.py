
# -*- coding: utf-8 -*-
import sqlite3

from PyQt5.QtCore import QObject

from XulDebugTool.ui.widget.model.database.DBManager import DBManager


class FavoriteDB(QObject):

    #插入数据的时候，判断之前为收藏的历史记录是否超过100条，超过就删除最早的历史记录
    @staticmethod
    def insertHistory(name,url,dateTime,isFavorite):
        conn = sqlite3.connect('XulDebugTool.db')
        conn.execute(
            "insert into "+DBManager.TABLE_HISTORY+" (name,url,date,favorite) values('" + name + "','" + url + "','" + dateTime + "'," + str(
                isFavorite) + ")")
        conn.commit()
        cursor = conn.execute("select count(*) as count from "+DBManager.TABLE_HISTORY)
        for row in cursor:
            count = row[0]
        if count > 100:
            cursor = conn.execute("select id from "+DBManager.TABLE_HISTORY+" limit " + str(count - 100) + " offset 0")
            idString = ''
            for row in cursor:
                idString += str(row[0]) + ','
            idString = idString.rsplit(',', 1)[0]
            conn.execute("delete from "+DBManager.TABLE_HISTORY+" where id in (" + idString + ")")
            conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def insertFavorites(name,url,dateTime,history_id):
        conn = sqlite3.connect('XulDebugTool.db')
        conn.execute("insert into "+DBManager.TABLE_FAVORITES+" (name,url,date,history_id) values('" + name + "','" + url + "','" + dateTime + "'," + str(history_id) + ")")
        conn.commit()
        conn.close()

    @staticmethod
    def selectHistory(sentence = ''):
        conn = sqlite3.connect('XulDebugTool.db')
        if sentence != '' and sentence != None:
            cursor = conn.execute("select * from "+DBManager.TABLE_HISTORY+" where 1 = 1 "+ sentence)
        else:
            cursor = conn.execute("select * from "+DBManager.TABLE_HISTORY+" order by id desc")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def selectFavorites(sentence = ''):
        conn = sqlite3.connect('XulDebugTool.db')
        if sentence != '' and sentence != None:
            cursor = conn.execute("select * from "+DBManager.TABLE_FAVORITES+" where 1 = 1 "+ sentence)
        else:
            cursor = conn.execute("select * from "+DBManager.TABLE_FAVORITES+" order by id desc")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def selectBySQL(sql):
        conn = sqlite3.connect('XulDebugTool.db')
        cursor = conn.execute(sql)
        result = cursor.fetchall()
        return result

    @staticmethod
    def updateHistory(clauseSentence,**update):
        entry = update
        sentence = ''
        for key in entry.keys():
            sentence += ","+key + " = \'" + str(entry[key])+ "\' "
        sentence = sentence.split(',', 1)[1]
        conn = sqlite3.connect('XulDebugTool.db')
        conn.execute("update "+DBManager.TABLE_HISTORY+" set " + sentence + " where 1 = 1 " + clauseSentence )
        conn.commit()
        conn.close()

    @staticmethod
    def updateFavorites(clauseSentence,**update):
        entry = update
        sentence = ''
        for key in entry.keys():
            sentence += ","+key + " = \'" + str(entry[key])+ "\' "
        sentence = sentence.split(',', 1)[1]
        conn = sqlite3.connect('XulDebugTool.db')
        conn.execute("update "+DBManager.TABLE_FAVORITES+" set " + sentence + " where 1 = 1 " + clauseSentence )
        conn.commit()
        conn.close()

    @staticmethod
    def deleteHistory(sentence = ''):
        conn = sqlite3.connect('XulDebugTool.db')
        if sentence != '' and sentence != None:
            conn.execute("delete from "+DBManager.TABLE_HISTORY+" where 1 = 1 " + sentence)
        else:
            conn.execute("delete from "+DBManager.TABLE_HISTORY)
        conn.commit()
        conn.close()

    @staticmethod
    def deleteHistoryBatch( list):
        conn = sqlite3.connect('XulDebugTool.db')
        ids = ""
        for item in list:
            if ids == "":
                ids = str(item.id)
            else:
                ids = ids +","+ str(item.id)
        conn.execute("delete from "+DBManager.TABLE_HISTORY+" where id in (" + ids+")")
        conn.commit()
        conn.close()

    @staticmethod
    def deleteFavorites(sentence = ''):
        conn = sqlite3.connect('XulDebugTool.db')
        if sentence != '' and sentence != None:
            conn.execute("delete from "+DBManager.TABLE_FAVORITES+" where 1 = 1 " + sentence)
        else:
            conn.execute("delete from "+DBManager.TABLE_FAVORITES)
        conn.commit()
        conn.close()

    @staticmethod
    def deleteFavoritesBatch(list):
        conn = sqlite3.connect('XulDebugTool.db')
        ids = ""
        for item in list:
            if ids == "":
                ids = str(item.id)
            else:
                ids = ids +","+ str(item.id)
        conn.execute("delete from "+DBManager.TABLE_FAVORITES+" where id in (" + ids+")")
        conn.commit()
        conn.close()



