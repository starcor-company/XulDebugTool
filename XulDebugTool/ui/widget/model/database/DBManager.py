# -*- coding: utf-8 -*-
import sqlite3


class DBManager(object):
    TABLE_DEVICE = "device"
    TABLE_LOGIN = "login"
    TABLE_CONFIGURATION = 'configuration'
    TABLE_FAVORITES = 'favorites'
    TABLE_HISTORY = 'history_query'

    @staticmethod
    def createTable():
        conn = sqlite3.connect('XulDebugTool.db')
        cursor = conn.cursor()
        cursor.execute('create table if not exists '+DBManager.TABLE_DEVICE+' (name varchar(50) primary key)')
        cursor.execute('create table if not exists '+DBManager.TABLE_LOGIN+' (name varchar(50) primary key)')
        cursor.execute('create table if not exists '+DBManager.TABLE_HISTORY+'(id integer primary key autoincrement, name nvarchar(50) null,url nvarchar(512) null,date TIMESTAMP null,favorite binary(1) default 0)')
        cursor.execute('create table if not exists '+DBManager.TABLE_FAVORITES+' (id integer primary key autoincrement, name nvarchar(50) null,url nvarchar(512) null,date TIMESTAMP null,history_id integer not null,UNIQUE(history_id),FOREIGN KEY (history_id) REFERENCES history_query(id))')
        cursor.execute('create table if not exists ' + DBManager.TABLE_CONFIGURATION + ' (id integer primary key autoincrement,config_key nvarchar(100) not null unique ,config_value nvarchar(512) null )')
        cursor.close()
        conn.close()

