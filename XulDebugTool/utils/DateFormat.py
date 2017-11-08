#!/usr/bin/python
# coding: utf-8
"""
author: CAI
last edited: 2017.10.29
"""

import time

class LogFormatTool(object):

    @classmethod
    def buildStardardTime(self):
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%03d" % (data_head, data_secs)
        return time_stamp


