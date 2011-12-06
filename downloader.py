# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/25 16:23:57
Last edit at 2011/07/25
'''
# a = file('1.txt','wb')
# a.truncate(1024**2)
# a.close()
import urllib2 as l
a = l.Request('http://127.0.0.1/123.txt')
a.add_header('Range','bytes=1-5')
f = l.urlopen(a)
print f.read()