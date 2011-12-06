# -*- coding: utf-8 -*-
'''
For: Basic HTTP Server with threading
by Lerry  http://lerry.org
Start from 2011/07/21 19:19:13
Last edit at 2011/07/21
'''
import os
from BaseHTTPServer import HTTPServer
from MyHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn


class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass

os.chdir('D:\\')   
    
def run_server(port):
 
    serveraddr = ('', port)

    serv = ThreadingServer(serveraddr, SimpleHTTPRequestHandler)

    serv.serve_forever()
    
if __name__=='__main__':
    run_server(80)