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
try:
    import cPickle as pickle
except:
    import pickle
import pickle
import config
from threading import Thread
from SimpleXMLRPCServer import SimpleXMLRPCServer
from xmlrpclib import ServerProxy
from SocketServer import ThreadingMixIn

TTL = config.TTL
UUID = uuid.uuid1().get_hex()
nodelist = {UUID:('127.0.0.1','1234')}
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
        temp = self.nodelist.copy()
        for node in temp:
            self._greet(node)

    def _greet(self,node):
        #get node's ip & port
        nodeinfo = nodelist[node]
        s = ServerProxy(('http://'+nodeinfo[0]+':'+nodeinfo[1]))
        #try:
        templist = pickle.loads(s.hello([self.UUID,ip,str(self.port)]))
        self.nodelist.update(templist)
        #except:
         #   del self.nodelist[node]


    def keepFind(self):
        '''
        maintain a node list
        '''
        while 1:
            #break
            self._greeting()
            time.sleep(1)

    def hello(self,info):
        '''
        introduce yourself to other node,
        and check if he is online
        '''
        if info:
            self.nodelist[info[0]] = tuple(info[1:])
            #print self.nodelist
        #random.shuffle(self.nodelist)
        return pickle.dumps(self.nodelist)

    def _start(self):
        s = ThreadXMLRPCServer(('',self.port))
        s.register_instance(self)
        s.serve_forever()

def main():
    n = Node(1234, nodelist)
    n._start()


if __name__ == "__main__":
    main()