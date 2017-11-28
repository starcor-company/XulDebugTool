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

    def run(self):
        from subprocess import Popen, PIPE
        p = Popen(self.cmd, stdout=PIPE, bufsize=1)
        l = []
        for line in iter(p.stdout.readline, b''):
            l.append(line.decode('utf-8'))
        # p.stdout.close()
        # p.wait()
        if self.isInterruptionRequested():
            return
        self.finishSignal.emit(l)
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
