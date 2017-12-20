#coding=utf-8
import time
from products.netUtils import jsonUtils
from products.netPublicModel.userControl import UserControl
from products.netWebAPI.base import BaseApi
from products.netModel.customerMap import CustomerMap
from products.netModel.org.location import Location
from products.netPublicModel.modelManager import ModelManager as MM
from products.netModel.devComponents.ipInterface import IpInterface
from products.netModel.device import Device
from products.netModel.network import Network

class CustomerMapApi(BaseApi):
    
    
    def listCustomerMaps(self):
        
        conditions = {}
        UserControl.addCtrlCondition(conditions)
        cms = CustomerMap._findObjects(conditions=conditions, sortInfo={"zIndex":-1})
        return jsonUtils.jsonDocList(cms)


    def removeCustomerMap(self, mcUid):
        mc = CustomerMap._loadObj(mcUid)
        if not  mc:
            return "warn:删除图失败"
        
        mc.remove()
        
        return "删除图成功"
            
    def createCustomerMap(self, title="", zIndex=0):
        conditions={}
        UserControl.addCtrlCondition(conditions)
        count = CustomerMap._countObjects(conditions=conditions)
        if count >= 20:
            return "warn:创建拓朴失败，不允许创建过多的拓朴图"
        
        user = UserControl.getUser()
        mc = CustomerMap()
        mc.ownCompany = user.ownCompany
        mc.title = title
        mc.zIndex = zIndex
        mc._saveObj()
        return "创建拓朴成功"
    
    def editCustomerMapProps(self, mcUid, title="", zIndex=0):
        mc = CustomerMap._loadObj(mcUid)
        mc.title = title
        mc.zIndex = zIndex
        mc._saveObj()
        return "编辑拓朴成功"
    
    def  map_getMapData(self, mcUid):
        mc = CustomerMap._loadObj(mcUid)
        if not mc: return {}
        
        mapData =  mc.mapData
        if not mapData:
            mc.mapData = {"bg":{"img":"default.png"},"size":{"w":1000,"h":600},"components":{},"connections":[]}
            
        return mc.mapData
    
    
    def map_savemapData(self, mcUid, mapData):
        mc = CustomerMap._loadObj(mcUid)
        if not mc: return "warn:保存失败"
        mc.mapData = mapData
        
    
    

        




    def map_listMos(self):
        conditions={}
        UserControl.addCtrlCondition(conditions)
        mos1 = Device._findObjects(conditions)
        mos2 = Network._findObjects(conditions)
        igs=["objThresholds","snmpConfig","ipmiConfig","wmiConfig","commConfig","templates", "ownCompany"]
        def updict(doc):
            return {"title": doc.titleOrUid(), "status": doc.getStatus(),
                    "moType":doc.__class__.__name__
                    }
        rs = jsonUtils.jsonDocList(mos1+mos2, updict=updict, ignoreProperyties=igs)
        return rs


    def map_listIfaces(self, moUid, moType):
        rs = []
        dr = MM.getMod('dataRoot')
        mo = dr.getMonitorObjByTypeAndUid(moUid, moType)
        if not mo: return rs
        igs = ["objThresholds","templates","ownCompany"]
        ifaces = mo.interfaces
        def updict(iface):
            return {}
        
        rs = jsonUtils.jsonDocList(ifaces, updict=updict, ignoreProperyties=igs)
        
        return rs
    
    
    def map_getDevsMainInfo(self, mos=[]):
        dr = MM.getMod('dataRoot')
        for _mo in mos:
            mo = dr.getMonitorObjByTypeAndUid(_mo.get("moUid"), _mo.get("moType"))
            if not mo:
                _mo["status"] = "unknown"
            else:    
                _mo["status"] = mo.getStatus()
                if _mo["status"] == "up":
                    ess = mo.getEventSeveritySummary()
                    if max(ess[3:]) > 0:
                        _mo["status"] = "warning"
                    
        return mos
    
    
    def map_getIfacesMainInfo(self, mos=[]):
        for _mo in mos:
            mo = IpInterface._loadObj(_mo.get("moUid"))
            if not mo:
                _mo["status"] = "unknown"
                _mo["throughRates"]={"inputRate":None, "outputRate":None}
            else:    
                _mo["status"] = mo.getStatus()
                _mo["getThroughValues"] = mo.getThroughValues()
                _mo["throughRates"] = mo.getThroughRates()
            
        return mos
        
        
