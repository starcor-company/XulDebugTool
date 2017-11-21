# coding: utf-8
"""
author: CAI
last edited: 2017.10.29
"""
import logging
import time

from XulDebugTool.controller.ConsoleDeskController import ConsoleController


class STCLogger():
    def __init__(self):

        self.loggername = "STCLogger"
        #当前日志模式
        self.setLogLevel("INFO")

        #logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(self.loggername)

        self.logger.setLevel(logging.DEBUG)

        # create a file handler
        self.handler = logging.FileHandler(time.strftime('%Y%m%d%H', time.localtime(time.time())) + ".txt", "a", encoding="UTF-8")
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
        self.filterLog("ERROR",args)
        self.removeHandler()
        return


    def w(self, *args):
        self.logger.warning(args)
        self.filterLog("WARNING", args)
        self.removeHandler()
        return

    def i(self, *args):
        self.logger.info(args)
        self.filterLog("INFO", args)
        self.removeHandler()
        return

    def d(self, *args):
        self.logger.debug(args)
        self.filterLog("DEBUG", args)
        self.removeHandler()
        return

    def c(self, *args):
        self.logger.critical(args)
        self.filterLog("CRITICAL", args)
        self.removeHandler()
        return



    def filterLog(self,mode, args):
        preLevel = self.getCurLogLevel(mode)
        if preLevel >= self.level:
            ConsoleController.windowPrintInfo(self.loggername, mode, args)
        else:
            return

    def setLogLevel(self,level):
        if level is "DEBUG":
            self.level = 0
        elif level is "INFO":
            self.level = 1
        elif level is "ERROR":
            self.level = 2
        elif level is "WARNING":
            self.level = 3
        elif level is "CRITICAL":
            self.level = 4

    def getCurLogLevel(self,level):
        if level is "DEBUG":
            return 0
        elif level is "INFO":
            return 1
        elif level is "ERROR":
            return 2
        elif level is "WARNING":
            return 3
        elif level is "CRITICAL":
            return 4

