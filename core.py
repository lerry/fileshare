# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/03 21:57:56
Last edit at 2011/07/03
'''
import time
try:
    import cPickle as pickle
except:
    import pickle
import config
from threading import Thread
from SimpleXMLRPCServer import SimpleXMLRPCServer
from xmlrpclib import ServerProxy
from SocketServer import ThreadingMixIn
from modules import utils


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    '''
    build a xmlrpcserver supporting mutithread
    '''
    pass

class Node(object):
    def __init__(self, port, nodelist, UUID):
        self.port = port
        self.nodelist = nodelist
        self.UUID = UUID
        self.ip = utils.get_ip()
        t = Thread(target=self.keepFind)
        t.setDaemon(1)
        t.start()

    def _greeting(self):
        temp = self.nodelist.copy()
        for node in temp:
            self._greet(node)

    def _greet(self,node):
        nodeinfo = self.nodelist[node]
        s = ServerProxy(('http://'+nodeinfo[0]+':'+nodeinfo[1]))
        try:
            templist = pickle.loads(s.hello([self.UUID,self.ip,str(self.port)]))
            self.nodelist.update(templist)
        except:
            del self.nodelist[node]


    def keepFind(self):
        '''
        maintain a node list
        '''
        while 1:
            #break
            self._greeting()
            print self.nodelist
            time.sleep(2)

    def hello(self,info):
        '''
        introduce yourself to other node,
        and check if he is online
        '''
        if info:
            self.nodelist[info[0]] = tuple(info[1:])
        return pickle.dumps(self.nodelist)

    def _start(self):
        s = ThreadXMLRPCServer(('',self.port))
        s.register_instance(self)
        s.serve_forever()

def main():
    n = Node(1234, utils.load_nodelist(), utils.get_uuid())
    n._start()


if __name__ == "__main__":
    main()