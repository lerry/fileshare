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
        if utils.is_sqlite(self.db):
            pass
        else:
            self._init()
        #self.update()

    def connect(self):
        try:
            conn = sqlite3.connect(self.db)
            return conn
        except:
            raise Exception("can't connect to %s" % dbfile)

    def _init(self):
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE hash_table(hash TEXT,path TEXT,size INTEGER,mtime TEXT,UNIQUE(hash,path))")
            conn.commit()

    def has_value(self, hash_value):
        '''check if there is a file with the given hash value'''
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute('''SELECT * FROM hash_table WHERE hash="%s"''' % hash_value)
            result = cur.fetchall()    
            if result:
                return result[0][1].encode(utils.get_code())
            else:
                return False    

    def has_file_in_db(self, name):
        '''give full path, check if has added to db, if so, return file path'''
        try:
            size = str(os.path.getsize(name))
            mtime = str(os.path.getmtime(name))
        except:
            size = '' #if file not exists or have no right
            mtime = ''
        #print name.encode('utf-8')
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute('''SELECT * FROM hash_table WHERE path="%s" AND size="%s" AND mtime="%s"''' % \
                        (name, size, mtime))
            result = cur.fetchall()
            if result:
                #print result
                return True
            else:
                #print 0,size,mtime
                return False

    def add(self, name):
        '''add new file info to db'''
        hash_value = utils.get_hash(name)
        size = str(os.path.getsize(name))
        mtime = str(os.path.getmtime(name))
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO hash_table VALUES (?,?,?,?)',(hash_value, name, size, mtime))
            print 'Added: ',name.encode('utf-8')
            conn.commit()

    def rm(self, name):
        '''remove info of files which are not already exists'''
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute('''DELETE FROM hash_table WHERE path="%s"''' % name)
            conn.commit()

    def update(self):
        '''scan the whole folder and update db'''
        file_list = utils.get_filelist(self.folder)
        #remove file which not exists
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute('SELECT path, mtime FROM hash_table')
            result = cur.fetchall()
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
            conn.commit()

            #add new file
            for name in file_list:
                if not self.has_file_in_db(name):
                    self.add(name)
                    #time.sleep(1)
            conn.commit()

if __name__ == "__main__":
    test = HashMaker('/home/public/Pictures','/dev/shm/test.db')
    test.update()
    print test.has_file_in_db('/dev/shm/fileshare/core.py')
    import chardet 
    fpath =test.has_value('87cd9eb2e7cfd77ffed0cc3604b8552fead8d03f')
    #print chardet.detect(fpath)
    print fpath#.encode('utf-8')
    #os.remove('/dev/shm/test.db')
    #print os.listdir('/home/public/编程工具/')
