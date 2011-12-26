# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/27 22:42:06
Last edit at 2011/12/26
'''
import os
import uuid
from ConfigParser import ConfigParser
import utils

class ConfigManager(object):
    def __init__(self, config_file):
        self.config_file = config_file
        if not os.path.exists(config_file):
            os.path.isfile(self.config_file)
            self._init_config()
        else:
            pass
        self.config = ConfigParser()
        self.config.read(config_file)

    def _init_config(self):
        config = ConfigParser()
        config.add_section('global')
        config.set('global','port',1234)
        config.set('global','uuid',utils.get_uuid())
        config.set('global','ttl',5)
        config.write(open(self.config_file,'w'))

    def get_uuid(self):
        return self.config.get('global','uuid')