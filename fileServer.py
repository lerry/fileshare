# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/27 22:49:51
Last edit at 2011/07/27
'''
import os
import posixpath
import urllib

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn

def get_handler(root_path):
    class _RerootedHTTPRequestHandler(SimpleHTTPRequestHandler):
        def translate_path(self, path):
            path = path.split('?',1)[0]
            path = path.split('#',1)[0]
            path = posixpath.normpath(urllib.unquote(path))
            words = path.split('/')
            words = filter(None, words)
            path = root_path#os.getcwd()
            for word in words:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir): continue
                path = os.path.join(path, word)
            self._test()    
            return path
        def _test(self):
            headers = str(self.headers).split()
            for index,data in enumerate(headers):
                #print data
                if data.strip().lower().startswith('range'):#.startswith('range:'):
                    print data, headers[index+1]
            #print str(headers)
    return _RerootedHTTPRequestHandler
        
class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass
    
    
def run_server(port=80, doc_root=os.getcwd()):
    serveraddr = ('', port)
    serv = ThreadingServer(serveraddr, get_handler(doc_root))
    serv.serve_forever()
    
if __name__=='__main__':
    run_server()
    