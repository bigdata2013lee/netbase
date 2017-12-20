#! /usr/bin/env python
#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

import time
import socket
import os,sys
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, defer, udp
from twisted.python import failure
from products.netLog.syslogProcessor import SyslogProcessor
from products.netUtils.IpUtil import asyncNameLookup
from products.netUtils.deamonBase import DeamonBase
from products.netUtils.logger import Logging
log = Logging.getLogger("nbsyslog")

SYSLOG_PORT = 514
try:
    SYSLOG_PORT = socket.getservbyname('syslog', 'udp')
except socket.error:
    pass

class Stats:
    """
    功能:日志统计状态类
    作者:wl
    时间:2013.3.13
    """
    def __init__(self):
        """
        功能:初始化
        作者:wl
        时间:2013.3.13
        """
        self.totalTime = 0
        self.totalEvents = 0
        self.maxTime = 0
    
    def add(self, rtime):
        """
        功能:日志单次统计结果更新
        作者:wl
        时间:2013.3.13
        """
        self.totalEvents += 1
        moreTime = time.time() - rtime
        self.maxTime = max(self.maxTime, moreTime)
        if not self.totalTime:
            self.totalTime = rtime

    def update(self,mod):
        """
        功能:日志批量统计结果更新
        作者:wl
        时间:2013.3.13
        """
        self.totalEvents = self.totalEvents % mod
        self.totalTime = time.time() - self.totalTime
    
    def clear(self):
        """
        功能:日志统计状态清零
        作者:wl
        时间:2013.3.13
        """
        self.totalTime = 0
    
    def report(self):
        """
        功能:日志统计状态报告
        作者:wl
        时间:2013.3.13
        """
        return self.totalTime, self.totalEvents, self.maxTime

class nbsyslog(DatagramProtocol,DeamonBase):
    """
    功能:监听syslog任务
    作者:wl
    时间:2013.3.13
    """
    EVENT_MOD = 100
    SAMPLE_DATE = 'Apr 10 15:19:22'
    SYSLOG_DATE_FORMAT = '%b %d %H:%M:%S'
    
    def __init__(self):
        """
        功能:初始化
        作者:wl
        时间:2013.3.13
        """
        DeamonBase.__init__(self)
        self.stats = Stats()
        self.processor = None
        
    def useUdpFileDescriptor(self, fd):
        """
        功能:使用UDP文件描述
        作者:wl
        时间:2013.3.13
        """
        s = socket.fromfd(fd, socket.AF_INET, socket.SOCK_DGRAM)
        os.close(fd)
        port = s.getsockname()[1]
        transport = udp.Port(port, self)
        s.setblocking(0)
        transport.socket = s
        transport.fileno = s.fileno
        transport.connected = 1
        transport._realPortNumber = port
        self.transport = transport
        self.numPorts = 1
        transport.startReading()
    
    def doTask(self):
        """
        功能:开始任务
        作者:wl
        时间:2013.3.13
        """
        reactor.listenUDP(self.options.syslogport, self,interface=self.options.listenip)
        minpriority=self.options.minpriority
        parsehost=self.options.parsehost
        monitor=""
        defaultPriority=3
        self.processor = SyslogProcessor(minpriority,parsehost,monitor,defaultPriority,self.stats)
        return defer.succeed("等待接收日志消息...")

    def expand(self, msg, client_address):
        """
        功能:解析
        作者:wl
        时间:2013.3.13
        """
        stop = msg.find('>')
        start = stop + 1
        stop = start + len(self.SAMPLE_DATE)
        dateField = msg[start:stop]
        try:
            date = time.strptime(dateField,self.SYSLOG_DATE_FORMAT)
            year = time.localtime()[0]
            date = (year, ) + date[1:]
            start = stop + 1
        except ValueError:
            date = time.localtime()
        stop = msg.find(' ', start)
        if msg[stop - 1] == ':':
            hostname = client_address[0]
        else:
            hostname = msg[start:stop]
            start = stop + 1
        body = msg[start:]
        prettyTime = time.strftime(self.SYSLOG_DATE_FORMAT, date)
        message = '%s %s %s' % (prettyTime, hostname, body)
        return message
    
    def datagramReceived(self, msg, client_address):
        """
        功能:数据接收
        作者:wl
        时间:2013.3.13
        """
        (ipaddr, port) = client_address
        try:
            msg = msg.decode('gbk')
        except:
            log.info("日志信息不是gbk编码格式")
        try:
            msg = msg.encode('utf-8')
        except:
            log.info("日志信息encode utf-8失败")
            
        message=self.expand(msg, client_address)
        log.debug(message)
        if self.options.noreverseLookup:
            d = defer.succeed(ipaddr)
        else:
            d = asyncNameLookup(ipaddr)
        d.addBoth(self.gotHostname, (msg, ipaddr, time.time()))
        d.addCallback(self.showStatistics)

    def gotHostname(self, response, data):
        """
        功能:获取主机名
        作者:wl
        时间:2013.3.13
        """
        (msg, ipaddr, rtime) = data
        if isinstance(response, failure.Failure):
            host = ipaddr
        else:
            host = response
        if self.processor:
            self.processor.process(msg, ipaddr, host, rtime)  
        return data
              

    def showStatistics(self,result):
        """
        功能:显示统计信息
        作者:wl
        时间:2013.3.13
        """
        if self.stats.totalEvents > self.EVENT_MOD:
            self.stats.update(self.EVENT_MOD)
            totalTime, totalEvents, maxTime = self.stats.report()
            log.info("平均处理一条消息花费%.5f秒",
                      (totalTime / self.EVENT_MOD))
            log.info("%s条时间消耗%f秒"%
                      (self.EVENT_MOD,totalTime))
            log.info("每条消息处理耗最大运行时间为%.5f秒",
                      maxTime)
            self.stats.clear()
    
    def buildOptions(self):
        """
        功能:命令行参数
        作者:wl
        时间:2013.3.13
        """
        DeamonBase.buildOptions(self)
        self.parser.add_option('--parsehost', dest='parsehost',
                               action='store_true', default=False,
                               help='尝试解析系统日志HEADER部分的主机名'
                               )
        self.parser.add_option('--minpriority', dest='minpriority',
                               default=7, type='int',
                               help='系统可接受的最小日志级别'
                               )
        self.parser.add_option('--syslogport', dest='syslogport',
                               default=SYSLOG_PORT, type='int',
                               help='系统日志监听端口'
                               )
        self.parser.add_option('--noreverseLookup', dest='noreverseLookup',
                               action='store_true', default=False,
                               help="不将远程设备IP转换成主机名"
                               )
    
    def run(self):
        """
        功能:启动
        作者:wl
        时间:2013.3.13
        """
        self.doTask()
        reactor.run()

if __name__ == '__main__':
    np = nbsyslog()
    np.run()