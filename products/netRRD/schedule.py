#! /usr/bin/env python
#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

from pynetsnmp.twistedsnmp import snmpprotocol

class Schedule:
    """
    功能:SNMP定制任务
    作者:wl
    时间:2013-1-7
    """
    def __init__(self):
        self.schedule = {}
        self.snmpPort = snmpprotocol.port()

    def getSnmpProxy(self,snmpConfig):
        """
        功能:得到一个snmp代理的连接,如果没有就创建
        参数:snmp配置对象
        作者:wl
        时间:2013-1-7
        """
        snmpProxy = snmpConfig.snmpConninfo.createSession(protocol = self.snmpPort.protocol,
                                       allowCache = True)
        snmpProxy.open()
        self.schedule[snmpConfig.deviceId] = snmpProxy
        return snmpProxy

    def close(self,snmpConfig):
        """
        功能:关闭SNMP代理
        参数:设备IP
        作者:wl
        时间:2013-1-7
        """
        snmpProxy = self.schedule.get(snmpConfig.deviceId,None)
        if snmpProxy:
            snmpProxy.close()
            self.schedule.pop(snmpConfig.deviceId)

    def countConnections(self):
        """
        功能:准备连接
        参数:定制任务列表
        作者:wl
        时间:2013-1-7
        """
        #不可以超过其最大连接数,否则关闭一些设备的连接
        return len(self.schedule)