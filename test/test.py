# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/03 22:10:20
Last edit at 2011/07/03
'''
import os
import hashlib
#it=os.listdir(os.getcwd())

#for i in it:
#    print hashlib.md5(open(i,'rb').read()).hexdigest()
b = 'abs'
class Person:
    def __init__(self,name):
        self.name = name

    def say_hi(self):
        print 'hi',self.name,b
    
a = Person(b)
#a.say_hi()
def Fib():
    a, b = 0, 1
    while 1:
        yield b
        a, b = b, a+b
 
fibs = Fib() 
print [fibs.next() for i in xrange(1000)]