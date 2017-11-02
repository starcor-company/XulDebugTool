# coding: utf-8
"""
author: CAI
last edited: 2017.10.29
"""
import logging
import time

from XulDebugTool.controller.ConsoleDeskController import ConsoleController


class STCLogger():
    def __init__(self,loggername):

        self.loggername = loggername

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

    def error(self, msg):
        self.logger.error(msg)
        ConsoleController.windowPrintInfo(self.loggername, "ERROR", msg)
        self.removeHandler()
        return

    def debug(self, msg):
        self.logger.debug(msg)
        ConsoleController.windowPrintInfo(self.loggername, "DEBUG", msg)
        self.removeHandler()
        return

    def warning(self, msg):
        self.logger.warning(msg)
        ConsoleController.windowPrintInfo(self.loggername,"WARNING", msg)
        self.removeHandler()
        return

    def info(self, msg):
        self.logger.info(msg)
        ConsoleController.windowPrintInfo(self.loggername, "INFO", msg)
        self.removeHandler()
        return

    def critical(self,msg):
        self.logger.critical(msg)
        ConsoleController.windowPrintInfo(self.loggername, "CRITICAL", msg)
        self.removeHandler()
        return


