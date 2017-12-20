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
收集点守护进程
'''
from twisted.internet import defer,reactor
from products.netCollectPoint.netCollectClient import NetCollectClient
from products.dataCollector.redisManager import RedisManager
from products.netUtils.deamonBase import DeamonBase
import logging
log = logging.getLogger("netcollectclient")
MAX_RUNNING_DEVICES = 100
FAIL_EVENT_SERVERITY = 5

class netCollectTask(RedisManager):

    def __init__(self,colConfig):
        """
                功能:初始化方法
        """
        self.colConfig = colConfig
        self.collectIp = colConfig[0][0]
        self.collectPort =colConfig[0][1]

    def collectPoint(self):
        """
                连接远端收集点
        """
        ntc = NetCollectClient(self.colConfig)
        return ntc.start(self.collectIp,int(self.collectPort))

    def collectTask(self):
        """
                收集点任务
        """
        d = self.collectPoint()
        d.addCallback(self.processSuccess)
        d.addErrback(self.processError)
        return d

    def processSuccess(self,facObj):
        """
                发送事件
        """
        resluts= facObj.getDatas()
        for reslut in resluts:
            for objRs in reslut:
                insertType=objRs["insertType"]
                del objRs["insertType"]
                if insertType=="event":
                    self.saveEvent(objRs)
                else:
                    self.saveResult(objRs)
        return defer.succeed("连接成功!")

    def processError(self,reason):
        """
                异常处理
        """
        log.warn(reason.getErrorMessage())
        return defer.succeed("连接失败!")

class netcollect(DeamonBase):
    """
        收集点守护进程
    """
    collectCycleInterval = 300

    def __init__(self):
        """
                初始化方法
        """
        DeamonBase.__init__(self)
        self.concurrentNum = 0
        self.colConfigs={}
    
    
    def splitConfig(self):
        """
                按照收集点分割配置
        """
        
    def remoteGetConfigs(self):
        """
                获取配置
        """
        try:
            colConfigs = self.getManageObjConifgs()
            if colConfigs[0]:
                return colConfigs[1]
            else:
                log.error(colConfigs[1])
        except Exception,ex:
            log.error(ex)
        return {}

    def update(self,result):
        """
                并发控制函数
        """
        self.concurrentNum -= 1

    def startTask(self):
        """
                开始运行任务
        """
        for i in xrange(len(self.colConfigs)):
            if self.concurrentNum > MAX_RUNNING_DEVICES:
                break
            self.concurrentNum += 1
            npt = netCollectTask(self.colConfigs.popitem())
            npt.collectTask().addBoth(self.update)
        if self.colConfigs:
            reactor.callLater(1,self.startTask)
    
    @licenseAuth
    def start(self):
        """
                开始运行
        """
        colConfigs = self.remoteGetConfigs()
        if colConfigs:self.colConfigs=colConfigs
        self.startTask()

    def runCycle(self):
        """
                循环运行
        """
        log.info("开始一个循环周期!")
        self.start()
        reactor.callLater(self.collectCycleInterval,self.runCycle)

    def run(self):
        """
                启动reactor
        """
        self.runCycle()
        log.info("开始启动收集点守护进程!")
        reactor.run()
        
    def buildOptions(self):
        DeamonBase.buildOptions(self)
        self.parser.add_option('--csmconfig',dest='csmconfig',
                               default='CollectConfig',
                               help='收集点守护进程配置类,默认为CollectConfig')

if __name__ == "__main__":
    nis = netcollect()
    nis.run()
