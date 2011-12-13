# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/03 21:57:56
Last edit at 2011/07/03
'''
import uuid
import time
import socket
import random
import config
from threading import Thread
from SimpleXMLRPCServer import SimpleXMLRPCServer
from xmlrpclib import ServerProxy
from SocketServer import ThreadingMixIn

TTL = config.TTL
UUID = uuid.uuid1().get_hex()
nodelist = [UUID:('127.0.0.1','724')]
ip = socket.gethostbyname(socket.gethostname())
port = config.PORT
LIMIT = 50

class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class Node(object):
    def __init__(self, port, nodelist):
        self.port = port
        self.nodelist = nodelist
        self.UUID = UUID
        t = Thread(target=self.keepFind)
        t.setDaemon(1)
        t.start()

    def _greeting(self):
        for node in self.nodelist:
            self._greet(node)

    def _greet(self,node):
        #get node's ip & port
        nodeinfo = nodelist[node]
        s = ServerProxy(('http://'+node[0], node[1]))
        templist = s.hello((self.UUID:))
        for item  in templist:


    def keepFind(self):
        '''
        maintain a node list
        '''
        while 1:
            #break
            print 'I am runing'
            time.sleep(1)

    def hello(self,info):
        '''
        introduce yourself to other node,
        and check if he is online
        '''
        if info not in self.nodelist:
            self.nodelist.append(info)
        random.shuffle(self.nodelist)
        return self.nodelist[:LIMIT]

    def _start(self):
        s = ThreadXMLRPCServer(('',self.port))
        s.register_instance(self)
        s.serve_forever()

def main():
    n = Node(1234, nodelist)
    n._start()


if __name__ == "__main__":
    main()