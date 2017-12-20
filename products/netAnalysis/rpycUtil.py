#coding=utf-8

import pickle
from products.rpcService.client import Client
from products.netUtils.settings import CollectorSettings
settings = CollectorSettings.getSettings()


rpcServiceClient = Client(hostName=settings.get('rpycConnection','rpcHost'), port=settings.getAsInt('rpycConnection', 'rpcPort')) #rpyc客户端

class RpycUtil(object):
    
    @classmethod
    def _dataRoot(cls):
        return rpcServiceClient.getServiceObj().getDataRoot()
    
    @classmethod
    def findDeviceByUid(cls, devUid):
        return cls._dataRoot().findDeviceByUid(devUid)
    
    @classmethod
    def findNetworkByUid(cls, netUid):
        return cls._dataRoot().findNetworkByUid(netUid)
    
    @classmethod
    def findNginxByUid(cls, middleUid):
        return cls._dataRoot().findNginxByUid(middleUid)
    @classmethod
    def findTomcatByUid(cls, middleUid):
        return cls._dataRoot().findTomcatByUid(middleUid)
    
    @classmethod
    def findApacheByUid(cls, middleUid):
        return cls._dataRoot().findApacheByUid(middleUid)
    @classmethod
    def findIisByUid(cls, middleUid):
        return cls._dataRoot().findIisByUid(middleUid)
    
    @classmethod
    def findWebsiteByUid(cls, websiteUid):
        return cls._dataRoot().findWebsiteByUid(websiteUid)
    
    @classmethod
    def findDeviceComponent(cls, cType, uid):
        return cls._dataRoot().findDeviceComponent(cType, uid)
    
    @classmethod
    def findNetworkComponent(cls, cType, uid):
        return cls._dataRoot().findNetworkComponent(cType, uid)
    
    @classmethod
    def getMonitorOjbTpl(cls, mo, tplUid):
        tpl = pickle.loads(cls._dataRoot().getMonitorOjbTpl(mo, tplUid, is_pickle=True))
        return tpl
    
    @classmethod
    def sendEvent(cls, eventInfo):
        _eventInfo = pickle.dumps(eventInfo)
        cls._dataRoot().sendEvent(_eventInfo)
        
    @classmethod
    def getMonitorObjByTypeAndUid(cls, moUid, moType):
        return cls._dataRoot().getMonitorObjByTypeAndUid(moUid, moType)
    
    
    @classmethod
    def insertPerfData(cls, timeId, value, dbName, tableName):
        cls._dataRoot().insertPerfData(timeId, value, dbName, tableName)


    @classmethod
    def insertStrStatusData(cls, dbName, tableName, recordId, timeId, value):
        cls._dataRoot().insertStrStatusData(dbName, tableName, recordId, timeId, value)
        
        
    @classmethod
    def insertStatusData(cls, statusValue, dbName, statusTableName):
        """
        插入状态数据
        """
        cls._dataRoot().insertStatusData(statusValue, dbName, statusTableName)
                