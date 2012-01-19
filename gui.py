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
from ui_main import Ui_main
from core import Node
from config import config

def main(q):
    n = Node(1234, 'nodes.db', config.get('uuid'), q)
    n._start()

class Demo(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_main()
        self.ui.setupUi(self)
        #self.q = Queue(1)
        #core = Thread(target=main, args=(self.q,))
        #t = Thread(target=self.get_queue)
        #core.setDaemon(1)
        #t.setDaemon(1)
        #core.start()
        #t.start()

        #self.old_list = ''

        self.ui.tab.setWindowTitle('hhh')
        self.ui.tabWidget.setTabText(0, 'Resource list'.center(30))
        self.ui.tabWidget.setTabText(1, 'Download Queue'.center(30))
        #print self.ui.splitter.sizes()
        self.ui.splitter.setSizes([30,200])

        self.ui.tree.setColumnCount(1)
        self.ui.tree.setHeaderLabels(['Nodes'.center(30),]) 
        
        title_list = ['Name','size','type','time']

        #self.ui.table.setRowCount(10)
        self.ui.table.setColumnCount(4)
        self.ui.table.setHorizontalHeaderLabels(title_list)
        #for i in title_list:
         #   self.ui.list.insertItem(title_list.index(i), QtGui.QListWidgetItem(i))
           

        '''
             self.table.setRowCount(10)
    self.table.setColumnCount(6)
     self.table.setHorizontalHeaderLabels(['SUN','MON','TUE','WED',
                                              'THU','FIR','SAT'])

        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Key','Value'])
        root= QTreeWidgetItem(self.tree)
        root.setText(0,'root')
        child1 = QTreeWidgetItem(root)
        child1.setText(0,'child1')
        child1.setText(1,'name1')
        child2 = QTreeWidgetItem(root)
        child2.setText(0,'child2')
        child2.setText(1,'name2')
        child3 = QTreeWidgetItem(root)
        child3.setText(0,'child3')
        child4 = QTreeWidgetItem(child3)
        child4.setText(0,'child4')
        child4.setText(1,'name4')
        self.tree.addTopLevelItem(root)
        self.setCentralWidget(self.tree)             
        '''


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