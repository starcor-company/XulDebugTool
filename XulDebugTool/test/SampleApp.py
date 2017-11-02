from PyQt5 import QtGui
import sys

from PyQt5.QtWidgets import *

from XulDebugTool.test.TestClass import TestClass
from XulDebugTool.ui.widget.PropertyEditor import PropertyEditor


class SampleApp(QMainWindow):
    def __init__(self, parent = None):
        super(SampleApp, self).__init__(parent)
        self.setWindowTitle("Property Editor")

        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.nodeEdit = PropertyEditor()

        self.button = QPushButton("Print")

        self.test_class = TestClass(self)
        self.button.clicked.connect(self.get_dict)

        self.nodeEdit.addProperty(self.test_class)

        self.layout.addWidget(self.nodeEdit)
        self.layout.addWidget(self.button)

        self.setCentralWidget(self.widget)
        self.show()

    def get_dict(self):
        print(self.test_class.__dict__)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SampleApp()
    window.show()
    sys.exit(app.exec_())
