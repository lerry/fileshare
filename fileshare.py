# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/03 21:57:56
Last edit at 2011/07/03
'''
import uuid
import time
import config
from threading import Thread
from SimpleXMLRPCServer import SimpleXMLRPCServer

TTL = config.TTL
UUID = uuid.uuid1().get_hex()
nodelist = [('127.0.0.1','724',UUID)]
port = config.PORT


class Node(object):
    def __init__(self, port, nodelist):
        self.port = port
        self.nodelist = nodelist
        t = Thread(target=self.keepFind)
        t.setDaemon(1)
        t.start()

    def keepFind(self):
        while 1:
            #break
            print 'I am runing'
            time.sleep(1)
    def hello(self):
        return 'hello'
    def _start(self):
        s = SimpleXMLRPCServer(('',self.port))
        s.register_instance(self)
        s.serve_forever()

def main():
    n = Node(1234, nodelist)
    n._start()


if __name__ == "__main__":
    main()