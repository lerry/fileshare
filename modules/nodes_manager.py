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
from utils import get_super_nodes

class NodeDb(object):
    '''
    manage nodelist
    '''
    def __init__(self, dbfile):
        self.nodelist = {}
        self.changed = True
        self.db_file = dbfile
        if os.path.isfile(dbfile):
            pass
        else:
            self._initdb()

    def connect(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except:
            raise Exception("can't connect to %s" % dbfile)


    def _initdb(self):
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute('CREATE TABLE nodelist(uuid TEXT, ip TEXT, port TEXT)')
            nodes_list = get_super_nodes()
            for i in nodes_list:
                ip, port = i, nodes_list[i] 
            cur.execute('INSERT INTO nodelist VALUES(?,?,?)', ('super_node',str(ip),str(port)))
            conn.commit()
            self.changed = True


    def _dict2tuple(self,info):
        '''
        convert {'u':('ip','p')} to ('u','ip','p')
        '''
        key = info.keys()[0]
        value = info[key]
        return (key,value[0],value[1])

    def has_node(self, info):
        '''
        check if a node in the list with the given uuid
        '''
        if self.changed:
            self.get_list()
        if info[0] in self.nodelist and (info[1], info[2]) == self.nodelist[info[0]]:
            print '111'
            return True
        else:
            print '222'
            return False    

    def get_list(self):
        '''
        return nodelist as a dictionary
        {'uuid':('192.168.1.8':'1234')}
        '''
        print 'safsa',self.nodelist
        #if not changed, return self.nodelist else update first
        if not self.changed:
            print 'not changed'
            return self.nodelist
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM nodelist')
            conn.commit()
            result = cur.fetchall()
            for item in result:
                self.nodelist[item[0]] = item[1:]
            self.changed = False  
            print 'changed'  
            return self.nodelist

    def add_node(self,node_info):
        '''
        need a tuple of 3 item or dict
        ('uuid','192.168.1.8','1234')
        '''
        with self.connect() as conn:
            cur = conn.cursor()
            print node_info
            if type(node_info) == dict:
                node_info = self._dict2tuple(node_info)
            if self.has_node(node_info):
                return
            else:
                cur.execute('INSERT INTO nodelist VALUES(?,?,?)', node_info)
                conn.commit()
                self.changed = True    

    def update_node(self,node_info):
        with self.connect() as conn:
            cur = conn.cursor()
            value = (node_info[1],node_info[2],node_info[0])
            cur.execute("UPDATE nodelist SET ip = '%s', port = '%s' WHERE uuid = '%s'" % value)
            conn.commit()
            self.changed = True

    def rm_node(self,uuid):
        '''
        remove a node from list
        '''
        #if uuid == 'super_node':
            #return
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM nodelist WHERE uuid = '%s'" % uuid)
            conn.commit()
            self.changed = True

def _test():
    s = NodeDb('test.db')

    #s.rm_node('uuid')
    s.add_node(('uuid','192.168.1.8','1234'))
    print s.has_node('super_node')
    s.update_node(('super_node','192.168.1.1','8488'))
    print s.get_list()



if __name__ == "__main__":
    import nodes_manager, doctest
    doctest.testmod(nodes_manager)
    #_test()