#! /usr/bin/env python
# -*- coding: utf-8 -*-
import zlib
import pickle
from products.netPublicModel.baseConfigModel import ConfigServiceModel
import logging
log = logging.getLogger("netipservice")

class ServiceConfig():
    """
    功能:服务配置类 
    作者:wl
    时间:2013.1.31
    """
    def __init__(self,svcDict):
        self.deviceId = svcDict["deviceId"]
        self.cuid = svcDict["cuid"]
        self.manageIp = svcDict["manageIp"]
        self.component = svcDict["component"]
        self.componentType = svcDict["componentType"]
        self.title = svcDict["title"]
        self.port = svcDict["port"]
        self.failSeverity = svcDict["failSeverity"]
        self.sendString = svcDict["sendString"]
        self.expectRegex = svcDict["expectRegex"]
        self.protocol = svcDict["protocol"]

class IpServiceConfig(ConfigServiceModel):
    
    def remoteGetManageObjConfigs(self,collectorIp):
        """
        功能:远程获取一个设备的IP服务配置
        参数:收集器uid
        作者:lb
        时间:2013.1.30
        """
        devConfigs =[]
        devices = self.findDevicesByCollectorIp(collectorIp)
        for dev in devices:
            if not dev.monitored:continue
            if not dev.getComponentType()=="Device":continue
            devConfigs.extend(self.getIpServiceConfig(dev))
        return zlib.compress(pickle.dumps(devConfigs),zlib.Z_BEST_COMPRESSION)

    def getIpServiceConfig(self,dev):
        """
        功能:远程获取一个设备的IP服务配置
        参数:收集器uid
        作者:lb
        时间:2013.1.30
        """
        serConfigs = []
        for sev in dev.ipServices:
            if not sev.monitored:continue
            deviceId = dev.getUid()
            manageIp = dev.manageIp
            protocol = sev.protocol
            component = sev.getUid()
            componentType =sev.getComponentType()
            port = sev.port
            failSeverity = 5
            title = sev.titleOrUid()
            sendString = ""
            expectRegex =""
            serConfigs.append(ServiceConfig(dict(deviceId = deviceId,
                                cuid=self.cuid,
                                 protocol = protocol,
                                 title = title,
                                 component = component,
                                 componentType=componentType,
                                 failSeverity = failSeverity,
                                 port = port,
                                 manageIp = manageIp,
                                 sendString = sendString,
                                 expectRegex = expectRegex)))
        if not serConfigs:
            log.debug("设备%s没有可监控服务"%dev.manageIp)
        return serConfigs

    
