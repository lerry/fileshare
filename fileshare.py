# -*- coding: utf-8 -*-
'''
For:
by Lerry  http://lerry.org
Start from 2011/07/03 21:57:56
Last edit at 2011/07/03
'''
import uuid
from SimpleXMLRPCServer import SimpleXMLRPCServer
from xmlrpclib import ServerProxy
TTL = 6

UUID = uuid.uuid1().get_hex()

nodelist = [('127.0.0.1','724',UUID)]
filedir = 'm:\\'

def get_file_list(filedir):
    '''
    �����ļ���Ϣ�б�, ���� �ļ�������С��sha1ֵ
    '''
    filelist = []
    return filelist


class Node:
    '''
    p2p�еĽڵ�
    '''
    def __init__(self,UUID,nodelist):
        self.UUID = UUID
        self.nodelist = nodelist
    
    def _GetNodelist(self.)
    
    def PutNodelist(self,thenode)
        '''
        �����Լ��Ľڵ��б�������ڵ�
        '''
        if not thenode in self.nodelist:
            
        return self.nodelist()
    def     

main():
    pass
    
    
if __name__ == __main__:
    main()