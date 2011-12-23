#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011-12-21 17:49
Last edit at 2011-12-21 17:49
'''
from core import Node
from modules import utils


def main():
    n = Node(1234, utils.load_nodelist(), utils.get_uuid())
    n._start()


if __name__ == "__main__":
    main()
