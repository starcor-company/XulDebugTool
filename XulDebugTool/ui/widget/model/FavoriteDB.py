
# -*- coding: utf-8 -*-
import sqlite3

from PyQt5.QtCore import QObject


class FavoriteDB(QObject):

    TABLE_FAVORITES = 'favorites'
    TABLE_HISTORY = 'history_query'

    def __init__(self):
        conn = sqlite3.connect('XulDebugTool.db')
        cursor = conn.cursor()
        # cursor.execute("drop table favorite")
        cursor.execute('create table if not exists history_query (id integer primary key not null, name nvarchar(50) null,url nvarchar(512) null,date TIMESTAMP null,favorite binary(1) default 0)')
        cursor.execute('create table if not exists favorites (id integer primary key not null, name nvarchar(50) null,url nvarchar(512) null,date TIMESTAMP null,history_id integer not null,UNIQUE(history_id),FOREIGN KEY (history_id) REFERENCES history_query(id))')
        cursor.close()
        conn.close()

    #插入数据的时候，判断之前为收藏的历史记录是否超过100条，超过就删除最早的历史记录
    def insertHistory(self,name,url,dateTime,isFavorite):
        conn = sqlite3.connect('XulDebugTool.db')
        conn.execute(
            "insert into history_query (name,url,date,favorite) values('" + name + "','" + url + "','" + dateTime + "'," + str(
                isFavorite) + ")")
        conn.commit()
        cursor = conn.execute("select count(*) as count from history_query")
        for row in cursor:
            count = row[0]
        if count > 100:
            cursor = conn.execute("select id from history_query limit " + str(count - 100) + " offset 0")
            idString = ''
            for row in cursor:
                idString += str(row[0]) + ','
            idString = idString.rsplit(',', 1)[0]
            conn.execute("delete from history_query where id in (" + idString + ")")
            conn.commit()
        cursor.close()
        conn.close()

    def insertFavorites(self,name,url,dateTime,history_id):
        conn = sqlite3.connect('XulDebugTool.db')
        conn.execute("insert into favorites (name,url,date,history_id) values('" + name + "','" + url + "','" + dateTime + "'," + str(history_id) + ")")
        conn.commit()
        conn.close()

    def selectHistory(self,sentence = ''):
        conn = sqlite3.connect('XulDebugTool.db')
        if sentence != '' and sentence != None:
            cursor = conn.execute("select * from history_query where 1 = 1 "+ sentence)
        else:
            cursor = conn.execute("select * from history_query order by id desc")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def selectFavorites(self,sentence = ''):
        conn = sqlite3.connect('XulDebugTool.db')
        if sentence != '' and sentence != None:
            cursor = conn.execute("select * from favorites where 1 = 1 "+ sentence)
        else:
            cursor = conn.execute("select * from favorites order by id desc")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def selectBySQL(self,sql):
        conn = sqlite3.connect('XulDebugTool.db')
        cursor = conn.execute(sql)
        result = cursor.fetchall()
        return result

    def updateHistory(self,clauseSentence,**update):
        entry = update
        sentence = ''
        for key in entry.keys():
            sentence += ","+key + " = \'" + str(entry[key])+ "\' "
        sentence = sentence.split(',', 1)[1]
        conn = sqlite3.connect('XulDebugTool.db')
        conn.execute("update history_query set " + sentence + " where 1 = 1 " + clauseSentence )
        conn.commit()
        conn.close()

    def updateFavorites(self,clauseSentence,**update):
        entry = update
        sentence = ''
        for key in entry.keys():
            sentence += ","+key + " = \'" + str(entry[key])+ "\' "
        sentence = sentence.split(',', 1)[1]
        conn = sqlite3.connect('XulDebugTool.db')
        conn.execute("update favorites set " + sentence + " where 1 = 1 " + clauseSentence )
        conn.commit()
        conn.close()

    def deleteHistory(self,sentence = ''):
        conn = sqlite3.connect('XulDebugTool.db')
        if sentence != '' and sentence != None:
            conn.execute("delete from history_query where 1 = 1 " + sentence)
        else:
            conn.execute("delete from history_query")
        conn.commit()
        conn.close()

    def deleteHistoryBatch(self, list):
        conn = sqlite3.connect('XulDebugTool.db')
        ids = ""
        for item in list:
            if ids == "":
                ids = str(item.id)
            else:
                ids = ids +","+ str(item.id)
        conn.execute("delete from history_query where id in (" + ids+")")
        conn.commit()
        conn.close()

    def deleteFavorites(self,sentence = ''):
        conn = sqlite3.connect('XulDebugTool.db')
        if sentence != '' and sentence != None:
            conn.execute("delete from favorites where 1 = 1 " + sentence)
        else:
            conn.execute("delete from favorites")
        conn.commit()
        conn.close()

    def deleteFavoritesBatch(self,list):
        conn = sqlite3.connect('XulDebugTool.db')
        ids = ""
        for item in list:
            if ids == "":
                ids = str(item.id)
            else:
                ids = ids +","+ str(item.id)
        conn.execute("delete from favorites where id in (" + ids+")")
        conn.commit()
        conn.close()



