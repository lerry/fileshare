#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011-12-21 21:49
Last edit at 2011-12-21 21:49
'''
from modules.config_manager import ConfigManager

config_file = 'config.ini'
config = ConfigManager(config_file)
UUID = config.get_uuid()