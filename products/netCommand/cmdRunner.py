#!/usr/bin/env python
#-*- coding:utf-8 -*-
import time
from twisted.internet import reactor,defer,error
from twisted.internet.protocol import ProcessProtocol
from products.netUtils.Utils import Timeout

class CmdRunner(ProcessProtocol):
    """
    功能:进程运行类,其继承ProcessProtocol类,用户创建一个子进程
    作者:wl
    时间:2013-1-7
    """
    
    stopped = None
    exitCode = None
    output = ''
    stderr=''
    
    def start(self, cmd):
        """
        功能:开始运行进程
        参数:命令对象
        返回:deffered对象
        作者:wl
        时间:2013-1-7
        """
        shell = '/bin/sh'
        self._cmd = cmd
        self.cmdline = (shell, '-c', 'exec %s' % cmd.command)
        self.command = ' '.join(self.cmdline)
        reactor.spawnProcess(self, shell, self.cmdline,env={})
        d = Timeout(defer.Deferred(), 30, cmd)
        self.stopped = d
        self.stopped.addErrback(self.timeout)
        return d

    def timeout(self, value):
        """
                杀死超时进程
        """
        try:
            self.transport.signalProcess('INT')
            reactor.callLater(2, self._reap)
        except error.ProcessExitedAlready:
            pass
        return value

    def _reap(self): 
        """
                杀死超时进程
        """
        try:
            self.transport.signalProcess('KILL')
        except Exception:
            pass

    def outReceived(self, data):
        """
        功能:接受并合并数据
        参数:数据
        返回:命令所有的输出值
        作者:wl
        时间:2013-1-7
        """
        self.output += data
    
    def errReceived(self, data):
        """
            功能:接受错误并合并
        """
        self.stderr += data

    def processEnded(self, reason):
        """
        功能:进程结束
        参数:原因对象
        作者:wl
        时间:2013-1-7
        """
        self.exitCode = reason.value.exitCode
        if self.exitCode is not None:
            data = [self._cmd, self.exitCode, self.output]
            if self.stderr:
                msg= "\n标准错误!:\n%r"
                data.append(self.stderr)

        if self.stopped:
            d, self.stopped = self.stopped, None
            if not d.called:
                d.callback(self)