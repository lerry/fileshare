# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/03 21:57:56
Last edit at 2011/12/26
'''
import socket
import time
try:
    import cPickle as pickle
except:
    import pickle
from config import config
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
        for node in self.templist:
            self._greet(node)

    def _greet(self,node='', nodeinfo=''):
        if not nodeinfo:
            #nodeinfo = self.nodes.get_list()[node]
            nodeinfo = self.templist[node]
        if nodeinfo:
            #print 'ss',nodeinfo
            s = ServerProxy(('http://'+nodeinfo[0]+':'+nodeinfo[1]))
            templist = {}
            try:
                templist = pickle.loads(s.hello((self.UUID,self.ip,str(self.port))))
            except:
                if not node == 'super_node':
                    print 'remove %s' % node
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
            self.templist = self.nodes.get_list()
            print 'nodes:',self.templist
            self._greeting()
            self._broadcast()
            time.sleep(5)

    def _broadcast_listener(self):
        host = ''
        port = config.getint('udp_port')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind((host, port))

        while 1:
            try:
                message, address = s.recvfrom(8192)
                #print "Got data from", address, message
                if message.startswith(config.get('sign')):
                    info = message[len(config.get('sign')):].split()[1:]
                    self._greet(nodeinfo=info)
            except:
                raise


    def _broadcast(self):
        dest = ('<broadcast>',config.getint('udp_port'))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        try:
            s.sendto('sun_p2p %s %s %s' % (self.UUID, self.ip, self.port), dest)
        except:
            pass



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
        t.setDaemon(1)
        t1 = Thread(target=self.keepFind)
        t1.setDaemon(1)
        t.start()
        t1.start()
        s = ThreadXMLRPCServer(('',self.port))#,logRequests=False
        s.register_instance(self)
        s.serve_forever()


def main():
    n = Node(1234, 'nodes.db', config.get('uuid'))
    n._start()


if __name__ == "__main__":
    main()