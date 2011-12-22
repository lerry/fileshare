#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011-12-22 23:52
Last edit at 2011-12-22 23:52
'''
import os
import sqlite3

nodelist_db = 'nodelist.db'

def load_nodelist():
    nodelist = {}
    if not os.path.exists(nodelist_db):
        nodelist = {'super_node':('192.168.1.8','1234')}
        nodelist_db = sqlite3.connect('nodelist.db')
    else:
        pass
    return nodelist