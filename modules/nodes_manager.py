#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011-12-22 23:52
Last edit at 2011-12-22 23:52
'''
import os
import db


class NodeDb(object):
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
        self.cur.execute('INSERT INTO nodelist VALUES(?,?,?)',('super_node','192.168.1.8',1234))
        self.conn.commit()

    def query(self,sql):
        self.cur.execute(sql)
        return self.cur.fetchall()



    def get_list(self):
        self.cur.execute('SELECT * FROM nodelist')
        result = self.cur.fetchall()
        nodelist = {}
        for item in result:
            nodelist[item[0]] = item[1:2]
        return nodelist

    def add_node(self,nodeinfo):
        self.cur



    def rm_node(self,uuid):
        self.cur.execute("DELETE FROM nodelist WHERE uuid = '%s'" % uuid)
        self.conn.commit()

def _test():
    s = NodeDb('test.db')
    print s.get_list()
    s.rm_node('super_node')

if __name__ == "__main__":
    import nodedb, doctest
    doctest.testmod(nodedb)
    _test()