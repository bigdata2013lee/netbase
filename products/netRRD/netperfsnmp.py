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
__doc__ = """
得到设备性能数据并将其插入到RRD文件中
"""

from twisted.internet import reactor,defer
from datetime import datetime,timedelta

from products.netUtils.chain import Chain
from products.netRRD.schedule import Schedule
from products.dataCollector.redisManager import RedisManager
from products.netUtils.deamonBase import DeamonBase
import logging
log = logging.getLogger("netperfsnmp")

MAX_RUNNING_DEVICES = 100

def checkException(alog,function,*args,**kw):
    """
    功能:检查函数的参数
    参数:函数名,函数参数
    作者:wl
    时间:2013.1.29
    """
    try:
        return function(*args,**kw)
    except Exception,ex:
        raise ex

try:
    sorted = sorted                     # added in python 2.4
except NameError:
    def sorted(lst,*args,**kw):
        """
        适用于python2.4之前的环境
        """
        lst.sort(*args,**kw)
        return lst

def firsts(lst):
    """
    功能:获取元组的第一个参数
    参数:一个元组列表
    作者:wl
    时间:2013.1.29
    """
    return [item[0] for item in lst]

class netPerfSnmpTask(RedisManager):

    def __init__(self,snmpConfig,schedule):
        """
        功能:snmp任务初始化
        参数:SNMP配置,定制任务对象
        作者:wl
        时间:2013-1-17
        """
        self.schedule = schedule
        self.snmpConfig = snmpConfig
        self.snmpProxy = None
        self.snmpConnInfo = snmpConfig.snmpConninfo
        self.device = snmpConfig.manageIp
        self.snmpStatus=self.snmpConfig.snmpStatus

    def connectCallback(self,result):
        """
        功能:流程控制函数
        参数:SNMP连接代理
        作者:wl
        时间:2013-1-17
        """
        log.debug("连接到%s",self.device)
        return result

    def connect(self):
        """
        功能:获取连接
        返回:返回SNMP连接代理
        作者:wl
        时间:2013-1-17
        """
        if (self.snmpProxy is None or
            self.snmpProxy.snmpConnInfo != self.snmpConnInfo):
            self.snmpProxy = self.schedule.getSnmpProxy(self.snmpConfig)

    def readDevices(self,unused = None):
        """
        功能:读取设备性能信息
        作者:wl
        时间:2013.1.29
        """
        self.startTime = datetime.now()
        d = defer.maybeDeferred(self.connect)
        d.addCallbacks(self.connectCallback,self.failure)
        d.addCallback(self.startReadDevice)
        d.addBoth(self.finished)
        return d

    def failure(self,reason):
        """
        功能:失败处理
        作者:wl
        时间:2013-1-22
        """
        msg = reason.getErrorMessage()
        if not msg:
            msg = reason.__class__
        msg = '%s %s' % (self.device,msg)
        return reason

    def finished(self,result):
        """
        功能:结束工作,关闭连接
        作者:wl
        时间:2013.1.29
        """
        try:
            self.schedule.close(self.snmpConfig)
        except Exception,ex:
            log.warn("Failed to close device %s: error %s" %
                     (self.device,str(ex)))

        endTime = datetime.now()
        duration = endTime - self.startTime
        if duration > timedelta(seconds = 60):
            log.warn("Collection for %s took %s seconds; cycle interval is %s seconds." % (
                self.device,duration,60))
        else:
            log.debug("Collection time for %s was %s seconds; cycle interval is %s seconds." % (
                self.device,duration,60))
        return result

    def chunk(self,lst,n):
        """
        功能:列表切割
        参数:列表,步长
        作者:wl
        时间:2013.1.29
        """
        return [lst[i:i + n] for i in xrange(0,len(lst),n)]

    def startReadDevice(self,results):
        """
        功能:读取设备的SNMP性能数据
        作者:wl
        时间:2013.1.29
        """
        #每次请求的最大OID数
        def getLater(oids):
            """
            功能:得到SNMP代理获取的结果
            作者:wl
            时间:2013.1.29
            """

            return checkException("",
                                  self.snmpProxy.get,
                                  oids,
                                  self.snmpProxy.snmpConnInfo.netSnmpTimeout,
                                  self.snmpProxy.snmpConnInfo.netSnmpTries)
        d = Chain(getLater,iter(self.chunk(self.snmpConfig.oidMap.keys(),self.snmpProxy.snmpConnInfo.netMaxOIDPerRequest))).run()
        d.addCallbacks(self.storeValues,self.failure)
        return d

    def storeValues(self,results):
        """
        功能:snmp进程的输出,写入到数据库中
        参数:updates:oid更新值 deviceName:设备名称
        作者:wl
        时间:2013.1.29
        """
        for success,result in results:
            if success:
                for oid,value in result.items():
                    oidObjs = self.snmpConfig.oidMap.get(oid)
                    if not oidObjs:continue
                    for oidObj in oidObjs:
                        if oidObj.get("componentId",""):
                            moUid=oidObj.get("componentId")
                        else:
                            moUid=self.snmpConfig.deviceId
                        #除以时间
                        if oidObj.get("dpName").endswith("Octets"):value=(value*8)
                        if oidObj.get("dpType")=="DERIVE":value=round(value/300.0,3)
                        data = {"moUid":moUid,
                                    "title":oidObj.get("title"),
                                     "componentType":oidObj.get("componentType"),
                                     "templateUid":oidObj.get("tpUid"),
                                     "dataSource":oidObj.get("dsName"),
                                     "dataPoint":oidObj.get("dpName"),
                                     "agent":"netperfsnmp",
                                     "value":value
                        }
                        self.saveResult(data)
            message = self.snmpStatus.updateStatus(success)
            if message:
                severity = 0
                if self.snmpStatus.count:
                    severity = 5
                data = {"moUid":self.snmpConfig.deviceId,
                            "title":self.snmpConfig.devTitle,
                             "componentType":self.snmpConfig.devType,
                             "message":message,
                             "severity":severity,
                             "collector":self.snmpConfig.cuid,
                             "agent":"netperfsnmp"
                }
                self.saveEvent(data)
        return results

class netperfsnmp(DeamonBase):
    """
    功能:定期查询设备的SNMP值
    作者:wl
    时间:2013.1.29
    """

    perfsnmpCycleInterval = 300

    def __init__(self):
        """
        初始化方法
        """
        DeamonBase.__init__(self)
        self.schedule = Schedule()
        self.perfSnmpConfigs = []
        self.totalOids = 0
        self.goodOids = 0

    def getDevicePingIssues(self):
        """
        得到所有PING失败的设备
        """
        return []

    def getDeviceConfig(self):
        """
        功能:获取设备配置信息
        返回:所有设备配置信息
        作者:wl
        时间:2013-1-24
        """
        try:
            snmpConfigs = self.getManageObjConifgs()
            for snmpConfig in snmpConfigs:
                self.totalOids += len(snmpConfig.oidMap)
            log.info("共计获取%d个设备的SNMP配置" % len(snmpConfigs))
            return snmpConfigs
        except Exception,ex:
            log.error(ex)

    def startTask(self):
        """
        功能:开始运行任务
        作者:wl
        时间:2013-1-16
        """
        for i in xrange(len(self.perfSnmpConfigs)):
            if self.schedule.countConnections() > MAX_RUNNING_DEVICES:
                break
            npt = netPerfSnmpTask(self.perfSnmpConfigs.pop(0),self.schedule)
            npt.readDevices().addBoth(self.update)
        if self.perfSnmpConfigs:
            reactor.callLater(1,self.startTask)

    @licenseAuth
    def start(self):
        """
        功能:开始运行
        作者:wl
        时间:2013-1-16
        """
        perfSnmpConfigs = self.getDeviceConfig()
        #如果没有取到取到数据则使用上一次的配置
        if perfSnmpConfigs:self.perfSnmpConfigs=perfSnmpConfigs
        self.startTask()

    def update(self,results):
        """
        结果统计更新
        """
        if results and type(results)==type([]):
            for success,result in results:
                if success:
                    self.goodOids += len(result)

    def resultStatics(self):
        """
        运行结果统计
        """
        message = "周期运行结果统计->totalOids:%d,goodOids:%d,badOids:%d" % (
                self.totalOids,self.goodOids,self.totalOids - self.goodOids)
        log.info(message)
        self.totalOids = 0
        self.goodOids = 0

    def runCycle(self):
        """
        功能:循环运行
        作者:wl
        时间:2013-1-16
        """
        if self.totalOids:
            self.resultStatics()
        self.start()
        reactor.callLater(self.perfsnmpCycleInterval,self.runCycle)

    def run(self):
        """
        启动reactor
        """
        self.runCycle()
        reactor.run()
    
    def buildOptions(self):
        DeamonBase.buildOptions(self)
        self.parser.add_option('--csmconfig',dest='csmconfig',
                               default='SnmpPerConfig',
                               help='SNMP守护进程配置类,默认为SnmpPerConfig')

if __name__ == '__main__':
    npf = netperfsnmp()
    npf.run()
