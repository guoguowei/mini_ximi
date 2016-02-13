#coding=utf8
'''
    对与客户端传输的tcp数据进行解包和打包

        第一个 4字节 特殊字符0xF4F4F4F4
        第二个 4字节 包体长度
        第三个 4字节 包体数据类型
        第四个 4字节 CMD
        第五个 4字节 是否gzip
        第六个 4字节 客户端平台定义
        第七个 4字节 协议版本号
        剩余的 12字节 预留
        N字节  包体
'''
__author__ = 'guozhiwei'

import struct
import logging
import traceback

from const_define import TCP_HEADER

HEAD_LEV = TCP_HEADER.HEAD_LEN #包头的长度
MAGIC_NUM = TCP_HEADER.MAGIC_NUM
BODY_DATA_TYPE_JSON = TCP_HEADER.BODY_DATA_TYPE_JSON
NOT_GZIP = TCP_HEADER.NOT_GZIP
CLIENT_PLATFORM_IOS = TCP_HEADER.CLIENT_PLATFORM_IOS
INIT_PROTOCOL_VERSION = TCP_HEADER.INIT_PROTOCOL_VERSION


def pack_msg(cmd, msg):
    head = struct.pack('!10I',MAGIC_NUM,len(msg),BODY_DATA_TYPE_JSON,cmd,NOT_GZIP,\
                CLIENT_PLATFORM_IOS,INIT_PROTOCOL_VERSION,0,0,0)
    return head+msg



def depack_msg(packed_msg):
    #解析包头
    try:
        data = struct.unpack("!10I", packed_msg)
        return {
            'magic_num' : data[0],
            'body_len' : data[1],
            'body_data_type' : data[2],
            'cmd' : data[3],
            'is_gzip' : data[4],
            'client_platform' : data[5],
            'protocol_version' : data[6],
            'ext_int1' : data[7],
            'ext_int2' : data[8],
            'ext_int3' : data[9]
        }
    except:
        logging.error(traceback.format_exc())
        return {}
