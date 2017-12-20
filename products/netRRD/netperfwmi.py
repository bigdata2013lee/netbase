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

__doc__="""netperfwmi
得到WMI性能数据,并将其放入到内存数据库"""

import pysamba.twisted.reactor
from twisted.internet import defer, reactor
from twisted.python.failure import Failure
from products.netRRD.wmiClient import WMIClient
from products.netRRD.schedule import Schedule
from products.dataCollector.redisManager import RedisManager
from products.netUtils.deamonBase import DeamonBase
import logging
log = logging.getLogger("netperfwmi")

Clear, Debug, Info, Warning, Error, Critical = xrange(6)

MAX_RUNNING_DEVICES=100

class netPerfWmiTask(RedisManager):
    """
    wmi任务类
    """
    QUERIES = 0
    STATE_WMIC_CONNECT = 'WMIC_CONNECT'
    STATE_WMIC_QUERY = 'WMIC_QUERY'
    STATE_WMIC_PROCESS = 'WMIC_PROCESS'

    def __init__(self,wmiConfig,schedule):
        """
        功能:进程任务初始化
        参数:SNMP配置,定制任务对象
        作者:wl
        时间:2013-1-17
        """
        self.wmiConfig=wmiConfig
        self.device=self.wmiConfig.manageIp
        self.schedule = schedule
        #self.radisClient = radisClient
        
    def failure(self, result, comp=None):
        """
        功能:失败处理
        作者:wl
        时间:2013-1-17
        """
        err = result.getErrorMessage()
        log.error("Device %s: %s", self.device, err)
#         message="设备%sWMI获取数据异常,请检查"%self.device
#         data = {"moUid":self.wmiConfig.objId,
#                     "title":self.device,
#                      "componentType":"",
#                      "message":message,
#                      "severity":5,
#                      "eventClass":"/status",
#                      "collector":self.wmiConfig.cuid,
#                      "agent":"netperfwmi"
#         }
#         self.saveEvent(data)
        return result

    def collectSuccessful(self, results):
        """
        收集成功
        """
        self.state = netPerfWmiTask.STATE_WMIC_PROCESS
        log.debug("%s [%s]数据收集成功, results=%s",
                  self.wmiConfig.manageIp, self.wmiConfig.manageIp, results)
        if not results: return None
        for tableName, datas in results.iteritems():
            for moUid,title,componentType,templateUid,dataSource,\
                dpname,dpType in self.wmiConfig.datapoints[tableName]:
                for data in datas:
                    dpvalue=data.get(dpname)
                    if dpvalue == None: continue
                    if dpType=="DERIVE":dpvalue=round(dpvalue/300.0,3)
                    data = {"moUid":moUid,
                        "title":title,
                         "componentType":componentType,
                         "templateUid":templateUid,
                         "dataSource":dataSource,
                         "dataPoint":dpname,
                         "agent":"netperfwmi",
                         "value":dpvalue}
                    self.saveResult(data)
                severity=5
                message="%s获取数据异常!"%title
                if len(datas)>0:
                    severity=0
                    message="%s获取数据正常!"%title
                data = {"moUid":moUid,
                            "title":title,
                             "componentType":componentType,
                             "message":message,
                             "severity":severity,
                             "eventClass":"/status",
                             "collector":self.wmiConfig.cuid,
                             "agent":"netperfwmi"
                }
                self.saveEvent(data)
        return results

    def collectData(self):
        """
        收集数据
        """
        self.state = netPerfWmiTask.STATE_WMIC_QUERY
        wmic = WMIClient(self.wmiConfig)
        d = wmic.sortedQuery(self.wmiConfig.queries)
        d.addCallbacks(self.collectSuccessful, self.failure)
        return d

    def doTask(self):
        """
        执行任务
        """
        d = self.collectData()
        d.addCallback(self.finished)
        return d
    
    def finished(self, result):
        """
        完成
        """
        if not isinstance(result, Failure):
            log.debug("Device %s scanned successfully",
                      self.device)
        else:
            log.debug("Device %s scanned failed, %s",
                      self.device, result.getErrorMessage())

        return result

class netperfwmi(DeamonBase):
    """
    WMI守护进程
    """
    perfWmiCycleInterval = 60

    def __init__(self):
        """
        初始化方法
        """
        DeamonBase.__init__(self)
        self.schedule = Schedule()
        self.perfWmiConfigs = []

    def getDevicePingIssues(self):
        """
        得到所有PING失败的设备
        """
        return []

    def startTask(self):
        """
        功能:开始运行任务
        作者:wl
        时间:2013-1-16
        """
        for i in xrange(len(self.perfWmiConfigs)):
            if self.schedule.countConnections() > MAX_RUNNING_DEVICES:
                break
            npt = netPerfWmiTask(self.perfWmiConfigs.pop(0),self.schedule)
            npt.doTask()
        if self.perfWmiConfigs:
            reactor.callLater(1,self.startTask)
            
    def getManageObjConfig(self):
        """
                功能:得到所有的设备配置
                返回:所有设备的配置列表
                作者:wl
                时间:2013-1-6
        """
        wmiConfigs=[]
        log.info("before getconfig")
        configResults = self.getManageObjConifgs()
        if configResults[0]:
            wmiConfigs=configResults[1]
            log.info("共计获取%d个设备的配置" % len(wmiConfigs))
        else:
            log.error(configResults[1])
        return wmiConfigs

    @licenseAuth
    def start(self):
        """
        功能:开始运行
        作者:wl
        时间:2013-1-16
        """
        perfWmiConfigs = self.getManageObjConfig()
        #如果没有取到取到数据则使用上一次的配置
        if perfWmiConfigs:self.perfWmiConfigs=perfWmiConfigs
        self.startTask()

    def runCycle(self):
        """
        功能:循环运行
        作者:wl
        时间:2013-2-21
        """
        self.start()
        reactor.callLater(self.perfWmiCycleInterval,self.runCycle)

    def run(self):
        """
        启动reactor
        """
        self.runCycle()
        reactor.run()

    def buildOptions(self):
        DeamonBase.buildOptions(self)
        self.parser.add_option('--csmconfig',dest='csmconfig',
                               default='WmiConfig',
                               help='SNMP守护进程配置类,默认为SnmpPerConfig')
        
if __name__ == '__main__':
    npw = netperfwmi()
    npw.run()
