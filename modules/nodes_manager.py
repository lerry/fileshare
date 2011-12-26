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
        self.db_file = dbfile
        if os.path.isfile(dbfile):
            pass
            #self._initdb()
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
            cur.execute('INSERT INTO nodelist VALUES(?,?,?)', ('super_node','202.197.209.98 ','1234'))
            conn.commit()


    def _dict2tuple(self,info):
        '''
        convert {'u':('ip','p')} to ('u','ip','p')
        '''
        key = info.keys()[0]
        value = info[key]
        return (key,value[0],value[1])

    def has_node(self,uuid):
        '''
        check if a node in the list with the given uuid
        '''
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM nodelist WHERE uuid = '%s'" % uuid)
            result = cur.fetchall()
            if result:
                return True
            else:
                return False

    def get_list(self):
        '''
        return nodelist as a dictionary
        {'uuid':('192.168.1.8':'1234')}
        '''
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM nodelist')
            conn.commit()
            result = cur.fetchall()
            nodelist = {}
            for item in result:
                nodelist[item[0]] = item[1:]
            return nodelist

    def add_node(self,node_info):
        '''
        need a tuple of 3 item or dict
        ('uuid','192.168.1.8','1234')
        '''
        with self.connect() as conn:
            cur = conn.cursor()
            if type(node_info) == dict:
                node_info = self._dict2tuple(node_info)
            if self.has_node(node_info[0]):
                self.update_node(node_info)
            else:
                cur.execute('INSERT INTO nodelist VALUES(?,?,?)', node_info)
                conn.commit()

    def update_node(self,node_info):
        with self.connect() as conn:
            cur = conn.cursor()
            value = (node_info[1],node_info[2],node_info[0])
            cur.execute("UPDATE nodelist SET ip = '%s', port = '%s' WHERE uuid = '%s'" % value)
            conn.commit()

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
