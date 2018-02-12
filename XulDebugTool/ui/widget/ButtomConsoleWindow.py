#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QTabWidget, QTabBar, QApplication

from XulDebugTool.ui.widget.ConsoleView import ConsoleWindow
from XulDebugTool.utils.IconTool import IconTool
from XulDebugTool.utils.Utils import Utils


class ButtomWindow(QTabWidget):
    def __init__(self, parent=None):
        super(ButtomWindow, self).__init__(parent)
        self.initUi()


    def initUi(self):
        self.tabBar = QTabBar()
        self.consoleView = ConsoleWindow()
        self.tabBar.tabBarClicked.connect(self.status)
        self.tabBar.setExpanding(False)
        self.setTabBar(self.tabBar)
        self.addTab(self.consoleView,IconTool.buildQIcon('logcat.png'), "Logcat")
        self.consoleView.setVisible(False)
        self.setFixedHeight(Utils.getItemHeight())
        self.setTabPosition(QTabWidget.South)
        self.setStyleSheet("QTabBar::tab {border: none; height: "+str(Utils.getItemHeight())+"px; width:100px;color:black;}"
                            "QTabBar::tab:selected { border: none;background: lightgray; } ")

    def status(self):
      if self.tabBar.tabText(self.tabBar.currentIndex()) == 'Logcat':
        if self.consoleView.isVisible():
          self.consoleView.setVisible(False)
          self.preHeight = self.width()
          self.setFixedHeight(Utils.getItemHeight())
        else:
          self.consoleView.setVisible(True)
          self.setMaximumHeight(Utils.getWindowHeight())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = ButtomWindow()
    mainWin.show()
    sys.exit(app.exec_())