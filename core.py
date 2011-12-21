# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/03 21:57:56
Last edit at 2011/07/03
'''
import sys
import re
import uuid
import time
import socket
from socket import SOCK_DGRAM, AF_INET
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

def getIP():
    '''
    get local ip address
    '''
    s = socket.socket(AF_INET, SOCK_DGRAM)
    try:
        s.connect(('www.baidu.com',0))
        return s.getsockname()[0]
    except:
        return socket.gethostbyname(socket.gethostname())

def guessIP():
    if "win" in sys.platform:
        return socket.gethostbyname(socket.gethostname())
    else:
        process = "/sbin/ifconfig"
        pattern = re.compile(r"inet\ addr\:((\d+\.){3}\d+)", re.MULTILINE)
        try:
            proc = subprocess.Popen(process, stdout=subprocess.PIPE)
            proc.wait()
            data = proc.stdout.read()
            return pattern.findall(data)[0][0]
        except:
            return "127.0.0.1"

TTL = config.TTL
UUID = uuid.uuid1().get_hex()
ip = getIP()
port = config.PORT
LIMIT = 50
nodelist = {UUID:('192.168.1.8','1234')}

class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    '''
    build a xmlrpcserver supporting mutithread
    '''
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
        nodeinfo = nodelist[node]
        s = ServerProxy(('http://'+nodeinfo[0]+':'+nodeinfo[1]))
        try:
            templist = pickle.loads(s.hello([self.UUID,ip,str(self.port)]))
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