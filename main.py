#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011-12-21 17:49
Last edit at 2011-12-21 17:49
'''
import sys
from PyQt4 import QtGui
from multiprocessing import Process
from gui import Demo


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
