#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For: some functions
by Lerry  http://lerry.org
Start from 2011-12-21 18:05
Last edit at 2011-12-21 18:05
'''
import os
import hashlib
import uuid
import socket
import platform
from socket import SOCK_DGRAM, AF_INET
from os.path import join


def fpath2url(fpath, froot):
    #'/root/path/123.mp3' '/root' >>>'/path/123.mp3'
    #'C:\\Downlaod\\test\\123.mp3' 'C:\\Download'>>>'/test/123.mp3'
    code = get_code()
    #froot = froot.decode(code)
    if '/' in fpath:
        sep = '/'
    elif '\\' in fpath:
        sep = '\\'
    else:
        sep = os.sep    

    temp = fpath.strip(froot).split(sep)
    return ('/'+'/'.join(temp)).decode(get_code())

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

def get_code():
    p = platform.uname()[0]
    if p == 'Windows':
        return 'gbk'
    else:
        return 'utf-8'

def get_super_nodes():
    super_nodes = {'192.168.1.6':1234}
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
            file_list.append(os.path.abspath(join(root, name).decode(get_code())))
    return file_list

def get_hash(filePath):
    '''Do not put the whole file in memory'''
    fh = open(filePath, 'rb')
    m = hashlib.sha1()
    while True:
        data = fh.read(1024**2)
        if not data:
            break
        m.update(data)
    return m.hexdigest()

def get_free_port(port=52724):
    '''check if the given port is in use, return a new port''' 
    sockobj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        sockobj.bind(('0.0.0.0', port))
        return port
    except:
        return get_free_port(port+1)
            
def bytes2size(bytes):
    if bytes >= 1024**4:
        return '%.2f' % float(bytes/1024**4.)+'TB'
    if bytes >= 1024**3:
        return '%.2f' % float(bytes/1024**3.)+'GB'
    if bytes >= 1024**2:
        return '%.2f' % float(bytes/1024**2.)+'MB'
    if bytes >= 1024:
        return '%.2f' % float(bytes/1024.)+'KB'
    else:
        return str('%.2f' % bytes)+'B'                


if __name__ == '__main__':
    '''
    print get_ip()
    print get_uuid()
    print get_code()
    print get_filelist('/dev/shm')
    print is_sqlite('../nodes.db')
    print get_free_port(8080)
    #print fpath2url(u'C:\\Downlaod\\你妹\\123.mp3', 'C:\\Download\\')
    print fpath2url('/root/path/123.mp3', '/root') =='/path/123.mp3'
    print fpath2url('C:\\Downlaod\\test\\123.mp3', 'C:\\Download\\') == '/test/123.mp3'
    '''
    print bytes2size(106)
