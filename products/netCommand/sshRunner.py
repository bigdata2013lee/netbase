#!/usr/bin/env python
#-*- coding:utf-8 -*-
from twisted.python import failure
from twisted.internet import defer
from products.netRRD.option import Options
from products.dataCollector.sshClient import SshClient
from products.netUtils.Utils import Timeout
import logging
log = logging.getLogger("netcommand")
MAX_CONNECTIONS = 256
class MySshClient(SshClient):
    """
    功能:SSH客户端类
    作者:wl
    时间:2013-1-7
    """

    def __init__(self,*args,**kw):
        SshClient.__init__(self,*args,**kw)
        self.defers = {}

    def addCommand(self,command):
        """
        功能:添加需要在远端设备上运行的命令
        参数:命令对象
        返回:deffered对象
        作者:wl
        时间:2013-1-7
        """
        d = defer.Deferred()
        self.defers[command] = d
        SshClient.addCommand(self,command)
        return d

    def addResult(self,command,data,code):
        """
        功能:添加结果
        参数:命令对象,命令运行的结果,运行命令的返回值
        作者:wl
        时间:2013-1-7
        """
        SshClient.addResult(self,command,data,code)
        d = self.defers.pop(command,None)
        if d is None:
            log.info("deffered对象不在字典中")
        elif not d.called:
            d.callback((data,code))

    def check(self,ip,timeout = 2):
        return True

    def clientFinished(self):
        """
        功能:关闭客户端
        作者:wl
        时间:2013-1-7
        """
        SshClient.clientFinished(self)
        self.commands = []
        self.results = []

class SshPool:
    """
    功能:SSH连接缓存池
    作者:wl
    时间:2013-1-7
    """

    def __init__(self):
        self.pool = {}

    def get(self,cmd):
        """
        功能:如果没有一个可用的SSH连接就创建一个新的SSH连接
        参数:命令对象
        作者:wl
        时间:2013-1-7
        """
        dc = cmd.manageObjConfig
        result = self.pool.get(dc.manageId,None)
        if result is None:
            options = Options(str(dc.username),str(dc.password),
                              dc.loginTimeout,dc.commandTimeout,
                              str(dc.keyPath),dc.concurrentSessions)
            result = MySshClient(dc.manageId,dc.manageId,dc.port,
                                 options = options)
            result.run()
            self.pool[dc.manageId] = result
        return result

    def _close(self,manageId):
        """
        功能:关闭设备的SSH连接
        参数:设备IP
        作者:wl
        时间:2013-1-7
        """
        c = self.pool.get(manageId,None)
        if c:
            if c.transport:
                c.transport.loseConnection()
            del self.pool[manageId]

    def close(self,cmd):
        """
        功能:关闭连接,get()的对称方法
        参数:命令对象
        作者:wl
        时间:2013-1-7
        """
        self._close(cmd.manageObjConfig.manageId)

    def trimConnections(self,schedule):
        """
        功能:准备连接
        参数:定制任务列表
        作者:wl
        时间:2013-1-7
        """
        # 计算下一次用到的设备列表
        manageIds = []
        for c in schedule:
            manageId = c.manageObjConfig.manageId
            if manageId not in manageIds:
                manageIds.append(manageId)
        #不可以超过其最大连接数,否则关闭一些设备的连接
        while manageIds and len(self.pool) > MAX_CONNECTIONS:
            self._close(manageIds.pop())

class SshRunner:
    """
    功能:SSH运行类,通过缓存的SSH连接运行一个SSH命令
    作者:wl
    时间:2013-1-7
    """

    exitCode = None
    output = None

    def __init__(self,pool):
        self.pool = pool

    def start(self,cmd):
        """
        功能:在远程设备开始运行命令
        作者:wl
        时间:2013-1-7
        """
        self.defer = defer.Deferred()
        c = self.pool.get(cmd)
        try:
            d = Timeout(c.addCommand(cmd.command),
                        cmd.manageObjConfig.commandTimeout,
                        cmd)
        except Exception,ex:
            self.pool.close(cmd)
            return defer.fail(ex)
        d.addErrback(self.timeout)
        d.addBoth(self.processEnded)
        return d

    def timeout(self,arg):
        """
        功能:命令超时
        作者:wl
        时间:2013-1-7
        """
        cmd, = arg.value.args
        self.pool.close(cmd)
        return arg

    def processEnded(self,value):
        """
        功能:结束处理函数
        作者:wl
        时间:2013-1-7
        """
        if isinstance(value,failure.Failure):
            return value
        self.output,self.exitCode = value
        return self
