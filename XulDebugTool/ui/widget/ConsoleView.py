import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import QMainWindow, QAction, \
    QSplitter, QApplication, QTextEdit, QWidget, QHBoxLayout, QComboBox, QPushButton, \
    QLineEdit, QSizePolicy, QVBoxLayout

from XulDebugTool.utils import IconTool
from XulDebugTool.utils.ConsoleStreamEmittor import ConsoleEmittor


class ConsoleWindow(QMainWindow):
    global textEdit

    def __init__(self, parent=None):
        super(ConsoleWindow, self).__init__(parent)

        sys.stdout = ConsoleEmittor(textWritten=self.normalOutputWritten)
        sys.stder = ConsoleEmittor(textWritten=self.normalOutputWritten)

        # 上
        self.searchButton = QLineEdit()
        self.searchButton.setPlaceholderText("搜索")
        self.searchButton.setMaximumWidth(300)
        self.searchButton.setMaximumHeight(32)
        self.searchButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.combo = QComboBox(self);
        self.combo.insertItem(0, 'Error');
        self.combo.insertItem(1, 'Debug');
        self.combo.insertItem(2, 'Verbose');
        self.combo.insertItem(3, 'Warning');
        self.combo.setCurrentIndex(0)

        layout_top = QHBoxLayout()
        layout_top.setAlignment(Qt.AlignRight)
        layout_top.setSpacing(20)
        layout_top.addWidget(self.combo)
        layout_top.addWidget(self.searchButton)

        self.functionTabWiget = QWidget()
        self.functionTabWiget.setLayout(layout_top)

        # 左
        self.clearButton = QPushButton(self)
        self.clearButton.setText("Clear")  # text
        self.clearButton.setIcon(QIcon("delete.png"))  # icon
        self.clearButton.clicked.connect(self.clear)
        self.clearButton.setToolTip("Clear the logcat")  # Tool tip
        self.clearButton.move(20, 20)

        self.settingButton = QPushButton(self)
        self.settingButton.setText("Setting")  # text
        self.settingButton.setIcon(QIcon("setting.png"))  # icon
        self.settingButton.clicked.connect(self.clear)
        self.settingButton.setToolTip("Clear the logcat")  # Tool tip
        self.settingButton.move(20, 20)

        layout_left = QVBoxLayout()
        layout_left.setAlignment(Qt.AlignLeft)
        layout_left.setSpacing(10)
        layout_left.addWidget(self.clearButton)
        layout_left.addWidget(self.settingButton)

        self.leftTabWiget = QWidget()
        self.leftTabWiget.setLayout(layout_left)
        self.leftTabWiget.setGeometry(10, 20, 20, 41)

        # 右
        self.textEdit = QTextEdit()
        self.textEdit.setText("This is a TextEdit!")


        self.messageSplitter = QSplitter(Qt.Horizontal)
        self.messageSplitter.addWidget(self.leftTabWiget)
        self.messageSplitter.addWidget(self.textEdit)
        self.messageSplitter.setHandleWidth(0)

        self.mainSplitter = QSplitter(Qt.Vertical)
        self.mainSplitter.addWidget(self.functionTabWiget)
        self.mainSplitter.addWidget(self.messageSplitter)
        self.mainSplitter.setHandleWidth(0)
        self.setCentralWidget(self.mainSplitter)

        self.mainSplitter.setStretchFactor(0, 0)
        self.mainSplitter.setStretchFactor(1, 0)

        self.messageSplitter.setStretchFactor(0, 0)
        self.messageSplitter.setStretchFactor(1, 2)
        self.show()



    def normalOutputWritten(self, text):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def initMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('Logcat')
        showLogAction = QAction('Show Log', self)
        fileMenu.addAction(showLogAction)

        helpMenu = menuBar.addMenu('Setting')
        aboutAction = QAction(IconTool.buildQIcon('setting.png'), 'About', self)
        helpMenu.addAction(aboutAction)

    def clear(self):
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ConsoleWindow()
    app.exec_()





