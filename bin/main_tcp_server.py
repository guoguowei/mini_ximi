#coding=utf8
'''
    tcp server主程序

        1. 新连接和连接的断开
        2. 收包和发包
        3. 建立延迟检测是否登陆的任务
'''
__author__ = 'guozhiwei'

import sys
import env
env.init_env()
import config

from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet.protocol import ServerFactory
import tcp_data_parser
import tx_mq


class ClientProtocol(protocol.Protocol):

    def connectionMade(self):
        '''
            当客户端有新的连接的时候,会自动调用该方法
        :return:
        '''
        self.recv_data_buffer = ''   #数据接受缓冲区
        self.is_sign_in = 0  #初始上来的时候没有登陆
        print 'coming new connection =>',self.transport.getPeer()
        reactor.callLater(15, self.checkSignIn)   #30秒之后调用checkSignIn方法


    def setSignIn(self):
        self.is_sign_in = 1


    def connectionLost(self, reason):
        '''
            当客户端连接断开的时候,会自动调用该方法
        :param reason:
        :return:
        '''
        print reason
        print 'connection is lost =>',self.transport.getPeer()


    def dataReceived(self, data):
        #接收数据
        parser = tcp_data_parser.TcpDataParser()
        recv_data = parser.parse(data)
        header = recv_data['header']
        body = recv_data['body']
        print '====start===='
        print 'header=>' + str(header)
        print 'body=>' + str(body)
        print '====end======'
        #将数据传递给rabbitmq
        _data = {
            'header' : header,
            'body' : body,
            'extra' : {
                'from' : config.MAIN_TCP_SERVER_NAME
            }
        }
        tx_mq.txRabbitmq.get_instance().send_msg_to_worker(_data)


    def checkSignIn(self):
        if not self.is_sign_in:
            self.transport.loseConnection()



class Factory(ServerFactory):

    pass


if __name__ == '__main__':
    import other_helper
    config.MAIN_TCP_SERVER_NAME = other_helper.get_host_name() + '_' + sys.argv[1]
    tx_mq.txRabbitmq.get_instance().init_for_main_tcp()
    factory = Factory()
    factory.protocol = ClientProtocol
    reactor.listenTCP(10231, factory)
    reactor.run()
