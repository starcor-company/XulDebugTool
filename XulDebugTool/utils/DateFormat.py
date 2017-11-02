#!/usr/bin/python
# coding: utf-8
"""
author: CAI
last edited: 2017.10.29
"""

from datetime import datetime



class LogFormatTool(object):

    @classmethod
    def buildStardardTime(self):
        windowStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return windowStr

