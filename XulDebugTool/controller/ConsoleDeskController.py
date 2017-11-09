#!/usr/bin/python
# coding: utf-8
"""
author: CAI
last edited: 2017.10.29
该类用于控制窗口日志输出
"""
from XulDebugTool.utils.DateFormat import LogFormatTool


class ConsoleController(object):

    @classmethod
    def windowPrintInfo(self, loggername, mode, msg=None):
        if msg is not None:
            windowStr = LogFormatTool.buildStandardTime() + " - " + loggername + " - " + mode + " - " + msg
        else:
            windowStr = LogFormatTool.buildStandardTime() + " - " + loggername + " - " + mode
        print(windowStr)
        return

