#coding=utf8
__author__ = 'guozhiwei'
import tcp_pack_helper
import const_define
import json_helper

class TcpDataParser:

    def __init__(self):
        self.buffer = ''


    def parse(self, data):
        self.buffer += data
        while True:
            #如果缓冲区数据长度小于包头的长度
            if len(self.buffer) < const_define.TCP_HEADER.HEAD_LEN:
                return (-1,None)
            #继续解析包头
            head_data = tcp_pack_helper.depack_msg(self.buffer[:const_define.TCP_HEADER.HEAD_LEN])
            if head_data['magic_num'] != const_define.TCP_HEADER.MAGIC_NUM:
                #没有按照规定的格式传输数据 不是正常的客户端  断开该连接
                self.transport.loseConnection()
                return

            cmd = head_data['cmd']
            #然后解析包体
            body_data = json_helper.loads(self.buffer[const_define.TCP_HEADER.HEAD_LEN:const_define.TCP_HEADER.HEAD_LEN+head_data['body_len']])
            #数据已经接收完毕 清空缓冲区
            self.buffer = ''
            return {
                'header':head_data,
                'body' : body_data,
            }
