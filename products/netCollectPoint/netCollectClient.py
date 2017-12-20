#! /usr/bin/env python
#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

__doc__ = """
ip服务客户端
"""
import re
import pickle
from twisted.internet import reactor,protocol,defer
import logging
log = logging.getLogger("netCollect")
from socket import getfqdn
hostname = getfqdn()

class CollectProtocol(protocol.Protocol):
    """
        通过twisted框架创建TCP/IP连接远程连接收集点服务器并返回结果
    """
    defer = None
    data = ""

    def connectionMade(self):
        """
        twisted框架,成功创建连接,发送配置数据
        """
        log.debug("连接到 %s" % self.transport.getPeer().host)
        self.colConfig = self.factory.colConfig
        config=self.colConfig[1]
        print "配置共计%s条"%len(config)
        self.transport.write("<<config:%s>>"%pickle.dumps(config))

    def dataReceived(self,data):
        """
        twisted框架,数据接收函数
        """
        log.debug("%s接收数据: %s",self.colConfig[0][0],data)
        self.data += data
        if self.data.startswith("<<result:") and self.data.endswith(">>"):
            self.factory.resluts=self.data[9:-2]
            self.loseConnection()

    def loseConnection(self):
        """
        twisted框架,连接断开后处理函数
        """
        ip,port = self.transport.addr
        log.debug("失去 %s 端口 %s的连接!",ip,port)
        self.data = ""
        try:
            self.defer.cancel()
        except:
            self.defer = None
        self.transport.loseConnection()

class NetCollectClient(protocol.ClientFactory):
    """
    twisted框架,client类，启动tcp连接
    """
    resluts=""
    deferred = None
    protocol = CollectProtocol

    def __init__(self,colConfig):
        self.colConfig = colConfig

    def clientConnectionLost(self,connector,reason):
        """
        twisted框架,client类，连接断开处理函数
        """
        errorMsg = reason.getErrorMessage()
        if errorMsg != 'Connection was closed cleanly.':
            log.debug("失去IP地址%s端口%s的连接: %s",
                  self.colConfig[0][0],self.colConfig[0][1],reason.getErrorMessage())
        if self.deferred:
            self.deferred.callback(self)
        self.deferred = None

    def clientConnectionFailed(self,connector,reason):
        """
        twisted框架,client类，连接失败处理函数
        """
        log.warn("连接%s (%s) 端口 %s 失败: %s",
                   self.colConfig[0][0],connector.host,self.colConfig[0][1],
                  reason.getErrorMessage())
        if self.deferred:
            self.deferred.callback(self)
        self.deferred = None

    def getDatas(self):
        """
                获取收集点数据
        """
        return pickle.loads(self.resluts)

    def start(self,ipAddress,port):
        """
                启动方法
        """
        d = self.deferred = defer.Deferred()
        reactor.connectTCP(ipAddress,port,self)
        return d
