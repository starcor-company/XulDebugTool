#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

import time

class FileHelper(object):
    LOGCONFIGPATH = ""
    LOGPATH = ""

    @classmethod
    def readLogSavePath(self):
        print(FileHelper.LOGCONFIGPATH)
        self.path = time.strftime('%Y%m%d%H', time.localtime(time.time())) + ".txt"
        # 读文件
        if not os.path.exists(FileHelper.LOGCONFIGPATH):
            return self.path
        else:
            try:
                f = open(FileHelper.LOGCONFIGPATH, 'r')

                if f:
                    text = f.read()
                    if text:
                        self.path = text
            except Exception as e:
                print(e)
            finally:
                f.close()
                return self.path

    @classmethod
    def writeLogSavePath(self,logPath):

        try:
            f = open(self.LOGCONFIGPATH, 'w')
            if f:
                f.write(logPath[0])
        except Exception as e:
            print(e)
        finally:
            if f:
                f.close()

    @classmethod
    def setLogPath(self):
        FileHelper.LOGPATH = FileHelper.readLogSavePath()

    @classmethod
    def initLogConfigPath(self):
        FileHelper.LOGCONFIGPATH = str(os.getcwd()) + "\LogConfig.txt"
        FileHelper.LOGPATH = FileHelper.readLogSavePath()







