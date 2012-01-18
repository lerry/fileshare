#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011-12-29 10:29
Last edit at 2011-12-29 10:49
'''
import sys
import time
from PyQt4 import QtCore
from PyQt4 import QtGui
from threading import Thread
from Queue import Queue
from ui_main import Ui_form
from core import Node
from config import config

def main(q):
    n = Node(1234, 'nodes.db', config.get('uuid'), q)
    n._start()

class Demo(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_form()
        self.ui.setupUi(self)
        self.q = Queue(1)
        core = Thread(target=main, args=(self.q,))
        t = Thread(target=self.get_queue)
        core.setDaemon(1)
        t.setDaemon(1)
        core.start()
        t.start()
        self.ui.list.setSortingEnabled(1)

        self.old_list = ''

    def get_queue(self):
        while 1:
            time.sleep(0.8)
            if not self.q.empty():
                #print 'Get task:',self.q.get()
                self.update_list(self.q.get())
                self.q.task_done()

    def update_list(self, list):
        if list == self.old_list:
            return
        else:
            self.old_list = list
        listItem = []
        for lst in list:
            listItem.append(QtGui.QListWidgetItem(lst+str(list[lst])))
        self.ui.list.clear()
        for i in range(len(listItem)):
            self.ui.list.insertItem(i+1,listItem[i])

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())