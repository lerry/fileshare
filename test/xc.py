# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/03 19:27:28
Last edit at 2011/07/03
'''
from xmlrpclib import *
s = ServerProxy('http://localhost:1235')
code, data=s.query('new')
#print code, data