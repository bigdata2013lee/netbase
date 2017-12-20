#!/usr/bin/env python
#-*- coding=utf-8 -*-

import time
import types
import pickle
from products.netUtils import xutils
from products.netModel.observer import Observer
from products.netModel.network import Network
from products.netModel.middleware.mwApache import MwApache
from products.netModel.middleware.mwTomcat import MwTomcat
from products.netModel.middleware.mwNginx import MwNginx
from products.netModel.middleware.mwIis import MwIis
from products.netModel.device import Device
from products.netModel.website import Website
from products.netModel.middleware.mwBase import MwBase
from products.netModel.collector import Collector
from products.netModel.mongodbManager import getNetPerfDB




class DataRoot(Observer):
    """
    功能:公共模型，向系统提供各种服务，它也是Rpyc服务内容的提供者之一
    """


    def __init__(self):
        Observer.__init__(self) 

    def __getOrgTypes(self):
        from products.netModel.org.deviceClass import DeviceClass
        from products.netModel.org.networkClass import NetworkClass
        from products.netModel.org.webSiteClass import WebSiteClass
        from products.netModel.org.middlewareClass import MiddlewareClass
        #from products.netModel.org.vmhostClass import VmhostClass
        from products.netModel.org.location import Location
        orgTypes = [DeviceClass,NetworkClass,WebSiteClass, Location, MiddlewareClass]

        return orgTypes
        
    def loadOrgByUid(self, orgType, uid):
        orgTypes = self.__getOrgTypes()
        for _orgType in orgTypes:
            if orgType == _orgType.__name__:
                return _orgType._loadObj(uid)

        return None
    
    def getOrgRoot(self, orgType):
        orgTypes = self.__getOrgTypes()
        
        for _orgType in orgTypes:
            if orgType == _orgType.__name__:
                return _orgType.getRoot() 
                
        return None         
        
       

    def __getMonitorObjTypes(self):
        deviceCptTypes = Device.getSubComponentTypes()
        mwClss = MwBase.getSubMwClss()
        return [Device, Website, Network] + mwClss +deviceCptTypes

    
    
    def recursionGetOrgByUid(self, orgType, uid):
        currentOrg = self.loadOrgByUid(orgType, uid)
        if currentOrg:return [org._getRefInfo() for org in currentOrg.listAllNodes()]
        return []
        

 
    def findDevices(self, condition={}):
        "加载所有设备"
        dataObjs = []
        devices = []
        
        cursor = Device._getDbTable().find(condition)
        for obj in cursor: dataObjs.append(obj)
        
        for obj in dataObjs:
            dev = Device._loadObjFromMap(obj)
            devices.append(dev)
            
        return devices

    def findDevicesByCollectorId(self, cuid):
        """
        功能:通过收集器UID,加载相应的设备对象列表
        参数: type->string 收集器对象uid
        """
        collector = self.getCollector(cuid)
        if not collector: return []
        return collector.devices
    
    def findManageObjsByCollectorId(self,cuid):
        """
        功能:通过收集器UID,加载相应的管理对象列表
        参数: type->string 收集器对象uid
        """
        collector = self.getCollector(cuid)
        if not collector: return []
        return collector.getAllMonitorObjs()

    def getCollector(self, uid):
        """
        功能:通过uid获取对应的收集器对象
        参数: uid  type->string
        """
        collector = Collector._loadObj(uid)
        return collector
    
    def getCollectorHost(self, uid):
        """
        功能:通过uid获取对应的收集器对象host属性
        参数: uid  type->string
        """
        collector = Collector._loadObj(uid)
        if collector:
            return collector.host
        return None
    
    def saveCollector(self,uid,host):
        """
        保存ip变动后的收集器
        """
        collector = Collector._loadObj(uid)
        if  not collector: return
        collector.host = host

    def findDeviceByUid(self, uid):
        """
        功能:通过uid获取对应的设备对象
        参数: uid  type->string
        """
        return Device._loadObj(uid)
    
    def findWebsiteByUid(self, uid):
        """
        功能:通过uid获取对应的站点对象
        参数: uid  type->string
        """
        return Website._loadObj(uid)
    
    def findNetworkByUid(self, uid):
        """
        功能:通过uid获取对应的网络设备对象
        参数: uid  type->string
        """
        return Network._loadObj(uid)        

    def findNginxByUid(self, uid):
        return MwNginx._loadObj(uid)
    
    def findTomcatByUid(self, uid):
        return MwTomcat._loadObj(uid)
    
    def findApacheByUid(self, uid):
        return MwApache._loadObj(uid)
    
    def findIisByUid(self, uid):
        return MwIis._loadObj(uid)
    
    def findDeviceComponent(self, cType, uid):
        """
        检索出一个设备组件对象
        @param cType: <String>设备组件子类名
        @param uid:<String>组件ID 
        """
        componentTypes = Device.getSubComponentTypes()
        if not uid:
            print "Warning: param uid is empty."
            return None
        
        for cls in componentTypes:
            if cls.__name__ == cType: return cls._loadObj(uid)
        return None
    
    
    
    def findNetworkComponent(self, cType, uid):
        """
        检索出一个设备组件对象
        @param cType: <String>设备组件子类名
        @param uid:<String>组件ID 
        """
        componentTypes = Network.getSubComponentTypes()
        if not uid:
            print "Warning: param uid is empty."
            return None
        
        for cls in componentTypes:
            if cls.__name__ == cType: return cls._loadObj(uid)
        return None
    
    def sendEvent(self, eventInfo):
        
        if type(eventInfo) in types.StringTypes:
            eventInfo = pickle.loads(eventInfo)
            
        eventManager = xutils.getEventManager()
        eventManager.insertEvent(eventInfo)
        

    def getMonitorOjbTpl(self, mo, tplUid, is_pickle=False):
        if not mo: return None
        tpl = mo.getTemplate(tplUid)
        if is_pickle: tpl = pickle.dumps(tpl)
        return tpl
    
    
    def getMonitorObjByTypeAndUid(self, moUid, moType):
        "通过moType 及 moUid 获取监控对象"
        if not (moUid and moType):
            print "log: warning moUid or moType is not, return None."
            return None
        
        monitorTypes = self.__getMonitorObjTypes()
        for moCls in monitorTypes:
            if moCls.__name__ == moType : return moCls._loadObj(moUid)
            
        return None
    
    
    def addUserMoney(self, uid, money):
        "用户充值"
        pass
    
    
    def insertPerfData(self, timeId, value, dbName, tableName):
        db = getNetPerfDB(dbName)
        db[tableName].save({"_id":timeId, "value": value}, safe=False)


    def insertStrStatusData(self, dbName, tableName, recordId, timeId, value):
        """
        插入文本状态数据 
        @param value: 实时数据的Value,或处理后的结果
        @param rs: 文本处理后的结束（处理方式：比较、关键字查找 etc.） 
        """
        db = getNetPerfDB(dbName)
        db[tableName].save({"_id":recordId, "timeId": timeId, "value": value}, safe=False)
        
        
    def insertStatusData(self, statusValue, dbName, statusTableName):
        """
        插入状态数据
        """
        timeId = int(time.time())
        db = getNetPerfDB(dbName)
        db[statusTableName].save({"_id":timeId, "value": statusValue}, safe=False)
        
        
        