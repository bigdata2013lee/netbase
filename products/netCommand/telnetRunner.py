#!/usr/bin/env python
#-*- coding:utf-8 -*-
from twisted.python import failure
from twisted.internet import defer
from products.netRRD.option import Options
from products.dataCollector import telnetClient
from products.netUtils.Utils import Timeout
MAX_CONNECTIONS = 256
    
class TelnetRunner:
    """
    功能:telnet运行类,通过缓存的telnet连接运行一个telnet命令
    作者:lb
    时间:2013-1-10
    """
    exitCode = None
    output = None

    def start(self, cmd):
        """
        功能:在远程设备开始运行命令
        作者:lb
        时间:2013-1-10
        """
        self.defer = defer.Deferred()
        dc = cmd.deviceConfig
        options = Options(dc.username, dc.password,
                          dc.loginTimeout, dc.commandTimeout,
                          dc.keyPath, dc.concurrentSessions)
        result = telnetClient.TelnetClient(dc.device, dc.device, dc.port,
                             options=options)
        result.run()
        try:
            d = Timeout(result.addCommand(cmd.command),
                        cmd.deviceConfig.commandTimeout,
                        cmd)
        except Exception, ex:
            self.pool.close(cmd)
            return defer.fail(ex)
        d.addBoth(self.processEnded)
        return d

    def processEnded(self, value):
        """
        功能:结束处理函数
        作者:lb
        时间:2013-1-10
        """
        if isinstance(value, failure.Failure):
            return value
        self.output, self.exitCode = value
        return self