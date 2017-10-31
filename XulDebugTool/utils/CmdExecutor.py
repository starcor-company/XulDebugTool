#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal


class CmdExecutor(QThread):

    finishSignal = pyqtSignal(list)

    def __init__(self, parent=None):
        super(CmdExecutor, self).__init__(parent)

    def exec(self, cmd):
        self.cmd = cmd
        self.start()

    def run(self):
        from subprocess import Popen, PIPE
        p = Popen(self.cmd, stdout=PIPE, bufsize=1)
        l = []
        for line in iter(p.stdout.readline, b''):
            l.append(line.decode('utf-8'))
        # p.stdout.close()
        # p.wait()
        self.finishSignal.emit(l)
