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
    def windowPrintInfo(self, loggername, mode, msg):
        windowStr = LogFormatTool.buildStardardTime() + " - " + loggername + " - " + mode + " - " + msg
        print(windowStr)
        return

    def windowRequest(self, loggername, mode, msg, url):
        windowStr = LogFormatTool.buildStardardTime() + " - " + loggername + "- REQUEST URL: " + url + " - " + mode + " - " + msg
        print(windowStr)
        return

    def windowResponse(self, loggername, mode, msg, url):
        windowStr = LogFormatTool.buildStardardTime() + " - " + loggername + "- RESPONSE URL: " + url + " - " + mode + " - " + msg
        print(windowStr)
        return
