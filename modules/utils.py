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
import socket
from socket import SOCK_DGRAM, AF_INET
from os.path import join

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


def get_super_nodes():
    super_nodes = ['202.197.209.98']
    return super_nodes


def get_uuid():
    if get_ip() not in get_super_nodes():
        return uuid.uuid4().get_hex()
    else:
        return 'super_node'

def is_sqlite(file_name):
    try:
        f = open(file_name,'rb')
        if f.read(6) == 'SQLite':
            return True
    except:
        return False

def get_filelist(folder):
    '''Give me a path, return all files with absolute path'''
    file_list = []
    for root,dirs,files in os.walk(folder):
        for name in files:
            file_list.append(os.path.abspath(join(root, name)))
    return file_list

if __name__ == '__main__':
    print get_ip()
    print get_uuid()
    print is_sqlite('test.db')
    print is_sqlite('../nodes.db')