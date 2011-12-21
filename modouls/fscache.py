#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011-12-18 16:01
Last edit at 2011-12-18 16:01
'''
import os
import hashlib
import timeit



class FSCache(object):
    '''
    A persistence cache manager
    '''
    def __init__(self, dbpath):
        self.db = dbpath
        if not os.path.exists(self.db):
            os.mkdir(self.db)

    def save(self,value):
        '''
        save value and return a key
        '''
        key = hashlib.sha1(value).hexdigest()
        cachefile = os.path.join(self.db, key)
        try:
            f = open(cachefile,'wb')
            f.write(value)
            f.close()
            return key
        except:
            pass

    def keys(self):
        return os.listdir(self.db)

    def put(self,key, value):
        '''
        save key and value
        '''
        cachefile = os.path.join(self.db, key)
        try:
            f = open(cachefile,'wb')
            f.write(value)
            f.close()
        except:
            pass

    def get(self, key):
        '''
        get value with key
        '''
        cachefile = os.path.join(self.db, key)
        if os.path.exists(cachefile):
            try:
                return open(cachefile,'rb').read()
            except:
                return None
        else:
            return None

    def rm(self, key):
        '''
        delete value with given key
        '''
        cachefile = os.path.join(self.db, key)
        try:
            os.remove(cachefile)
        except:
            return "Failed,may you don't have right"

    def has(self, key):
        '''
        check if there is ^^^^
        '''
        if os.path.exists(os.path.join(self.db, key)):
            return True
        else:
            return False



def hash_stor():
    f = open('test','rb')
    t = []
    cache = FSCache('.cache')
    while 1:
        temp = f.read(1024**2)
        if not temp:
            break
        key = cache.save(temp)
        t.append(key)
    print t


if __name__ == '__main__':
    hash_stor()