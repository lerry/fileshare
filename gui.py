#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011-12-29 10:29
Last edit at 2011-12-29 10:49
'''
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from ui_main import Ui_form


class Demo(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_form()
        self.ui.setupUi(self)

        self.ui.list.setSortingEnabled(1)
        self.update_list()

    def update_list(self):
        item = ['OaK','Banana','Apple',' Orange','Grapes','Jayesh']
        listItem = []
        for lst in item:
            listItem.append(QtGui.QListWidgetItem(lst))
        for i in range(len(listItem)):
            self.ui.list.insertItem(i+1,listItem[i])

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())





