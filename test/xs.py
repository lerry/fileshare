# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/03 19:27:20
Last edit at 2011/07/03
'''
import os
from SimpleXMLRPCServer import SimpleXMLRPCServer
xs = SimpleXMLRPCServer(('',1724))
def test(x):
    return [1,2,3,x]
def getUptime():
    return os.popen('uptime').read()
xs.register_function(test)
xs.register_function(getUptime)
xs.serve_forever()