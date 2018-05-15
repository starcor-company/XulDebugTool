#!/usr/bin/python
# -*- coding: utf-8 -*-
from urllib.parse import quote

import urllib3

from XulDebugTool.logcatapi.Logcat import STCLogger


class XulDebugServerHelper(object):
    HOST = ''
    __LIST_PAGE = 'list-pages'
    __GET_LAYOUT = 'get-layout'
    __LIST_USER_OBJECTS = 'list-user-objects'
    __GET_USER_OBJECT = 'get-user-object'
    __SET_ATTR = 'set-attr'
    __SET_STYLE = 'set-style'
    __ADD_CLASS = 'add-class'
    __REMOVE_CLASS = 'remove-class'
    __CLEAR_ALL_CACHES = 'clear-all-caches'
    __REQUEST_FOCUS = 'request-focus'
    __GET_SELECTOR = 'get-selector'
    __FIRE_EVENT = 'fire-event'

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
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def getLayout(pageId, skipProp=True, withBindingData=True, withPosition=True, withSelector=True):
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + quote(XulDebugServerHelper.__GET_LAYOUT + '/' + pageId)
                http = urllib3.PoolManager()
                r = http.request('GET', url, fields={'skip-prop': skipProp,
                                         'with-binding-data': withBindingData,
                                         'with-position': withPosition,
                                         'with-selector': withSelector})
            except Exception as e:
                STCLogger().e(e)
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
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def getUserObject(objectId):
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + quote(XulDebugServerHelper.__GET_USER_OBJECT + '/' + objectId)
                http = urllib3.PoolManager()
                r = http.request('GET', url)
            except Exception as e:
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def updateUrl(type, id, key, value):
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + quote(type + '/' + id + '/' + key + '/' + value)
                http = urllib3.PoolManager()
                STCLogger().i("updateUrl = " + url)
                r = http.request('GET', url)
            except Exception as e:
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def clearAllCaches():
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + XulDebugServerHelper.__CLEAR_ALL_CACHES
                http = urllib3.PoolManager()
                STCLogger().i("clearAllCaches = " + url)
                r = http.request('GET', url)
            except Exception as e:
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def focusChooseItemUrl(id):
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + XulDebugServerHelper.__REQUEST_FOCUS + '/' + id
                http = urllib3.PoolManager()
                STCLogger().i("focusChooseItemUrl = " + url)
                r = http.request('GET', url)
            except Exception as e:
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def getAllSelector():
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + XulDebugServerHelper.__GET_SELECTOR
                http = urllib3.PoolManager()
                STCLogger().i("getAllSelector = " + url)
                r = http.request('GET', url)
            except Exception as e:
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def getPageSelector(pageId):
        return XulDebugServerHelper.getLayout(pageId, False, False, False, True)

    @staticmethod
    def updateClassUrl(type, id, className):
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + quote(type + '/' + id + '/' + className)
                http = urllib3.PoolManager()
                STCLogger().i("updateClassUrl = " + url)
                r = http.request('GET', url)
            except Exception as e:
                STCLogger().e(e)
                return
            return r

    @staticmethod
    def fireItemEvent(action, id):
        if XulDebugServerHelper.HOST == '':
            raise ValueError('Host is empty!')
        else:
            try:
                url = XulDebugServerHelper.HOST + quote(XulDebugServerHelper.__FIRE_EVENT + '/' + id + '/' + action)
                http = urllib3.PoolManager()
                STCLogger().i("fireItemEvent = " + url)
                r = http.request('GET', url)
            except Exception as e:
                STCLogger().e(e)
                return r