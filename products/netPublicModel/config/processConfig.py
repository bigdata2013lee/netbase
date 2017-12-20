#!/usr/bin/env python
#-*- coding:utf-8 -*-
import zlib
from products.netPublicModel.config.snmpConnInfo import SnmpConnInfo
from products.netPublicModel.baseConfigModel import ConfigServiceModel
import logging
log = logging.getLogger("netprocess")

class ProcessConfig():
    """
    进程配置类
    """
    cuid=None
    psid = None
    name = None
    restart = None
    cycleTime = None
    severity = "Warning"
    originalName = None
    componentType = None
    ignoreParameters = False

class DeviceConfig():
    """
    设备配置类
    """
    def __init__(self,cuid,device):
        self.deviceId = device.getUid()
        self.title = device.title
        self.manageIp = device.manageIp
        self.snmpConninfo = SnmpConnInfo(self.manageIp,device.snmpConfig)
        self.thresholds = []
        self.processes = {}
        self.createDeviceProcessConfig(cuid,device)

    def createDeviceProcessConfig(self,cuid,device):
        for p in device.processes:
            if not p.monitored:continue
            proc = ProcessConfig()
            proc.psid = p.getUid()
            proc.cuid=cuid
            proc.name = p.titleOrUid()
            proc.originalName = p.uname
            proc.ignoreParameters = False
            proc.restart = False
            proc.severity = 5
            proc.componentType = p.getComponentType()
            self.processes[proc.psid] = proc
        if not self.processes:
            log.debug("设备%s没有可监控进程"%self.manageIp)
            

class ProcessDeviceConfig(ConfigServiceModel):

    def remoteGetManageObjConfigs(self,collectorIp):
        devices = self.findDevicesByCollectorIp(collectorIp)
        import pickle
        devList = []
        if devices:
            for dev in devices:
                if not dev.monitored:continue
                if not dev.getComponentType()=="Device":continue
                devList.append(DeviceConfig(self.cuid,dev))
        return zlib.compress(pickle.dumps(devList),zlib.Z_BEST_COMPRESSION)
