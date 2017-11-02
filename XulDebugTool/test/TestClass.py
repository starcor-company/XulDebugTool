from PyQt5 import QtCore, QtGui


class TestClass(QtCore.QObject):

    def __init__(self, parent = None):
        super(TestClass, self).__init__(parent)
        self.name = 'Czesc'
        self.number = 4
        #self.color = QtGui.QColor(4)
        self.radius = 0.00
        self._id = 5
        self.test = True
        #self.lst = [1,2,3,4,5]
        #self.dict = {'abc' : 1, 'def' : 2}