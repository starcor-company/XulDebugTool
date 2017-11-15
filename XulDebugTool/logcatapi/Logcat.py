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

    def e(self, *args):
        self.logger.error(args)
        ConsoleController.windowPrintInfo(self.loggername, "ERROR", args)
        self.removeHandler()
        return


    def w(self, *args):
        self.logger.warning(args)
        ConsoleController.windowPrintInfo(self.loggername,"WARNING", args)
        self.removeHandler()
        return

    def i(self, *args):
        self.logger.info(args)
        ConsoleController.windowPrintInfo(self.loggername, "INFO", args)
        self.removeHandler()
        return

    def d(self, *args):
        self.logger.debug(args)
        ConsoleController.windowPrintInfo(self.loggername,"DEBUG", args)
        self.removeHandler()
        return

    def c(self, *args):
        self.logger.critical(args)
        ConsoleController.windowPrintInfo(self.loggername, "CRITICAL", args)
        self.removeHandler()
        return


