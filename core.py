# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/03 21:57:56
Last edit at 2011/12/26
'''
import sys
import socket
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
from modules.nodes_manager import NodeDb

class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    '''
    build a xmlrpcserver supporting mutithread
    '''
    pass

class Node(object):
    def __init__(self, port, nodes_file, UUID):
        self.port = port
        self.nodes = NodeDb(nodes_file)
        self.UUID = UUID
        self.ip = utils.get_ip()

    def _greeting(self):
        self.templist = self.nodes.get_list()
        for node in self.templist:
            self._greet(node)

    def _greet2(self,node):
        nodeinfo = self.nodes.get_list()[node]
        if nodeinfo:
            s = ServerProxy(('http://'+nodeinfo[0]+':'+nodeinfo[1]))
            try:
                templist = pickle.loads(s.hello((self.UUID,self.ip,str(self.port))))
                for item in templist:
                    if not item == self.UUID:
                        print 3333
                        self.nodes.add_node({item:templist[item]})
                        print 4444444
            except:
                print 'remove %s' % node
                if not node == 'super_node':
                    self.nodes.rm_node(node)

    def _greet(self,node):
        nodeinfo = self.nodes.get_list()[node]
        if nodeinfo:
            s = ServerProxy(('http://'+nodeinfo[0]+':'+nodeinfo[1]))
            templist = {}
            try:
                templist = pickle.loads(s.hello((self.UUID,self.ip,str(self.port))))
            except:
                print 'remove %s' % node
                if not node == 'super_node':
                    self.nodes.rm_node(node)
            if templist:
                for item in templist:
                    if item != self.UUID and item not in self.templist:
                        print 'add:',{item:templist[item]}
                        self.nodes.add_node({item:templist[item]})
                        print 4444444


    def keepFind(self):
        '''
        maintain a node list
        '''
        time.sleep(2)
        while 1:
            #break
            print 'nodes:',self.nodes.get_list()
            self._greeting()
            self._broadcast()
            time.sleep(5)

    def _broadcast_listener(self):
        host = ''
        port = config.UDP_PORT
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind((host, port))

        while 1:
            try:
                message, address = s.recvfrom(8192)
                print "Got data from", address, message
            except:
                raise


    def _broadcast(self):
        dest = ('<broadcast>',config.UDP_PORT)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto('sun_p2p %s %s %s' % (self.UUID, self.ip, self.port), dest)



    def hello(self,info):
        '''
        introduce yourself to other node,
        and check if he is online
        '''
        if info:
            if info[0] != self.UUID:
                self.nodes.add_node(info)
        return pickle.dumps(self.nodes.get_list())

    def _start(self):
        t = Thread(target=self._broadcast_listener)
        #t.setDaemon(1)
        t1 = Thread(target=self.keepFind)
        #t1.setDaemon(1)
        t.start()
        t1.start()
        s = ThreadXMLRPCServer(('',self.port))#,logRequests=False
        s.register_instance(self)
        s.serve_forever()


def main():
    n = Node(1234, 'nodes.db', config.UUID)
    n._start()


if __name__ == "__main__":
    main()