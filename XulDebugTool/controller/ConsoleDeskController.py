#!/usr/bin/python
# coding: utf-8
"""
author: CAI
last edited: 2017.10.29
该类用于控制窗口日志输出
"""
import re

from XulDebugTool.utils.DateFormat import LogFormatTool


class ConsoleController(object):

    @classmethod
    def windowPrintInfo(self, loggername, mode, msg):
        windowStr = LogFormatTool.buildStandardTime() + " - " + loggername + " - " + mode + " - "

        print(windowStr, end=' ')
        for text in msg:
            print(self.getLogContent(self, text), end=' ')
        print("<br />")
        return

    def getLogContent(self, text):
        if isinstance(text, str):
            regexUrl = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                                  re.IGNORECASE)
            urls = regexUrl.findall(text)
            for url in urls:
                preS = "<a href=\"" + url + "\">" + url + "</a>"
                text = text.replace(url, preS)

        return text

