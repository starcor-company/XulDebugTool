import webbrowser

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel

from XulDebugTool.ui.BaseWindow import BaseWindow


class AboutWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        super().initWindow()
        self.setupUi()
        self.show()
        # self.setWindowOpacity(0.8)

    def setupUi(self):
        self.initWindowTitle()
        self.initAboutTitle()
        self.initProduction()
        self.initGitAddress()
        self.initCompanyAddress()
        self.initVersionNumber()

    def initVersionNumber(self):
        self.versionNumber = QtWidgets.QLabel(self)
        self.versionNumber.setGeometry(QtCore.QRect(50, 230, 300, 21))
        self.versionNumber.setObjectName("label_4")
        self.versionNumber.setText("版本号：1.0 beta1") #版本号应该写到版本配置文件里面去，从哪里读取

    def initCompanyAddress(self):
        self.company = QtWidgets.QPushButton(self)
        self.company.setGeometry(50, 195, 300, 23)
        self.company.setStyleSheet("QPushButton{background: transparent; color: blue}")
        self.company.setObjectName("pushButton")
        self.company.clicked.connect(self.openCompanyUrl)
        self.company.setText("https://www.starcor.com/ch/index.html")

    def initGitAddress(self):
        self.gitAddress = QtWidgets.QPushButton(self)
        self.gitAddress.setGeometry(QtCore.QRect(50, 160, 300, 50))
        self.gitAddress.setStyleSheet("QPushButton{background: transparent; color: blue; text-align: left}")
        self.gitAddress.setLayoutDirection(Qt.LayoutDirectionAuto)
        self.gitAddress.setObjectName("label_3")
        self.gitAddress.clicked.connect(self.openGitUrl)
        self.gitAddress.setText("https://github.com/starcor-company/XulDebugTool")

    def initProduction(self):
        self.production = QLabel(self)
        self.production.setGeometry(50, 125, 300, 23 * 2)
        self.production.setWordWrap(True)
        self.production.setText("Copyright (c) 2017, 北京视达科科技有限责任公司")

    def initAboutTitle(self):
        self.aboutTitle = QtWidgets.QLabel(self)
        self.aboutTitle.setGeometry(QtCore.QRect(0, 18, 400, 100))
        self.aboutTitle.setStyleSheet("QLabel{background: black; color: white;}")
        font = QFont()
        font.setPointSize(32)
        self.aboutTitle.setAlignment(Qt.AlignCenter)
        self.aboutTitle.setFont(font)
        self.aboutTitle.setObjectName("label_2")
        self.aboutTitle.setText("XulDebugTool")

    def initWindowTitle(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setFixedSize(400, 300)
        self.setStyleSheet("QMainWindow{border-color: black; background: white;}")
        self.setWindowTitle("关于")

    def openCompanyUrl(self):
        webbrowser.open("https://www.starcor.com/ch/index.html")

    def openGitUrl(self):
        webbrowser.open("https://github.com/starcor-company/XulDebugTool")
