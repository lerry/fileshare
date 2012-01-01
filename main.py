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
from Queue import Queue
from threading import Thread
from multiprocessing import Process
from gui import Demo
def main():
    n = Node(1234, 'nodes.db', config.get('uuid'), q)
    n._start()


if __name__ == "__main__":
    q = Queue()
    #core = Process(target=main, args=(q,))
    core = Thread(target=main)
    core.setDaemon(1)
    core.start()
    app = QtGui.QApplication(sys.argv)
    demo = Demo(q)
    demo.show()
    sys.exit(app.exec_())
