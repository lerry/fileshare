#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For: some functions
by Lerry  http://lerry.org
Start from 2011-12-21 18:05
Last edit at 2011-12-21 18:05
'''
import os
import uuid
try:
    import cPickle as pickle
except:
    import pickle

LIMIT = 50


def get_ip():
    '''
    get local ip address
    '''
    s = socket.socket(AF_INET, SOCK_DGRAM)
    try:
        s.connect(('www.baidu.com',0))
        return s.getsockname()[0]
    except:
        return socket.gethostbyname(socket.gethostname())


def load_nodelist():
    nodelist = {}
    if not os.path.exists('nodelist.dat'):
        nodelist = {'super_node':('192.168.1.8','1234')}
        nodelist_file = open('nodelist.dat','wb')
        pickle.dump(nodelist,nodelist_file)
        nodelist_file.close()
    else:
        nodelist = pickle.load(open('nodelist.dat','rb'))
    return nodelist


def get_uuid():
    return uuid.uuid4().get_hex()