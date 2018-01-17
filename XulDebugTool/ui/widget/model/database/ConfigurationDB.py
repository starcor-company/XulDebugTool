# -*- coding: utf-8 -*-

import sqlite3

from PyQt5.QtCore import QObject

from XulDebugTool.ui.widget.model.database.DBManager import DBManager


class ConfigurationDB(QObject):

    @staticmethod
    def saveConfiguration(key ,value):
        if key == None or len(str(key))<1:
            return
        conn = sqlite3.connect('XulDebugTool.db')
        cursor = conn.execute("select count(*) from "+DBManager.TABLE_CONFIGURATION+" where config_key = '"+str(key)+"'");
        for row in cursor:
            count = row[0]
        if count > 0:
            conn.execute("update "+DBManager.TABLE_CONFIGURATION+" set config_value = '"+str(value)+"' where config_key = '"+str(key)+"'")
        else:
            conn.execute("insert into "+DBManager.TABLE_CONFIGURATION+" (config_key,config_value) values('"+str(key)+"','"+str(value)+"')")
        conn.commit()
        conn.close()

    @staticmethod
    def getConfiguration(key):
        if key == None or len(str(key))<1:
            return
        conn = sqlite3.connect('XulDebugTool.db')
        cursor = conn.execute("select * from " + DBManager.TABLE_CONFIGURATION + " where config_key = '" + str(key)+"'");
        result = ''
        for row in cursor:
            result = row[2]
        cursor.close()
        conn.close()
        return result





