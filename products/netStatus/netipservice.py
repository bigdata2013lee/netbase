#! /usr/bin/env python
#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################
from products.netPublicModel.collectorLicense import licenseAuth

__doc__ = '''
IP服务守护进程
'''
from twisted.internet import defer,reactor
from products.netStatus.netTcpClient import NetTcpClient
from products.dataCollector.redisManager import RedisManager
from products.netUtils.deamonBase import DeamonBase
import logging
log = logging.getLogger("netipservice")
MAX_RUNNING_DEVICES = 1000
FAIL_EVENT_SERVERITY = 5


class netIpServiceTask(RedisManager):

    def __init__(self,serviceConfig):
        """
        功能:初始化方法
        参数:服务配置对象,任务调试对象,redis终端
        作者:wl
        时间:2013.1.30
        """
        self.serviceConfig = serviceConfig
        self.device = serviceConfig.manageIp

    def scanDevice(self,ipAddress):
        """
        功能:扫描设备
        参数:设备ip
        作者:wl
        时间:2013.1.30
        """
        ntc = NetTcpClient(self.serviceConfig,0)
        return ntc.start(ipAddress)

    def serviceTask(self):
        """
        功能:IP服务定制任务
        作者:wl
        时间:2013.1.30
        """
        d = self.scanDevice(self.device)
        d.addCallback(self.processSuccess)
        d.addErrback(self.processError)
        return d

    def processSuccess(self,result):
        """
        功能:发送事件
        参数:结果
        作者:lb
        时间:2013-2-1
    	"""
        evt = result.getEvent()
        severity = evt.get('severity',0)
        dictMap={'critical':5, 'error':4, 'warning':3, 'info':2, 'debug':1, 'clear':0}
        severity=dictMap.get(severity,severity)
        data = {"moUid":evt.get("component"),
                            "title":evt.get("title"),
                             "componentType":evt.get("componentType"),
                             "message":evt.get("summary",""),
                             "severity":severity,
                             "eventClass":"/status",
                             "collector":evt.get("cuid"),
                             "agent":"netipservice"
        }
        if evt['severity'] != 0:
            data['severity'] = FAIL_EVENT_SERVERITY
            self.saveEvent(data)
            return defer.succeed("Failed")
        self.saveEvent(data)
        return defer.succeed("Connected")

    def processError(self,reason):
        """
        功能:异常处理
        参数:reason 异常对象
        作者:wl
        时间:2013.1.30
        """
        log.warn(reason.getErrorMessage())
        return defer.succeed("Failed due to internal error")

class netipservice(DeamonBase):
    """
    功能:IP服务守护进程
    作者:wl
    时间:2013.1.30
    """
    serviceCycleInterval = 300
    uidGroupLen = 200

    def __init__(self):
        """
        功能:初始化方法
        作者:wl
        时间:2013.1.30
        """
        DeamonBase.__init__(self)
        self.concurrentNum = 0
        self.sevConfigs=[]

    def remoteGetConfigs(self):
        """
        功能:通过配置对象UID列表批量获取对象下的服务配置对象
        参数:配置对象uid列表
        作者:wl
        时间:2013.1.29
        """
        try:
            sevConfigs = self.getManageObjConifgs()
            return sevConfigs
        except Exception,ex:
            log.error(ex)

    def update(self,result):
        """
        功能:并发控制函数
        作者:lb
        时间:2013-1-16
        """
        self.concurrentNum -= 1

    def startTask(self):
        """
        功能:开始运行任务
        作者:wl
        时间:2013-1-16
        """
        for i in xrange(len(self.sevConfigs)):
            if self.concurrentNum > MAX_RUNNING_DEVICES:
                break
            self.concurrentNum += 1
            npt = netIpServiceTask(self.sevConfigs.pop(0))
            npt.serviceTask().addBoth(self.update)
        if self.sevConfigs:
            reactor.callLater(1,self.startTask)

    @licenseAuth
    def start(self):
        """
        功能:开始运行
        作者:wl
        时间:2013-1-16
        """
        sevConfigs = self.remoteGetConfigs()
        #如果没有取到取到数据则使用上一次的配置
        if sevConfigs:self.sevConfigs=sevConfigs
        self.startTask()

    def runCycle(self):
        """
        功能:循环运行
        作者:wl
        时间:2013-1-16
        """
        self.start()
        reactor.callLater(self.serviceCycleInterval,self.runCycle)

    def run(self):
        """
        功能:启动reactor
        作者:wl
        时间:2013-1-16
        """
        self.runCycle()
        log.info("开始启动服务的守护进程!")
        reactor.run()
        
    def buildOptions(self):
        DeamonBase.buildOptions(self)
        self.parser.add_option('--csmconfig',dest='csmconfig',
                               default='IpServiceConfig',
                               help='服务守护进程配置类,默认为IpServiceConfig')

if __name__ == "__main__":
    nis = netipservice()
    nis.run()
