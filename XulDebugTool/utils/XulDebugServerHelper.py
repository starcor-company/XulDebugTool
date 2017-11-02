#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib3


class XulDebugServerHelper(object):
    HOST = ''
    __LIST_PAGE = 'list-pages'
    __GET_LAYOUT = 'get-layout'
    __LIST_USER_OBJECTS = 'list-user-objects'
    __GET_USER_OBJECT = 'get-user-object'

    @staticmethod
    def listPages():
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + XulDebugServerHelper.__LIST_PAGE
                http = urllib3.PoolManager()
                r = http.request('GET', url)
            except Exception as e:
                print(e)
                return
            return r

    @staticmethod
    def getLayout(pageId, skipProp=True, withBindingData=True, withPosition=True):
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + XulDebugServerHelper.__GET_LAYOUT + '/' + pageId
                http = urllib3.PoolManager()
                r = http.request('GET', url,
                                 fields={'skip-prop': skipProp,
                                         'with-binding-data': withBindingData,
                                         'with-position': withPosition})
            except Exception as e:
                print(e)
                return
            return r

    @staticmethod
    def isXulDebugServerAlive():
        r = XulDebugServerHelper.listPages()
        if r:
            return r.status == 200
        else:
            return False

    @staticmethod
    def listUserObject():
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + XulDebugServerHelper.__LIST_USER_OBJECTS
                http = urllib3.PoolManager()
                r = http.request('GET', url)
            except Exception as e:
                print(e)
                return
            return r

    @staticmethod
    def getUserObject(objectId):
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + XulDebugServerHelper.__GET_USER_OBJECT + '/' + objectId
                http = urllib3.PoolManager()
                r = http.request('GET', url)
            except Exception as e:
                print(e)
                return
            return r
