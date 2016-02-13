#coding=utf8
__author__ = 'guozhiwei'


class TcpSession(object):

    def __init__(self, session_id, tcp_protocol):
        '''
        :param session_id:  连接建立的时候的会话id
        :param tcp_protocol:  twisted的tcp protocol对象
        :return:
        '''
        self.session_id = session_id
        self.tcp_protocol = tcp_protocol
