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
from threading import Thread
from Queue import Queue
from ui_main import Ui_form


class Demo(QtGui.QMainWindow):
    def __init__(self, queue, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_form()
        self.q = queue
        self.ui.setupUi(self)

        self.ui.list.setSortingEnabled(1)
        #self.update_list()
        t = Thread(target=self.get_queue)
        t.setDaemon(1)
        t.start()

    def get_queue(self):
        while 1:
            if self.q.qsize() != 0:
                print 'queue:',self.q.get()
                #self.update_list(self.q.get())
        
    def update_list(self, list):
        listItem = []
        for lst in list:
            listItem.append(QtGui.QListWidgetItem(lst))
        for i in range(len(listItem)):
            self.ui.list.insertItem(i+1,listItem[i])

if __name__ == "__main__":
    q = Queue()
    app = QtGui.QApplication(sys.argv)
    demo = Demo(q)
    demo.show()
    sys.exit(app.exec_())





