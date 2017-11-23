
# -*- coding: utf-8 -*-
import sqlite3
import time

from PyQt5.QtCore import QObject


class FavoriteDB(QObject):
    def __init__(self):
        conn = sqlite3.connect('XulDebugTool.db');
        cursor = conn.cursor();
        # cursor.execute("drop table favorite")
        cursor.execute('create table if not exists favorite (id integer primary key not null, name nvarchar(50) null,url nvarchar(512) null,date nvarchar(50) null,favorite binary(1) default 0 )')
        cursor.close()
        conn.close()

    #插入数据的时候，判断之前为收藏的历史记录是否超过100条，超过就删除最早的历史记录
    def insertFavorite(self,name,url,isFavorite):
        conn = sqlite3.connect('XulDebugTool.db');

        dateTime =time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(time.time()))

        conn.execute("insert into favorite (name,url,date,favorite) values('" + name + "','" + url + "','" + dateTime + "',"+str(isFavorite)+")")
        conn.commit()

        cursor = conn.execute("select count(*) as count from favorite")
        for row in cursor:
            count = row[0]
        if count > 100:
            cursor = conn.execute("select id from favorite limit "+ str(count-10)+" offset 0")
            idString = ''
            for row in cursor:
                idString += str(row[0])+','
            idString = idString.rsplit(',',1)[0]
            conn.execute("delete from favorite where id in ("+idString+")")
            conn.commit()
        cursor.close()
        conn.close()

    def selectFavorites(self,sentence = ''):
        conn = sqlite3.connect('XulDebugTool.db');
        if sentence != '' and sentence != None:
            cursor = conn.execute("select * from favorite where "+ sentence)
        else:
            cursor = conn.execute("select * from favorite order by id desc")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def updateFavorites(self,id,**update):
        entry = update
        sentence = ''
        for key in entry.keys():
            sentence += key + " = " + str(entry[key])+ ","
        sentence = sentence.rsplit(',', 1)[0]
        conn = sqlite3.connect('XulDebugTool.db');
        conn.execute("update favorite set " + sentence + " where id = " + str(id))

        conn.commit()
        conn.close()

    def deleteFavorites(self,sentence = ''):
        conn = sqlite3.connect('XulDebugTool.db');
        if sentence != '' and sentence != None:
            conn.execute("delete from favorite where " + sentence)
        else:
            conn.execute("delete from favorite")
        conn.commit()
        conn.close()
        pass




