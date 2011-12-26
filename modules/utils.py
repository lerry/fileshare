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