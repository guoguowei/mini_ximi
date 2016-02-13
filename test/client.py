#coding=utf8
'''
    tcp 客户端
'''
__author__ = 'guozhiwei'

import env
env.init_env()

from twisted.internet import reactor
from twisted.internet.protocol import Protocol
import tcp_pack_helper
import json_helper
from twisted.internet import task
from twisted.internet.protocol import ReconnectingClientFactory


class MyProtocol(Protocol):

    def connectionMade(self):
        '''
            客户端连接成功之后会自动调用该方法
        :return:
        '''
        print 'is already connect to the server'
        msg = {
            'uid' : 911,
            'pwd' : 'dkjfkdjfkdjfkd',
        }
        cmd = 1000   #定义1000表示登陆
        pack_msg = tcp_pack_helper.pack_msg(cmd, json_helper.dumps(msg))
        self.transport.write(pack_msg)
        t = task.LoopingCall(self.heart_beat)
        t.start(10, now=True)



    def connectionLost(self, reason):
        print reason
        print 'connection is lost =>',self.transport.getPeer()
        print 'now reconnect'


    def heart_beat(self):
        msg = {
            'uid' : 911,
        }
        cmd = 1001
        pack_msg = tcp_pack_helper.pack_msg(cmd, json_helper.dumps(msg))
        self.transport.write(pack_msg)




class MyClientFactory(ReconnectingClientFactory):
    '''
        ReconnectingClientFactory  会自动进行断线重连
    '''
    protocol = MyProtocol
    maxDelay = 5




if __name__ == '__main__':

    reactor.connectTCP('127.0.0.1', 10231, MyClientFactory())
    reactor.run()
