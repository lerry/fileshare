# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/02 06:52:27
Last edit at 2011/07/02
'''
import socket
s = socket.socket()
host = socket.gethostname()
port = 1234
s.connect((host,port))
print s.recv(1024)