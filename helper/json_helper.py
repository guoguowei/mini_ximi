#coding=utf8
'''
    json 的简单封装
'''
import ujson
__author__ = 'guozhiwei'


def decode(data):
    return ujson.loads(data)


def encode(data):
    return ujson.dumps(data)

dumps = encode
loads = decode