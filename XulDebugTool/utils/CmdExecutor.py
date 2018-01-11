#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal, QTimer


class CmdExecutor(QThread):

    finishSignal = pyqtSignal(list)
    _lastCallback = None

    def __init__(self, parent=None):
        super(CmdExecutor, self).__init__(parent)
        self.initConnectTimer()

    def exec(self, cmd):
        self.cmd = cmd
        self.__intConnectTime = 0
        self.connectTime.start(1000)
        self.start()

    def threadFinish(self):
        print(self.isFinished())
        if self.isRunning():
            self.wait()
        print(self.isFinished())
        self.finishSignal.emit(self.l)

    def run(self):
        self.finished.connect(self.threadFinish)
        from subprocess import Popen, PIPE
        p = Popen(self.cmd, stdout=PIPE, bufsize=-1)
        stdout_data, stderr_data = p.communicate(input=None, timeout=None)
        if stderr_data is not None:
            print("CmdExecutor stderr_data = " + stderr_data.decode('utf-8'))
        if stdout_data is not None:
            print("CmdExecutor stdout_data = "+stdout_data.decode('utf-8'))
        self.l = stdout_data.decode('utf-8').split('\n')
        # for line in iter(p.stdout.readline, b''):
        #     l.append(line.decode('utf-8'))
        #     # print("aaaaaaaaaaaaaa : "+line.decode('utf-8'))
        p.stdout.close()
        # p.wait()
        if self.isInterruptionRequested():
            return
        self.connectTime.stop()

    def initConnectTimer(self):
        self.connectTime = QTimer()
        self.connectTime.timeout.connect(self.onCmdExectuedTimeout)

    def onCmdExectuedTimeout(self):
        if self.__intConnectTime >= 20:
            self.requestInterruption()
            self.connectTime.stop()
            self.finishSignal.emit(['cmdExectuedTimeout'])
        else:
            self.__intConnectTime = self.__intConnectTime + 1


    def setFinishCallback(self, callback):
        if self._lastCallback is not None:
            self.finishSignal.disconnect(self._lastCallback)
        self.finishSignal.connect(callback)
        self._lastCallback = callback
