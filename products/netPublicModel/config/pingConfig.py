#!/usr/bin/env python
#-*- coding:utf-8 -*-
import zlib
import pickle
from products.netPublicModel.baseConfigModel import ConfigServiceModel
import logging
log = logging.getLogger("netping")

class DeviceConfig():
    '''
    功能:Ping下的设备配置类
    作者:wl
     时间:2013-1-22
    '''
    def __init__(self,cuid,dev):
        '''
        功能:ping配置类
        作者:wl
        时间:2013-1-22
        '''
        self.deviceId = dev.getUid()
        self.cuid=cuid
        self.deviceIp = dev.manageIp
        self.devicePort =dev.commConfig.get("hcPorts","80")
        self.hcType =dev.commConfig.get("hcType","ping") #取值类型：ping/端口
        self.title = dev.titleOrUid()
        self.componentType = dev.getComponentType()

class PingConfig(ConfigServiceModel):
    '''
    功能:Ping配置类
    作者:wl
     时间:2013-1-22
    '''
    def remoteGetManageObjConfigs(self,collectorIp):
        """
        功能:远程获取收集器下设备的Ping配置
        参数:收集器对象uid
        作者:wl
        时间:2013.2.26
        """
        objs = self.findManageObjsByCollectorIp(collectorIp)
        pingConfigs = []
        if objs:
            for obj in objs:
                if not (obj.getComponentType()=="Device" or obj.getComponentType()=="Network" or
                obj.getComponentType()=="Bootpo"):continue
                if hasattr(obj, "monitored") and not obj.monitored:continue
                pingConfigs.append(DeviceConfig(self.cuid,obj))
        return zlib.compress(pickle.dumps(pingConfigs),zlib.Z_BEST_COMPRESSION)
