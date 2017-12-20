#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

import sys
import logging
log = logging.getLogger("SnmpClient")

from twisted.internet import reactor, error, defer
from twisted.python import failure
from twisted.internet.error import TimeoutError,ReactorNotRestartable

from pynetsnmp.twistedsnmp import snmpprotocol

from products.netUtils.driver import drive

global defaultTries, defaultTimeout
defaultTries = 2
defaultTimeout = 5

DEFAULT_MAX_OIDS_BACK = 40

from products.dataCollector.baseClient import BaseClient

class SnmpClient(BaseClient):

    def __init__(self, hostname, ipaddr, options=None, device=None, 
                 datacollector=None,connInfo=None, plugins=[]):
        BaseClient.__init__(self, device, datacollector)
        global defaultTries, defaultTimeout
        self.hostname = hostname
        self.device = device
        self.options = options
        self.datacollector = datacollector
        self.plugins = plugins
        self.connInfo=connInfo
        self._getdata = {}
        self._tabledata = {}
        self.proxy = None

    def initSnmpProxy(self):
        if self.proxy is not None: self.proxy.close()
        srcport = snmpprotocol.port()
        self.proxy = self.connInfo.createSession(srcport.protocol)
        self.proxy.open()
        
    def start(self):
        """
        开始snmp收集
        """
        self.initSnmpProxy()
        drive(self.doRun).addBoth(self.clientFinished)

    def doRun(self, driver):
        log.debug("测试SNMP配置")
        yield self.proxy.walk('1.3.6')
        try:
            driver.next()
        except TimeoutError, ex:
            errMsg="连接设备%s超时"%self.hostname
            log.info(errMsg)
            return
        except Exception, ex:
            errMsg="设备%s无法进行通讯"%self.hostname
            log.exception(errMsg)
            self.datacollector.transportWrite({"message":errMsg,"data":[]})
            return
        changed = True
        if changed:
            yield drive(self.collect)


    def collect(self, driver):
        for plugin in self.plugins:
            try:
                pname = plugin.name()
                log.debug('启用 %s', pname)
                self._tabledata[pname] = {}
                log.debug("向插件%s发送查询信息", pname)
                if plugin.snmpGetMap:
                    yield self.proxy.get(plugin.snmpGetMap.getoids())
                    self._getdata[pname] = driver.next()
                for tmap in plugin.snmpGetTableMaps:
                    rowSize = len(tmap.getoids())
                    maxRepetitions = max(DEFAULT_MAX_OIDS_BACK / rowSize, 1)
                    yield self.proxy.getTable(tmap.getoids(),
                                              maxRepetitions=maxRepetitions,
                                              limit=sys.maxint)
                    self._tabledata[pname][tmap] = driver.next()
            except Exception, ex:
                if not isinstance( ex, error.TimeoutError ):
                    errMsg="设备%s插件%s非预期的错误"
                    log.exception(errMsg,self.hostname, pname)
                    self.datacollector.transportWrite({"message":errMsg%(self.hostname, pname),"data":[]})

    def getResults(self):
        """
        获取结果
        ((plugin, (getdata, tabledata),)
        getdata = {'.1.2.4.5':"value",}
        tabledata = {tableMap : {'.1.2.3.4' : {'.1.2.3.4.1': "value",...}}} 
        """
        data = []
        for plugin in self.plugins:
            pname = plugin.name()
            getdata = self._getdata.get(pname,{})
            tabledata = self._tabledata.get(pname,{})
            if getdata or tabledata:
                data.append((plugin, (getdata, tabledata)))
        return data 

    def clientFinished(self, result):
        log.info("snmp客户端完成对%s信息的收集" % self.hostname)
        if isinstance(result, failure.Failure):
            from twisted.internet import error
            if isinstance(result.value, error.TimeoutError):
                errMsg="连接设备%s超时:请检查snmp配置是否正确?"
                log.warning(errMsg,self.hostname)
                self.datacollector.transportWrite({"message":errMsg%self.hostname,"data":[]})
            else:
                errMsg="设备%s存在错误:%s"
                log.error(errMsg, self.hostname, result)
                self.datacollector.transportWrite({"message":errMsg%(self.hostname,result),"data":[]})
        self.proxy.close()
        if self.datacollector:
            self.datacollector.clientFinished(self)
        else:
            reactor.stop()

    def stop(self):
        """
        关闭snmp代理
        """
        if self.proxy:
            self.proxy.close()
