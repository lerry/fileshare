# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/03 19:27:20
Last edit at 2011/07/03
'''
from SimpleXMLRPCServer import SimpleXMLRPCServer
xs = SimpleXMLRPCServer(('',724))
def test(x):
    return [1,2,3,x]
    
xs.register_function(test)
xs.serve_forever()    