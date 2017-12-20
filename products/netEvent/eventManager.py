#coding=utf-8

import time
from products.netEvent.event import Event
from products.netUtils import xutils 
from products.netModel.devComponents.base import DeviceComponent
from products.netModel.device import Device

class EventManager(object):
    

    def currentEvent2Histroy(self, currentEvent):
        """
        当前事件转换为历史事件
        @param currentEvt: 
        """
        if not currentEvent:return
        
        currentEvent.historical = True
        return currentEvent
    
    def __setEventObjProperties(self, event, eventInfo, fg="merge"):
        """
        设置事件对象的属性或记录内容
        分三种情况：合并(fg=merge)、新事件(fg=new)、clear事件(fg=clear)
        """
        notAllowUpdateKeys = {
            "merge": ["_id", "evtKey", "evtKeyId", "clearId", "count", "firstTime", "endTime", "agent"],
            "new": ["_id", "count", "firstTime", "endTime"],
            "clear": ["_id", "count", "firstTime", "endTime"]
        }
        
        event.endTime = time.time()
        
        for key, value in eventInfo.items():
            if key in notAllowUpdateKeys[fg]: continue
            event._medata[key] = value
        
        event.endTime = time.time()
        if fg == "merge":
            event.count += 1
            
        if fg == "new":
            event.firstTime = time.time() - 1
            
        if fg == "clear":
            event.firstTime = time.time() - 1
                

    def __setEvtObjLabel(self, mo, eventInfo):
        if isinstance(mo, DeviceComponent) and mo.device: 
            eventInfo["label"] = mo.device.getManageId()
            return
        
        eventInfo["label"] = (hasattr(mo, "getManageId") and mo.getManageId()) or mo.titleOrUid()
        
    def __setEvtObjAvdProperties(self, eventInfo):
        """
        @note: 
        todo:可在此判断moUid是什么对象，如果是DeviceComponent子类，就是设备的组件，可在事件中加入设备相关的信息
        """
        from products.netPublicModel.modelManager import ModelManager as MM
        
        dr = MM.getMod("dataRoot")
        moUid = eventInfo.get("moUid", None)
        componentType = eventInfo.get("componentType", None)
        if not (moUid and  componentType): return
        mo = dr.getMonitorObjByTypeAndUid(moUid, componentType)
        if not mo: return
        self.__setEvtObjLabel(mo, eventInfo)
        
        company = mo.ownCompany
        if company: eventInfo["companyUid"] = company.getUid()
        if isinstance(mo, DeviceComponent) and mo.device: 
            eventInfo["device"] = mo.device.getUid()
            eventInfo["deviceIp"] = mo.device.manageIp
        
        if isinstance(mo, Device):
            eventInfo["deviceIp"] = mo.manageIp
            
        if not  eventInfo.get("collector", None):
            eventInfo["collector"] = hasattr(mo, "collector") and mo.collector and mo.collector.getUid()
        
        
        
    def insertEvent(self, eventInfo):
        """
        向事件库中插入一条事件
        @note: 
            1.如果是'恢复'事件，则把相应匹配当前事件转为历史事件
            2.如果是普通事件（非恢复事件），则合并原事件信息，并累加发生次数
            2.1 如果是新事件，则直接创建一条新的事件记录
        """
        self.__setEvtObjAvdProperties(eventInfo)
        
        evtKeyId = eventInfo.get("evtKeyId", None) or xutils.mkMd5(eventInfo.get("evtKey"))
        clearId = eventInfo.get("clearId", None) or xutils.mkMd5(eventInfo.get("clearKey"))
        eventInfo["evtKeyId"] = evtKeyId
        eventInfo["clearId"] = clearId
        if eventInfo.get("severity", None) == xutils.severitys["clear"]:  #clear 事件
            events = Event._findObjects({"clearId":clearId, "historical":False})
            for evt in events:
                self.currentEvent2Histroy(evt)
                
            
        else: #普通事件
            events = Event._findObjects({"evtKeyId":evtKeyId, "historical":False})
            findEvent  = Event() 
            if events: #匹配到已有事件
                findEvent = events[0] 
                self.__setEventObjProperties(findEvent, eventInfo, fg="merge")
            else: #新事件
                self.__setEventObjProperties(findEvent, eventInfo, fg="new")
                
            
            findEvent._saveObj()
            
 
    def findEvents(self, conditions={}, sortInfo={}, skip=0, limit=None):
        """
                查询事件
        @param conditions: 条件
        @param sortInfo: 排序方式
        @param skip: 跳过多少条
        @param limit: 获取多少条
        """
        return Event._findObjects(conditions=conditions, sortInfo=sortInfo, skip=skip, limit=limit)
    
    def findCurrentEvents(self, conditions={}, sortInfo={}, skip=0, limit=None):
        """
            查询当前事件
            @param conditions: 条件
            @param sortInfo: 排序方式
            @param skip: 跳过多少条
            @param limit: 获取多少条
        """
        conditions.update({"historical":False})
        return Event._findObjects(conditions=conditions, sortInfo=sortInfo, skip=skip, limit=limit)
    
    def findHistoryEvents(self, conditions={}, sortInfo={}, skip=0, limit=None):
        """
            查询历史事件
            @param conditions: 条件
            @param sortInfo: 排序方式
            @param skip: 跳过多少条
            @param limit: 获取多少条
        """
        conditions.update({"historical":True})
        return Event._findObjects(conditions=conditions, sortInfo=sortInfo, skip=skip, limit=limit)
    
    
    def getEventSeveritySummary(self, conditions):
        """
            获取事件摘要
            @param conditions: conditions->dict 事件的条件
            @return: result 级别0-5的事件个数
        """
        events = self.findCurrentEvents(conditions=conditions)
        result = [0,0,0,0,0,0]
        for evt in events:
            severity = int(evt.severity)
            result[severity]+=1
        
        return  result
     
     
     

    def confirmEvents(self, eventIds=[]):
        """
        确认一条或多条事件
        确认后的事件，被转为历史事件
        """
        conditions={'_id': {"$in":[xutils.fixObjectId(uid) for uid in eventIds]}}
        evts = self.findCurrentEvents(conditions=conditions)
        for evt in evts: self.currentEvent2Histroy(evt)
        return "ok"

        
        
        
