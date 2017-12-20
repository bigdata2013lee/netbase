#!/usr/bin/env python
#coding=utf-8
import re
import os
import zlib
from products.netPublicModel.config.snmpConnInfo import SnmpConnInfo
from products.netPublicModel.baseConfigModel import ConfigServiceModel
import logging
log = logging.getLogger("netperfsnmp")

class SnmpStatus:
    """
    功能:设备SNMP状态
    作者:wl
    时间:2013.1.29
    """
    def __init__(self,snmpState):
        """
        功能:初始化方法
        参数:设备snmp服务状态值
        作者:wl
        时间:2013.1.29
        """
        self.count=snmpState

    def updateStatus(self,success):
        """
        功能:更新SNMP状态
        参数:设备名,snmp结果状态,事件
        作者:wl
        时间:2013.1.29
        """
        if success:
            summary = 'SNMP服务已启动'
            self.count = 0
            return summary
        else:
            summary = 'SNMP服务已停止'
            self.count += 1
        return summary

class SnmpConfig():
    """
    功能:SNMP配置数据类
    作者:wl
    时间:2013.1.29
    """
    def __init__(self,cuid,dev,devConfig):
        """
        功能:SNMP配置数据初始化
        参数:配置对象
        作者:wl
        时间:2013.1.29
        """
        self.deviceId = dev.getUid()
        self.cuid=cuid
        self.manageIp = dev.manageIp
        self.devType = dev.getComponentType()
        self.devTitle = dev.titleOrUid()
        self.snmpConninfo = SnmpConnInfo(dev.manageIp,dev.snmpConfig)
        self.oidMap = devConfig
        self.snmpStatus = SnmpStatus(0)

class SnmpPerConfig(ConfigServiceModel):

    def remoteGetManageObjConfigs(self,collectorIp):
        """
        功能:远程获取收集器下的符合条件的所有设备
        参数:收集器对象uid
        作者:wl
        时间:2013.2.26
        """
        import pickle
        snmpConfigs = []
        devices = self.findDevicesByCollectorIp(collectorIp)
        for dev in devices:
            if not dev.monitored:continue
            status = dev.getPingStatus()
            if not status:continue
            oidMap = self.getComponentConfig(dev)
            for comp in self.getMonitoredComponents(dev):
                oidMap.update(self.getComponentConfig(comp))
            snmpConfigs.append(SnmpConfig(self.cuid,dev,oidMap))
        return zlib.compress(pickle.dumps(snmpConfigs),zlib.Z_BEST_COMPRESSION)

    def remoteGetSnmpDeviceConfig(self,collectorIp,ipAddress):
        import pickle
        devConfig =None
        devices = self.findDevicesByCollectorIp(collectorIp)
        for dev in devices:
            if dev.manageIp==ipAddress:
                oidMap = self.getComponentConfig(dev)
                for comp in self.getMonitoredComponents(dev):
                    oidMap.update(self.getComponentConfig(comp))
                devConfig=SnmpConfig(self.cuid,dev,oidMap)
                break
        return pickle.dumps(devConfig)
    
    def transformOid(self,oid,comp):
        """
        根据OID索引转化为OID
        """
        oid = '.' + oid.strip(".")
        snmpIndex = getattr(comp,"snmpIndex","")
        if snmpIndex: oid = "%s.%s" % (oid,snmpIndex)
        return oid

    def getComponentConfig(self,comp):
        """
        功能:获取组件下的所有配置
        参数:配置对象
        作者:wl
        时间:2013.2.26
        """
        oidMap = {}
        title = comp.titleOrUid()
        validOid = re.compile(r'(?:\.?\d+)+$')
        componentType = comp.getComponentType()
        componentId = componentType != "Device" and comp.getUid() or ""
        for tp in comp.templates:
            if not tp:continue
            for dsName,ds in tp.findDataSources("SnmpDataSource").iteritems():
                execCycle=ds.get("execCycle")
                for dpName ,dp in ds.dataPoints.iteritems():
                    if not ds.get("monitored"): continue
                    oid=dp.get("oid")
                    tpUid = tp.getUid()
                    dpType = dp.get("type","GUAGE")
                    if not oid:
                        log.warn("数据源%s上没有填写OID"%dsName)
                        continue
                    oid=self.transformOid(oid, comp)
                    if not validOid.match(oid):
                        log.warn("OID%格式不正确"%oid)
                        continue
                    if not oidMap.has_key(oid):oidMap[oid] = []
                    oidMap.get(oid,[]).append(dict(componentId = componentId,componentType = componentType,
                                                   dpName = dpName,dpType=dpType,dsName = dsName,tpUid = tpUid,execCycle=execCycle,title=title))
        return oidMap
