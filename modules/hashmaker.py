#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For: make hash and store in a sqlite db
by Lerry  http://lerry.org
Start from 2012-01-07 11:35
Last edit at 2012-01-07 11:35
'''
import os
#import time
import sqlite3
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

        #self.update()

    def _init(self):
        self.connect()
        self.cur.execute("CREATE TABLE hash_table(hash TEXT,path TEXT,size INTEGER,mtime TEXT,UNIQUE(hash,path))")
        self.conn.commit()

    def connect(self):
        self.conn = sqlite3.connect(self.db)
        self.cur = self.conn.cursor()

    def has_file(self, hash_value):
        '''check if there is a file with the given hash value'''
        self.cur.execute('''SELECT * FROM hash_table WHERE hash="%s"''' % hash_value)
        result = self.cur.fetchall()    
        if result:
            return True
        else:
            return False    

    def has_file_in_db(self, name):
        '''give full path, check if has added to db'''
        try:
            size = str(os.path.getsize(name))
            mtime = str(os.path.getmtime(name))
        except:
            size = '' #if file not exists or have no right
            mtime = ''
        #print name.encode('utf-8')
        self.cur.execute('''SELECT * FROM hash_table WHERE path="%s" AND size="%s" AND mtime="%s"''' % \
        (name, size, mtime))
        result = self.cur.fetchall()
        if result:
            #print result
            return True
        else:
            #print 0,size,mtime
            return False

    def add(self, name, many=False):
        '''add new file info to db'''
        hash_value = utils.get_hash(name)
        size = str(os.path.getsize(name))
        mtime = str(os.path.getmtime(name))
        #print hash_value
        try:
            self.cur.execute('INSERT INTO hash_table VALUES (?,?,?,?)',(hash_value, name, size, mtime))
            print 'Added: ',name.encode('utf-8')
            if not many:
                self.conn.commit()
        except:
            pass

    def rm(self, name, many=False):
        '''remove info of files which are not already exists'''
        self.cur.execute('''DELETE FROM hash_table WHERE path="%s"''' % name)
        if not many:
            self.conn.commit()

    def update(self):
        '''scan the whole folder and update db'''
        file_list = utils.get_filelist(self.folder)
        #remove file which not exists
        self.cur.execute('SELECT path, mtime FROM hash_table')
        result = self.cur.fetchall()
        for name in result:
            try:
                notchanged = str(name[1]) == str(os.path.getmtime(name[0]))
            except:
                notchanged = False    
            #print notchanged
            if os.path.isfile(name[0]) and name[0] in file_list and notchanged:
                pass
            else:    
                print 'Removed:',name[0].encode('utf-8')
                self.rm(name[0])
        self.conn.commit()

        #add new file
        for name in file_list:
            if not self.has_file_in_db(name):
                self.add(name)
                #time.sleep(1)
        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    test = HashMaker('/home/public/Pictures','/dev/shm/test.db')
    test.update()
    print test.has_file_in_db('/dev/shm/fileshare/core.py')
    print test.has_file('90b00f01eb3120e1d713beb2930698bc05bacc81')
    test.close()
    #os.remove('/dev/shm/test.db')
    #print os.listdir('/home/public/编程工具/')
