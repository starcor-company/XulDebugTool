# coding: utf-8
"""
author: CAI
last edited: 2017.10.29
"""
import logging
import time


class STCLogger():
    def __init__(self,loggername):

        #logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(loggername)

        self.logger.setLevel(logging.DEBUG)

        # create a file handler
        self.handler = logging.FileHandler(time.strftime('%Y%m%d%H%M', time.localtime(time.time())) + ".txt", "a", encoding="UTF-8")
        self.handler.setLevel(logging.DEBUG)

        # create a logging format
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)

        # add the handlers to the logger
        self.logger.addHandler(self.handler)

    def debug(self, msg):
        self.logger.debug(msg)
        self.logger.removeHandler(self.handler)
        return

    def warning(self, msg):
        self.logger.warning(msg)
        self.logger.removeHandler(self.handler)
        return

    def info(self, msg):
        self.logger.info(msg)
        self.logger.removeHandler(self.handler)
        return


