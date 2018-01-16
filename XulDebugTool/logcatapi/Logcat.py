# coding: utf-8
"""
author: CAI
last edited: 2017.10.29
"""
import logging

from XulDebugTool.controller.ConsoleDeskController import ConsoleController
from XulDebugTool.utils.FileHelper import FileHelper


class STCLogger():
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    def __init__(self):

        self.loggername = "STCLogger"
        #当前日志模式
        self.setLogLevel(self.INFO)

        #logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(self.loggername)

        self.logger.setLevel(logging.DEBUG)

        # create a file handler
        self.handler = logging.FileHandler(FileHelper.LOGPATH, "a", encoding="UTF-8")
        self.handler.setLevel(logging.DEBUG)

        # create a logging format
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)

        # add the handlers to the logger
        self.logger.addHandler(self.handler)

    def removeHandler(self):
        self.logger.removeHandler(self.handler)
        return

    def e(self, *args):
        self.logger.error(args)
        self.filterLog(self.ERROR,args)
        self.removeHandler()
        return


    def w(self, *args):
        self.logger.warning(args)
        self.filterLog(self.WARNING, args)
        self.removeHandler()
        return

    def i(self, *args):
        self.logger.info(args)
        self.filterLog(self.INFO, args)
        self.removeHandler()
        return

    def d(self, *args):
        self.logger.debug(args)
        self.filterLog(self.DEBUG, args)
        self.removeHandler()
        return

    def c(self, *args):
        self.logger.critical(args)
        self.filterLog(self.CRITICAL, args)
        self.removeHandler()
        return



    def filterLog(self,mode, args):
        preLevel = self.getCurLogLevel(mode)
        if preLevel >= self.level:
            ConsoleController.windowPrintInfo(self.loggername, mode, args)
        else:
            return

    def setLogLevel(self,level):
        if level is self.DEBUG:
            self.level = 0
        elif level is self.INFO:
            self.level = 1
        elif level is self.WARNING:
            self.level = 2
        elif level is self.ERROR:
            self.level = 3
        elif level is self.CRITICAL:
            self.level = 4

    def getCurLogLevel(self,level):
        if level is self.DEBUG:
            return 0
        elif level is self.INFO:
            return 1
        elif level is self.WARNING:
            return 2
        elif level is self.ERROR:
            return 3
        elif level is self.CRITICAL:
            return 4

