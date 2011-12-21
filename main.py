#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011-12-21 17:49
Last edit at 2011-12-21 17:49
'''
from core import Node
import utils

nodelist = {'83e92cb95e36444eb8a2daa87a7abbdf':('192.168.1.8','1234')}


def main():
    n = Node(1234, loadNodelist())
    n._start()


if __name__ == "__main__":
    main()
