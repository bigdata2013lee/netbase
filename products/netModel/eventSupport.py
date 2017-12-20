#coding=utf-8
from products.netUtils import xutils

class EventSupport(object):
    
    def getEventSeveritySummary(self):
        """获取事件级别摘要"""
        evtMgr = xutils.getEventManager()
        _conditions = {"moUid":self.getUid(), "componentType": self.getComponentType()}
        return  evtMgr.getEventSeveritySummary(_conditions)
    
    def events(self, conditions={}, sortInfo={"endTime": -1}, skip=0, limit=None):
        """获取事件"""
        evtMgr = xutils.getEventManager()
        _conditions = {"moUid":self.getUid(), "componentType": self.getComponentType()}
        _conditions.update(conditions)
        return evtMgr.findCurrentEvents(conditions=_conditions, sortInfo=sortInfo, skip=skip, limit=limit)
    
    def historyEvents(self, conditions={}, sortInfo={}, skip=0, limit=None):
        """获取历史事件"""
        evtMgr = xutils.getEventManager()
        _conditions = {"moUid":self.getUid(), "componentType": self.getComponentType()}
        _conditions.update(conditions)
        return evtMgr.findHistoryEvents(conditions=_conditions, sortInfo=sortInfo, skip=skip, limit=limit)


class DeviceEventSupport(EventSupport):
    
    
    def getEventSeveritySummary(self):
        """获取事件级别摘要"""
        evtMgr = xutils.getEventManager()
        _conditions = {"$or":[{"device": self.getUid()},{"moUid":self.getUid(), "componentType": self.getComponentType()}]}
        return  evtMgr.getEventSeveritySummary(_conditions)
    
    def events(self, conditions={}, sortInfo={"endTime":-1}, skip=0, limit=None):
        """获取事件"""
        evtMgr = xutils.getEventManager()
        _conditions = {"$or":[{"device": self.getUid()},{"moUid":self.getUid(), "componentType": self.getComponentType()}]}
        _conditions.update(conditions)
        return evtMgr.findCurrentEvents(conditions=_conditions, sortInfo=sortInfo, skip=skip, limit=limit)
    
    def historyEvents(self, conditions={}, sortInfo={}, skip=0, limit=None):
        """获取历史事件"""
        evtMgr = xutils.getEventManager()
        _conditions = {"$or":[{"device": self.getUid()},{"moUid":self.getUid(), "componentType": self.getComponentType()}]}
        _conditions.update(conditions)
        return evtMgr.findHistoryEvents(conditions=_conditions, sortInfo=sortInfo, skip=skip, limit=limit)
    
    

class OrgEventSupport(object):
        
    def getEventSeveritySummary(self, moConditions={}):
        "获取事件摘要"
        
        objs = self.getAllMonitorObjs(conditions=moConditions)
        evtMgr = xutils.getEventManager()
        _conditions = {"moUid":{"$in":[mo.getUid() for mo in objs]}}
        return  evtMgr.getEventSeveritySummary(_conditions)
        
    def events(self, conditions={}, moConditions={}, sortInfo={"endTime":-1}, skip=0, limit=None):
        """获取事件"""
        objs = self.getAllMonitorObjs(conditions=moConditions)
        evtMgr = xutils.getEventManager()
        _conditions = {"moUid":{"$in":[mo.getUid() for mo in objs]}}
        _conditions.update(conditions)
        return evtMgr.findCurrentEvents(conditions=_conditions, sortInfo=sortInfo, skip=skip, limit=limit)
        
        
    def historyEvents(self, conditions={}, moConditions={}, sortInfo={}, skip=0, limit=None):
        """获取历史事件"""
        objs = self.getAllMonitorObjs(conditions=moConditions)
        evtMgr = xutils.getEventManager()
        _conditions = {"moUid":{"$in":[mo.getUid() for mo in objs]}}
        _conditions.update(conditions)
        return evtMgr.findHistoryEvents(conditions=_conditions, sortInfo=sortInfo, skip=skip, limit=limit)
    
    

class DeviceClsOrgEventSupport(object):
        
    def getEventSeveritySummary(self, moConditions={}):
        "获取事件摘要"
        
        objs = self.getAllMonitorObjs(conditions=moConditions)
        evtMgr = xutils.getEventManager()
        uids = [mo.getUid() for mo in objs]
        _conditions = {"$or":[{"device":{"$in":uids}}, {"moUid":{"$in":uids}}]}
        return  evtMgr.getEventSeveritySummary(_conditions)
        
    def events(self, conditions={}, moConditions={}, sortInfo={"endTime":-1},  skip=0, limit=None):
        """获取事件"""
        objs = self.getAllMonitorObjs(conditions=moConditions)
        evtMgr = xutils.getEventManager()
        uids = [mo.getUid() for mo in objs]
        _conditions = {"$or":[{"device":{"$in":uids}}, {"moUid":{"$in":uids}}]}
        _conditions.update(conditions)
        return evtMgr.findCurrentEvents(conditions=_conditions, sortInfo=sortInfo, skip=skip, limit=limit)
        
        
    def historyEvents(self, conditions={}, moConditions={}, sortInfo={}, skip=0, limit=None):
        """获取历史事件"""
        objs = self.getAllMonitorObjs(conditions=moConditions)
        evtMgr = xutils.getEventManager()
        uids = [mo.getUid() for mo in objs]
        _conditions = {"$or":[{"device":{"$in":uids}}, {"moUid":{"$in":uids}}]}
        _conditions.update(conditions)
        return evtMgr.findHistoryEvents(conditions=_conditions, sortInfo=sortInfo, skip=skip, limit=limit)
