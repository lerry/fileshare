# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/03 19:27:20
Last edit at 2011/07/03
'''
from xmlrpclib import ServerProxy
from os.path import join, isfile
from SimpleXMLRPCServer import SimpleXMLRPCServer
from urlparse import urlparse
import sys

MAX_HISTORY_LENGTH = 5

OK = 1
FAIL = 2
EMPTY = ''

def getPort(url):
    name = urlparse(url)[1]
    return int(url[url.find(':')+1:])

class Node(object):
    def __init__(self, url, dirname, secret):
        self.url = url
        self.dirname= dirname
        self.secret = secret
        self.known = set()

    def query(self, query, history=[]):
        code, data = self._handle(query)
        if code == OK:
            return code, data
        else:
            history+=[self.url]
            if len(history) >= MAX_HISTORY_LENGTH:
                return FAIL, EMPTY
            return self._broadcast(query,history)

    def hello(self,other):
        self.known.add(other)
        return OK

    def fetch(self, query, secret):
        if secret != self.secret:
            return FAIL
        code, data = self.query(query)
        if code == OK:
            f = open(join(self.dirname, query), 'w')
            f.write(data)
            f.close()
            return OK
        else:
            return FAIL

    def _start(self):
        s = SimpleXMLRPCServer('',getPort(self.url))
        s.register_instance(self)
        s.serve_forever()

    def _handle(self, query):
        name = join(self.dirname, query)
        if not isfile:
            return FAIL, EMPTY
        return OK, open(name).read()

    def _broadcast(self, query, history):
        for other in self.known.copy():
            if other in history: continue
            try:
                s = ServerProxy(other)
                code, data = s.query(query, history)
                if code == OK:
                    return code, data
            except:
                self.known.remove(other)
        return FAIL, EMPTY

def main():
    url, dirname, secret = sys.argv[1:]
    n = Node(url, dirname, secret)
    n._start()

if __name__ == '__main__':
    main()