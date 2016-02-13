#coding=utf8
'''
    导入import目录的基本路径
'''
__author__ = 'guozhiwei'
import os
import sys

def init_env():
    '''
        导入sys path
    :return:
    '''
    file_basic_path = os.path.dirname(os.path.abspath(__file__))
    basic_path = file_basic_path[0:-4]
    os.environ["BASIC_PATH"] = basic_path  #basic path 放到全局的一个变量当中去
    sys.path.append( basic_path )
    sys.path.append( basic_path+'/config')
    sys.path.append( basic_path+'/helper')
    sys.path.append( basic_path+'/lib')
