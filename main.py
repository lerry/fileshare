#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011-12-29 10:29
Last edit at 2012-1-27 22:29
'''
import os
import sys
import time
from PyQt4 import QtCore
from PyQt4 import QtGui
from threading import Thread
from Queue import Queue
from core import Node
from config import config

#def main(q):
#    n = Node(1234, 'nodes.db', config.get('uuid'), q)
#    n._start()

class App(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        
        x, y, w, h = 500, 200, 660, 480
        self.setGeometry(x, y, w, h)
        print self.width()
        print self.height()
        self.setWindowTitle('main')

        self.status = self.statusBar()
        self.tree = QtGui.QTreeView()
        self.list = QtGui.QListView()
        self.tab = QtGui.QTabWidget(self)

        self.splitter = QtGui.QSplitter()
        self.splitter.addWidget(self.tree)
        self.splitter.addWidget(self.list)
        #self.splitter.addWidget(self.tab)

        self.splitter.setSizes([30, 120])
        self.tab.addTab(self.splitter, 'main')
        self.tab.addTab(QtGui.QTextEdit(), 'text')
        self.tab.setTabText(0, 'Resource list'.center(30))
        self.tab.setTabText(1, 'Download Queue'.center(30))

        self.setCentralWidget(self.tab)

        self.status.showMessage('Hi')

        sPath = QtCore.QString('/home/lerry/')

        self.dirmodel = QtGui.QFileSystemModel()
        
        self.dirmodel.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)
        self.tree.setModel(self.dirmodel)
        self.tree.setRootIndex(self.dirmodel.setRootPath(sPath)) 

        self.filemodel = QtGui.QFileSystemModel()
        self.filemodel.setFilter(QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)
        self.filemodel.setRootPath(sPath)
        #self.ui.listView.setRootIndex(self.filemodel.setRootPath(QtCore.QString('/home/lerry')))
        self.list.setModel(self.filemodel)
        self.list.setRootIndex(self.filemodel.setRootPath(sPath)) 

        QtCore.QObject.connect(self.tree, QtCore.SIGNAL("clicked(QModelIndex)"), self.update)

    #@pyqtSignature("QModelIndex") #declares signals to other components:
    def update(self, index):
        sPath = self.dirmodel.fileInfo(index).absoluteFilePath()
        #print sPath
        self.list.setRootIndex(self.filemodel.setRootPath(sPath))


    def get_queue(self):
        while 1:
            time.sleep(0.8)
            if not self.q.empty():
                #print 'Get task:',self.q.get()
                self.update_list(self.q.get())
                self.q.task_done()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    demo = App()
    demo.show()
    sys.exit(app.exec_())