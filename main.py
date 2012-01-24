#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011-12-29 10:29
Last edit at 2011-12-29 10:49
'''
import os
import sys
import time
from PyQt4 import QtCore
from PyQt4 import QtGui
from threading import Thread
from Queue import Queue
from ui_main import Ui_main
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
        self.tree = QtGui.QTreeWidget()
        self.table = QtGui.QTableWidget(5,4)
        self.tab = QtGui.QTabWidget(self)

        self.splitter = QtGui.QSplitter()
        self.splitter.addWidget(self.tree)
        self.splitter.addWidget(self.table)
        #self.splitter.addWidget(self.tab)

        self.splitter.setSizes([30, 120])
        self.tab.addTab(self.splitter, 'main')
        self.tab.addTab(QtGui.QTextEdit(), 'text')
        self.tab.setTabText(0, 'Resource list'.center(30))
        self.tab.setTabText(1, 'Download Queue'.center(30))

        self.setCentralWidget(self.tab)

        self.status.showMessage('Hi')

        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(['Nodes'.center(30),]) 
        root = QtGui.QTreeWidgetItem(self.tree)      
        root.setText(0,'Local')
        folders, files = self.get_file_list()
        for i in folders:
            child = QtGui.QTreeWidgetItem(root)
            child.setText(0,i)  

        title_list = ['Name','size','type','time']
        self.table.setColumnCount(4)
        self.table.setRowCount(len(files))
        self.table.setHorizontalHeaderLabels(title_list)
        for n, i in enumerate(files):
            item = QtGui.QTableWidgetItem(i)
            #print n
            self.table.setItem(n, 0, item)    
    
    def get_detail(self, file_path):
        f_size = os.path.getsize(file_path)
        f_type = 'file' 
        f_time = '' 
        return (f_size, f_type, f_time)      

    def get_file_list(self):
        folder_path = '/dev/shm/'    
        temp_list = os.listdir(folder_path)
        folder_list = []
        file_list = []
        for i in temp_list:
            full_path = os.path.join(folder_path, i)
            if os.path.isdir(full_path):
                folder_list.append(i)
            elif os.path.isfile(full_path):
               file_list.append(i)    
        return (folder_list, file_list)


        ''' grid = QtGui.QGridLayout()'''

class Demo(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_main()
        self.setupUi(self)
        #self.q = Queue(1)
        #core = Thread(target=main, args=(self.q,))
        #t = Thread(target=self.get_queue)
        #core.setDaemon(1)
        #t.setDaemon(1)
        #core.start()
        #t.start()
        self.init_ui()
        self.statusbar.showMessage('Ready')

    def init_ui(self):   
        self.tab.setWindowTitle('hhh')

        #print self.horizontalLayout.sizes()
        #self.horizontalLayout.setSizes([30,200])
        self.horizontalLayout.addStretch(1)

        
        '''
        enumerate(file_list)

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
        self.list.clear()
        for i in range(len(listItem)):
            self.list.insertItem(i+1,listItem[i])

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    demo = App()
    demo.show()
    sys.exit(app.exec_())