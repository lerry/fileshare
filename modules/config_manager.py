# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/27 22:42:06
Last edit at 2011/07/27
'''
import os
from ConfigParser import ConfigParser

config_file = 'config.ini'

class ConfigManager(object):
    def __init__(self, config_file):
        self.config_file = config_file
        if not:
            os.path.isfile(self.config_file)
TTL = 5
PORT = 1234