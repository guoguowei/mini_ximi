#coding=utf8
'''
    rabbitmq的客户端txamqp类库 二次封装
'''
import os
import env
env.init_env()

import config
from txamqp.protocol import AMQClient
from txamqp.client import TwistedDelegate
from txamqp.content import Content

import txamqp.spec
import logging
import traceback

from twisted.internet import error, protocol, reactor
from twisted.internet.defer import inlineCallbacks, Deferred, returnValue
import json_helper
import tcp_session_manager


class txRabbitmq:

    instance = None

    channel = None

    def __init__(self):
        self.channel = None
        self.client = None
        self.init_config()


    def init_config(self):
        if not config.RABBITMQ_CONNECT_INFO:
            logging.error('not found config RABBITMQ_CONNECT_INFO')
            os._exit(-1)
        self.host = config.RABBITMQ_CONNECT_INFO['host']
        self.port = config.RABBITMQ_CONNECT_INFO['port']
        self.vhost = config.RABBITMQ_CONNECT_INFO['vhost']
        self.username = config.RABBITMQ_CONNECT_INFO['username']
        self.password = config.RABBITMQ_CONNECT_INFO['password']
        self.spec = config.RABBITMQ_CONNECT_INFO['spec']


    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        cls.instance = txRabbitmq()
        return cls.instance


    @inlineCallbacks
    def connect(self):
        host = self.host
        port = self.port
        spec = self.spec
        user = self.username
        password = self.password
        vhost = self.vhost
        delegate = TwistedDelegate()
        onConn = Deferred()
        p = AMQClient(delegate, vhost, txamqp.spec.load(spec), heartbeat=0)
        f = protocol._InstanceFactory(reactor, p, onConn)
        c = reactor.connectTCP(host, port, f)

        def errb(thefailure):
            thefailure.trap(error.ConnectionRefusedError)
            logging.error(traceback.format_exc())
        onConn.addErrback(errb)
        client = yield onConn
        self.client = client
        yield self.authenticate(self.client, user, password)
        returnValue(client)


    @inlineCallbacks
    def authenticate(self, client, user, password):
        yield client.authenticate(user, password)


    @inlineCallbacks
    def open_channel(self, client):
        channel = yield client.channel(1)
        channel.channel_open()
        self.channel = channel
        yield channel
        txRabbitmq.channel = channel
        returnValue(channel)


    @inlineCallbacks
    def _init_worker(self, channel):
        yield channel.exchange_declare(exchange=config.EXCHANGE_NAME_WORKER, type="direct", durable=True)
        yield channel.queue_declare(queue=config.WORKER_QUEUE_NAME)
        yield channel.queue_bind(queue=config.WORKER_QUEUE_NAME, exchange=config.EXCHANGE_NAME_WORKER, routing_key=config.WORKER_QUEUE_NAME)


    @inlineCallbacks
    def init_for_main_tcp(self, *args, **keys):
        try:
            queue = config.MAIN_TCP_SERVER_QUEUE_NAME + '_' + str(config.MAIN_TCP_SERVER_NAME)
            client = yield self.connect()
            channel = yield self.open_channel(client)
            yield self._init_worker(channel)
            yield channel.queue_declare(queue=queue, *args, **keys)
            yield channel.exchange_declare(exchange=config.MAIN_TCP_SERVER_EXCHANGE_NAME, type="direct", durable=True)
            yield channel.exchange_declare(exchange=config.EXCHANGE_NAME_WORKER, type="direct", durable=True)
            yield channel.queue_bind(0, queue, config.MAIN_TCP_SERVER_EXCHANGE_NAME, queue)
            reply = yield channel.basic_consume(queue=queue, no_ack=True)
            queue = yield client.queue(reply.consumer_tag)
            logging.info('init for hub mq finish')
            while True:
                data = yield queue.get()
                msg = json_helper.loads(data.content.body)
                print msg
                #处理消息
                # SessionManager.handler_data_from_mq(msg)
        except:
            logging.error(traceback.format_exc())


    def get_channel(self):
        return txRabbitmq.channel


    def send_msg_to_worker(self, data):
        try:
            routing_keys_worker = config.WORKER_QUEUE_NAME

            channel = self.get_channel()
            msg = Content(json_helper.dumps(data))
            msg["delivery mode"] = 1
            exchange_name_worker = config.EXCHANGE_NAME_WORKER
            d = channel.basic_publish(
                exchange=exchange_name_worker, content=msg, routing_key=routing_keys_worker)
            print '=====send msg to worker===='
            print msg
            print '==========================='
            d.addErrback(self.errb)
        except:
            print traceback.format_exc()


    @inlineCallbacks
    def errb(self, thefailure):
        msg = thefailure.getErrorMessage()
        logging.error(msg)
        if msg.find('CONNECTION_FORCED'):
            client = yield self.connect()
            yield self.open_channel(client)
            logging.error(traceback.format_exc())
