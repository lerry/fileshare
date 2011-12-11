# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/03 21:57:56
Last edit at 2011/07/03
'''
import uuid
import cofig
from SimpleXMLRPCServer import SimpleXMLRPCServer

MAX_HISTORY_LENTH = 5
UUID = uuid.uuid1().get_hex()
nodelist = [('127.0.0.1','724',UUID)]

class Node(object):
    def __init__(self, port, nodelist):
        self.port = port
        self.nodelist = nodelist
    def hello(self):
        ${0}

def main():
    pass


if __name__ == "__main__":
    main()