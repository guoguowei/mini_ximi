#coding=utf8
__author__ = 'guozhiwei'

import os

hostname = 'localhost'

try:
    hostname = os.environ['HOSTNAME']
    hostname = hostname.lower()
    exec('from config.%s import *' % hostname.replace('-', '_'))
except:
    from development import *
