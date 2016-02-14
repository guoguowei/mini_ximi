#coding=utf8
'''
    接收mq消息
'''
__author__ = 'guozhiwei'
import env
env.init_env()

import tx_mq

from twisted.internet import reactor

if __name__ == '__main__':

    mq = tx_mq.txRabbitmq.get_instance()
    mq.init_for_worker()
    reactor.run()
