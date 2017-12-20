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
from twisted.internet import reactor,protocol,defer
from products.netUtils.Utils import unused
import logging
log = logging.getLogger("netipservice")
from socket import getfqdn
hostname = getfqdn()

class ZenTcpTest(protocol.Protocol):
    """
    功能:通过twisted框架创建TCP/IP连接远程连接ip服务并返回结果
    作者:wl
    时间:2013.1.30
    """
    defer = None
    data = ""

    def connectionMade(self):
        """
        功能:twisted框架,成功创建连接，发送测试数据
        作者:wl
        时间:2013.1.30
        """
        log.debug("Connected to %s" % self.transport.getPeer().host)
        self.factory.msg = "pass"
        self.cfg = self.factory.cfg

        if self.cfg.sendString:
            sendString = self.cfg.sendString.decode("string_escape")
            log.debug("Sending: %s",sendString)
            self.transport.write(sendString)

        if self.cfg.expectRegex:
            log.debug("Waiting for results to check against regex '%s'",
                      self.cfg.expectRegex)
            self.defer = reactor.callLater(self.cfg.timeout,self.expectTimeout)
        else:
            self.loseConnection()

    def dataReceived(self,data):
        """
        功能:twisted框架,数据接收函数,正则匹配接收到的数据
        参数:接收到的数据
        作者:wl
        时间:2013.1.30
        """
        log.debug("%s %s received data: %s",self.cfg.manageIp,
                  self.cfg.title,data)
        self.data += data
        if self.cfg.expectRegex:
            if re.search(self.cfg.expectRegex,data):
                log.debug("Found %s in '%s' -- closing connection",
                          self.cfg.expectRegex,data)
                self.loseConnection()
            else:
                log.debug("No match for %s in '%s' -- looking for more data",
                          self.cfg.expectRegex,data)

    def expectTimeout(self):
        """
        功能:数据交互超时处理函数
        作者:wl
        时间:2013.1.30
        """
        msg = "IP Service %s TIMEOUT waiting for '%s'" % (
                    self.cfg.title,self.cfg.expectRegex)
        log.debug("%s %s",self.cfg.manageIp,msg)
        self.factory.msg = msg
        self.loseConnection()

    def loseConnection(self):
        """
        功能:twisted框架,连接断开后处理函数
        作者:wl
        时间:2013.1.30
        """
        ip,port = self.transport.addr
        log.debug("Closed connection to %s on port %s for %s",
                  ip,port,self.cfg.title)
        self.data = ""
        try:
            self.defer.cancel()
        except:
            self.defer = None
        self.transport.loseConnection()


class NetTcpClient(protocol.ClientFactory):
    """
    功能:twisted框架,client类，启动tcp连接
    作者:wl
    时间:2013.1.30
    """
    protocol = ZenTcpTest
    msg = "pass"
    deferred = None

    def __init__(self,svc,status):
        self.cfg = svc
        self.status = status

    def clientConnectionLost(self,connector,reason):
        """
        功能:twisted框架,client类，连接断开处理函数
        参数:twisted protocol对象,twisted error对象
        作者:wl
        时间:2013.1.30
        """
        unused(connector)
        errorMsg = reason.getErrorMessage()
        if errorMsg != 'Connection was closed cleanly.':
            log.debug("Lost connection to %s (%s) port %s: %s",
                  self.cfg.manageIp,self.cfg.manageIp,self.cfg.port,
                  reason.getErrorMessage())
        if self.deferred:
            self.deferred.callback(self)
        self.deferred = None

    def clientConnectionFailed(self,connector,reason):
        """
        功能:twisted框架,client类，连接失败处理函数
        参数:twisted protocol对象,twisted error对象
        作者:wl
        时间:2013.1.30
        """
        log.debug("Connection to %s (%s) port %s failed: %s",
                  self.cfg.manageIp,connector.host,self.cfg.port,
                  reason.getErrorMessage())
        self.msg = "IP Service %s已停止!" % self.cfg.title
        if self.deferred:
            self.deferred.callback(self)
        self.deferred = None

    def getEvent(self):
        """
        功能:获取IP服务事件
        作者:wl
        时间:2013.1.30
        """
        if self.msg == "pass" and self.status > 0:
            self.status = sev = 0
            self.msg = "IP Service %s back up" % self.cfg.title

        elif self.msg != "pass":
            self.status += 1
            sev = self.cfg.failSeverity

        else:
            self.status = sev = 0
            self.msg = "IP Service %s back up" % self.cfg.title

        return dict(manageIp = self.cfg.manageIp,
				    deviceId = self.cfg.deviceId,
                    title=self.cfg.title,
                    cuid=self.cfg.cuid,
                    component = self.cfg.component,
                    componentType = self.cfg.componentType,
                    ipAddress = self.cfg.manageIp,
                    summary = self.msg,
                    severity = sev,
                    eventClass = "",
                    eventGroup = "TCPTest",
                    agent = "netipservice",
                    manager = hostname)

    def start(self,ip_address):
        """
        功能:启动方法
        参数:ip string
        作者:wl
        时间:2013.1.30
        """
        d = self.deferred = defer.Deferred()
        reactor.connectTCP(ip_address.encode("idna"),self.cfg.port,self,3)
        return d
