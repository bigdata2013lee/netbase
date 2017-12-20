#! /usr/bin/env python
#coding=utf-8
from products.netModel.observer import Observer
from products.netModel.collector import Collector
from products.netModel.device import Device



class ConfigServiceModel(Observer):

    def __init__(self):
        Observer.__init__(self)
        self.cuid=""

    def getCollectorByHost(self,collectorIp):
        """
            功能:通过收集器IP获取对应的收集器对象
            参数: collectorIp  type->string
            作者:wl
            时间:2013.10.25  
        """
        collector = Collector._loadByHost(collectorIp)
        return collector

    def findDevicesByCollectorIp(self,collectorIp):
        """
                功能:通过收集器IP,加载相应的设备对象列表
                参数: 收集器IP
                作者:wl
                时间:2013.10.25 
        """
        collector=self.getCollectorByHost(collectorIp)
        if not collector: return []
        self.cuid=collector.getUid()
        allDevices=collector.devices
        allDevices.extend(collector.networks)
        return allDevices
    
    def findManageObjsByCollectorIp(self,collectorIp):
        """
        功能:通过收集器IP,加载相应的管理对象列表
        参数: 收集器IP
        作者:wl
        时间:2013.10.25 
        """
        collector=self.getCollectorByHost(collectorIp)
        if not collector: return []
        self.cuid=collector.getUid()
        return collector.getAllMonitorObjs()

    def getDeviceByUid(self,uid):
        """
        功能:通过设备uid获取设备对象
        参数:设备对象uid
        作者:wl
        时间:2013.1.29
        """
        return Device._loadObj(uid)


    def getMonitoredComponents(self,dev):
        """
        获取设备下监控的组件列表
        参数:dev
        类型:device对象
        """
        compList = []
        if hasattr(dev, "interfaces"):
            for interface in dev.interfaces:
                if not interface.monitored:continue
                compList.append(interface)
        if hasattr(dev, "fileSystems"):
            for filesystem in dev.fileSystems:
                if not filesystem.monitored:continue
                compList.append(filesystem)

        return compList
    
    def getDeviceByManageIp(self,collectorIp,IpAddress):
        """
        获取设备对象通过IP
        """
        import pickle
        devObj=None
        devices = self.findDevicesByCollectorIp(collectorIp)
        for dev in devices:
            if not dev.monitored:continue
            if dev.manageIp==IpAddress:
                devObj=dev
                break 
        return pickle.dumps(devObj)

    def remoteGetManageObjConfigs(self):
        """
        远程得到管理对象的配置
        """
        pass
    
    
    
if __name__ == "__main__":
    pass
