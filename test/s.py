# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/02 06:52:17
Last edit at 2011/07/02
'''
import socket
s = socket.socket()
host = socket.gethostname()
port = 1234
s.bind((host,port))
a=[1,2,3,6,4]
s.listen(5)
while 1:
    c, addr = s.accept()
    print 'connection from', addr
    c.send('hello')
    c.close()