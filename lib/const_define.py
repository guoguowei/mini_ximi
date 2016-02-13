#coding=utf8
'''
    常量定义
'''
__author__ = 'guozhiwei'


class TCP_HEADER(object):

    HEAD_LEN = 40 #包头的长度
    MAGIC_NUM = 0xF4F4F4F4
    BODY_DATA_TYPE_JSON = 1  #包体为json
    NOT_GZIP = 0  #不用gzip压缩
    CLIENT_PLATFORM_IOS = 1  #客户端平台定义 IOS
    CLIENT_PLATFORM_ANDROID = 2  #客户端平台定义 IOS
    INIT_PROTOCOL_VERSION = 1000  #该协议的版本号



TCP_CMD_INFO = {
        1000 : 'sign_in'   #登陆
}
