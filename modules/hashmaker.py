#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For: make hash and store in a sqlite db
by Lerry  http://lerry.org
Start from 2012-01-07 11:35
Last edit at 2012-01-07 11:35
'''
import os
import sqlite3
import hashlib
import utils


class HashMaker(object):
    '''give a folder path, hash all files,
       and store there information(hashvalue path size) in sqlite db
    '''
    def __init__(self, folder, db_file):
        self.folder = folder
        self.db = db_file
        if not utils.is_sqlite(self.db):
            self._init()
        else:
            self.connect()

        self.update_db()

    def _init(self):
        self.connect()
        self.cur.execute("CREATE TABLE hash_table(hash TEXT,path TEXT,size INTEGER,UNIQUE(hash))")
        self.conn.commit()

    def connect(self):
        self.conn = sqlite3.connect(self.db)
        self.cur = self.conn.cursor()

    def has_file(self, name):
        '''give full path, check if has added to db'''
        try:
            size = os.path.getsize(name)
        except:
            size = 0 #if file not exists or have no right
        self.cur.execute("SELECT * FROM hash_table WHERE path='%s' AND size='%s'" % (name, size))
        result = self.cur.fetchall()
        if result:
            return True
        else:
            return False

    def add(self, name, many=False):
        '''add new file info to db'''
        hash_value = hashlib.sha1(open(name,'rb').read()).hexdigest()
        size = os.path.getsize(name)
        #print hash_value
        try:
            self.cur.execute('INSERT INTO hash_table VALUES (?,?,?)',(hash_value, name, size))
        except:
            pass
        if not many:
            self.conn.commit()

    def rm(self, name):
        '''remove info of files which are not already exists'''
        self.cur.execute('DELETE FROM hash_table WHERE path="%s"' % name)
        self.conn.commit()

    def update_db(self):
        '''scan the whole folder and update db'''
        #add new file
        file_list = utils.get_filelist(self.folder)
        for name in file_list:
            if not self.has_file(name):
                self.add(name,many=True)
        self.conn.commit()

        #remove file which not exists
        self.cur.execute('SELECT path FROM hash_table')
        result = self.cur.fetchall()
        for name in result:
            if not os.path.isfile(name[0]):
                self.rm(name)

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    test = HashMaker('/dev/shm/fileshare/','test.db')
    print test.has_file('/dev/shm/fileshare/core.py')
    test.close()
    os.remove('test.db')
