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
通过SNMP获取设备进程数据
'''
from twisted.internet import reactor
from products.netRRD.schedule import Schedule
from products.netRRD.netProcessTask import NetProcessTask
from products.netUtils.deamonBase import DeamonBase
import logging
log = logging.getLogger("netprocess")
MAX_RUNNING_DEVICES = 100

class netprocess(DeamonBase):
    """
    进程的守护进程,用于判断进程的状态变化和进程的CPU,内存变化情况
    """
    processCycleInterval = 300
    def __init__(self):
        """
        功能:初始化
        作者:wl
        时间:2013-1-15
        """
        DeamonBase.__init__(self)
        self.schedule = Schedule()
        self.processSnmpConfigs = []

    def getDeviceConfig(self):
        """
        功能:获取设备配置信息
        返回:所有设备配置信息
        作者:wl
        时间:2013-1-16
        """
        try:
            processSnmpConfigs =self.getManageObjConifgs()
            log.info("共计获取%d个进程的配置" % len(processSnmpConfigs))
            return processSnmpConfigs
        except Exception,ex:
            log.error(ex)

    def startTask(self):
        """
        功能:开始运行任务
        作者:wl
        时间:2013-1-16
        """
        for i in xrange(len(self.processSnmpConfigs)):
            if self.schedule.countConnections() > MAX_RUNNING_DEVICES:
                break
            npt = NetProcessTask(self.processSnmpConfigs.pop(0),self.schedule)
            npt.handleProcess()
        if self.processSnmpConfigs:
            reactor.callLater(1,self.startTask)
    
    @licenseAuth
    def start(self):
        """
        功能:开始运行
        作者:wl
        时间:2013-1-16
        """
        processSnmpConfigs = self.getDeviceConfig()
        #如果没有取到取到数据则使用上一次的配置
        if processSnmpConfigs:self.processSnmpConfigs=processSnmpConfigs
        self.startTask()

    def runCycle(self):
        """
        功能:循环运行
        作者:wl
        时间:2013-1-16
        """
        self.start()
        reactor.callLater(self.processCycleInterval,self.runCycle)

    def run(self):
        """
        功能:启动
        作者:wl
        时间:2013-1-16
        """
        self.runCycle()
        reactor.run()
        
    def buildOptions(self):
        DeamonBase.buildOptions(self)
        self.parser.add_option('--csmconfig',dest='csmconfig',
                               default='ProcessDeviceConfig',
                               help='进程守护进程配置类,默认为ProcessDeviceConfig')

if __name__ == '__main__':
    np = netprocess()
    np.run()
