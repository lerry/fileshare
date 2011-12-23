#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011-12-22 23:52
Last edit at 2011-12-23 23:41
'''
import os
import sqlite3


class NodeDb(object):
    '''
    manage nodelist
    '''
    def __init__(self, dbfile):
        if os.path.isfile(dbfile):
            try:
                self.conn = sqlite3.connect(dbfile)
                self.cur = self.conn.cursor()
            except:
                raise Exception("can't connect to %s" % dbfile)
        else:
            self.conn = sqlite3.connect(dbfile)
            self.cur = self.conn.cursor()
            self._initdb()

    def _initdb(self):
        self.cur.execute('CREATE TABLE nodelist(uuid TEXT, ip TEXT, port INTEGER)')
        self.cur.execute('INSERT INTO nodelist VALUES(?,?,?)', ('super_node','192.168.1.8',1234))
        self.conn.commit()

    def has_node(self,uuid):
        '''
        check if a node in the list with the given uuid
        '''
        self.cur.execute("SELECT * FROM nodelist WHERE uuid = '%s'" % uuid)
        result = self.cur.fetchall()
        if result:
            return True
        else:
            return False

    def get_list(self):
        '''
        return nodelist as a dictionary
        {'uuid':('192.168.1.8':1234)}
        '''
        self.cur.execute('SELECT * FROM nodelist')
        result = self.cur.fetchall()
        nodelist = {}
        for item in result:
            nodelist[item[0]] = item[1:]
        return nodelist

    def add_node(self,node_info):
        '''
        need a tuple of 3 item
        ('uuid','192.168.1.8',1234)
        '''
        if self.has_node(node_info[0]):
            self.update_node(node_info)
        else:
            self.cur.execute('INSERT INTO nodelist VALUES(?,?,?)', node_info)
            self.conn.commit()

    def update_node(self,node_info):
        value = (node_info[1],node_info[2],node_info[0])
        self.cur.execute("UPDATE nodelist SET ip = '%s', port = '%s' WHERE uuid = '%s'" % value)
        self.conn.commit()

    def rm_node(self,uuid):
        '''
        remove a node from list
        '''
        self.cur.execute("DELETE FROM nodelist WHERE uuid = '%s'" % uuid)
        self.conn.commit()

def _test():
    s = NodeDb('test.db')

    #s.rm_node('uuid')
    s.add_node(('uuid','192.168.1.8',1234))
    print s.has_node('super_node')
    s.update_node(('super_node','192.168.1.1',8488))
    print s.get_list()



if __name__ == "__main__":
    import nodes_manager, doctest
    doctest.testmod(nodes_manager)
    #_test()
