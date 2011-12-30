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
from config import config
from core import Node
from modules import utils
from threading import Thread
from gui import Demo
def main():
    n = Node(1234, 'nodes.db', config.get('uuid'))
    n._start()


if __name__ == "__main__":
    core = Thread(target=main)
    core.setDaemon(1)
    core.start()
    app = QtGui.QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
