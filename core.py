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
        temp = self.nodes.get_list()
        for node in temp:
            self._greet(node)

    def _greet(self,node):
        nodeinfo = self.nodes.get_list()[node]
        if nodeinfo:
            s = ServerProxy(('http://'+nodeinfo[0]+':'+nodeinfo[1]))
            try:
                print 11111111111
                templist = pickle.loads(s.hello((self.UUID,self.ip,str(self.port))))
                print 222222,templist
                for item in templist:
                    print 3333333
                    if not item == self.UUID:
                        self.nodes.add_node({item:templist[item]})
                        print 4444444
            except:
                print 'remove %s' % node
                self.nodes.rm_node(node)


    def keepFind(self):
        '''
        maintain a node list
        '''
        time.sleep(2)
        while 1:
            #break
            print 'nodes:',self.nodes.get_list()
            self._greeting()
            time.sleep(5)

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
        t = Thread(target=self.keepFind)
        t.setDaemon(1)
        t.start()
        s = ThreadXMLRPCServer(('',self.port))
        s.register_instance(self)
        s.serve_forever()


def main():
    n = Node(1234, 'nodes.db', utils.get_uuid())
    n._start()


if __name__ == "__main__":
    main()