#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from XulDebugTool.ui.widget.model.database.ConfigurationDB import ConfigurationDB


class ConfigHelper(object):
    LOGCATPATH = ""

    #以下是配置信息所对应的key
    KEY_LOGCATPATH = 'logcatPath'

    @staticmethod
    def initLogConfigPath():
        ConfigHelper.LOGCATPATH = ConfigurationDB.getConfiguration(ConfigHelper.KEY_LOGCATPATH)
        if len(ConfigHelper.LOGCATPATH)<=0:
            ConfigHelper.LOGCATPATH = str(os.getcwd()) + "\logcat.txt"
            ConfigurationDB.saveConfiguration(ConfigHelper.KEY_LOGCATPATH,ConfigHelper.LOGCATPATH)










