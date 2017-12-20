#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.cc
#
#
###########################################################################
from products.netPublicModel.collectorLicense import licenseAuth
__doc__ = '''
Ping守护进程
'''

import time
from twisted.internet import reactor,defer
from products.netPing.AsyncPing import Ping,PingJob
from products.dataCollector.redisManager import RedisManager
from products.netUtils.deamonBase import DeamonBase
import logging
log = logging.getLogger("netping")

class netping(RedisManager,DeamonBase):
    """
    功能:PING类
    作者:wl
    时间:2013-1-22
    """
    monitorUnknownCycleInterval = 10
    mintorUnknownDevice = []
    pingCycleInterval = 60

    def __init__(self):
        """
        功能:初始化PING对象
        作者:wl
        时间:2013-1-22
        """
        DeamonBase.__init__(self)
        self.pinger = Ping()
        self.pingConfigs=[]

    def getDeviceConfig(self):
        """
        功能:得到设备配置
        返回:所有设备配置对象列表
        作者:wl
        时间:2013-1-22
        """
        log.info("before getconfig")
        try:
            pingConfigs = self.getManageObjConifgs()
            log.info("共计获取%d个设备的配置" % len(pingConfigs))
            return pingConfigs
        except Exception,ex:
            log.error(ex)

    def connected(self):
        """
        功能:连接控制函数
        作者:wl
        时间:2013-1-22
        """
        lst = defer.DeferredList(map(self.ping,self.pingConfigs),consumeErrors = True)
        lst.addCallback(self.pingResult,time.time())
    
    @licenseAuth
    def start(self):
        """
        功能:开始运行
        作者:wl
        时间:2013-1-16
        """
        pingConfigs = self.getDeviceConfig()
        #如果没有取到取到数据则使用上一次的配置
        if pingConfigs:self.pingConfigs=pingConfigs
        self.connected()

    def runCycle(self):
        """
        功能:循环调用函数
        作者:wl
        时间:2013-1-22
        """
        try:
            self.start()
        except Exception,ex:
            log.error(ex.message)
        reactor.callLater(self.pingCycleInterval,self.runCycle)

    def ping(self,pingConfig):
        """
        功能:PING发送
        作者:wl
        时间:2013-1-22
        """
        pj = PingJob(pingConfig)
        self.pinger.sendPacket(pj)
        return pj.deferred

    def pingResult(self,results,start):
        """
        功能:获取PING结果并保存
        作者:wl
        时间:2013-1-22
        """
        good = [pj for s,pj in results if s and pj.rtt >= 0]
        bad = [err.value for s,err in results if not s]
        for g in good:self.save(g,0)
        for b in bad:self.save(b,5)

    def save(self,pingJob,severity):
        """
        功能:保存PING结果至redis
        作者:wl
        时间:2013-1-22
        """
        data = {
          'moUid':pingJob.deviceId,
          'title':pingJob.title,
          "componentType":pingJob.componentType,
          "message":pingJob.message,
          "severity":severity,
          "eventClass":"/status",
          "collector":pingJob.cuid,
          "agent":"netping"
        }
        self.saveEvent(data)

    def run(self):
        """
        功能:启动
        作者:wl
        时间:2013-1-22
        """
        self.runCycle()
        reactor.run()
        
    def buildOptions(self):
        DeamonBase.buildOptions(self)
        self.parser.add_option('--csmconfig',dest='csmconfig',
                               default='PingConfig',
                               help='ping守护进程配置类,默认为PingConfig')

if __name__ == '__main__':
    np = netping()
    np.run()
