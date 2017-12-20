#coding=utf-8
from products.netWebAPI.base import BaseApi
from products.netUtils import jsonUtils
from products.netUtils import xutils
from products.netEvent.event import Event
import re
import types
from products.netPublicModel.userControl import UserControl
import time
from products.netModel.collector import Collector
import md5


ignoreProperyties1=['companyUid','collector',"evtKeyId","clearId","evtKey","clearKey"]
ignoreProperyties2=['companyUid','collector','serviceNoteUid',"evtKeyId","clearId","evtKey","clearKey"]

def getSeverity(value):
    for k, v in xutils.severitys.items():
        if v == value:
            return k
    return ""
     
class EventApi(BaseApi):
    
    def searchHistoryEvents(self, pageData, conditions={}):
        _pageData = pageData or {"skip":0}
        
        user = UserControl.getUser()
        company = None
        if user: company = user.ownCompany
        conditions["companyUid"] = company and company.getUid()
        
        for name, val in conditions.items():
            if type(val) in types.StringTypes and val.find("regex:") == 0:
                val = val.replace("regex:", "")
                conditions[name] = re.compile(val)
            if name == "componentType":
                ctypes = conditions[name].replace(" ", "").split(",")
                conditions[name]={"$in":ctypes}

        evtMgr = xutils.getEventManager()
        events = evtMgr.findHistoryEvents(conditions=conditions, skip=_pageData["skip"], limit=_pageData['limit'], sortInfo=_pageData["sort"])
        count = Event._getDbTable().find(conditions).count()
        ret = {"total":count, "results":jsonUtils.jsonDocList(events)}
        return ret

    def searchEvents(self, pageData, conditions={}):
        
        _pageData = pageData or {"skip": 0}
        user = UserControl.getUser()
        company = None
        if user: company = user.ownCompany
        conditions["companyUid"] = company and company.getUid()
        
        for name, val in conditions.items():
            if type(val) in types.StringTypes and val.find("regex:") == 0:
                val = val.replace("regex:", "")
                conditions[name] = re.compile(val)
            if name == "componentType":
                ctypes = conditions[name].replace(" ", "").split(",")
                conditions[name]={"$in":ctypes}
        
        evtMgr = xutils.getEventManager()
        events = evtMgr.findEvents(conditions=conditions, skip=_pageData["skip"], limit=_pageData['limit'], sortInfo=_pageData["sort"])
        count = Event._getDbTable().find(conditions).count()
        ret = {"total":count, "results":jsonUtils.jsonDocList(events,ignoreProperyties=ignoreProperyties1)}
        return ret

    def getEventSeveritySummarys(self):
        """
        所有主监控对象的事件摘要
        """
        monitorClss = Collector.getMainMonitorClss()
        conditions = {}
        rs=[]
        
        UserControl.addCtrlCondition(conditions)
        for mCls in monitorClss:
            mos = mCls._findObjects(conditions=conditions)
            for mo in mos:
                ess = mo.getEventSeveritySummary()
                if sum(ess[2:]) == 0: continue # >=info级别求和为0，忽略
                _r = {"uid": mo.getUid(),"title":mo.titleOrUid(), "componentType":mo.getComponentType(),"ess":ess}
                rs.append(_r)
                
        return rs
    
    
    def listMoEvents(self, uid, componentType):
        """
        主监控对象新最事件列表
        """
        mo=None
        evts = []
        monitorClss = Collector.getMainMonitorClss()
        for mCls in monitorClss:
            if mCls.getComponentType() == componentType:
                mo = mCls._loadObj(uid)
        
        if mo: evts = mo.events()
        
        return jsonUtils.jsonDocList(evts,ignoreProperyties=ignoreProperyties2)
        
    def getLast5MinEventsNotification(self):
        "列出最近5分钟事件,用于APP通知"
        rs = {"label":"", "message":"", "count":0, "idsmark":""}
        evtMgr = xutils.getEventManager()
        conditions={}
        user = UserControl.getUser()
        company = None
        if user: company = user.ownCompany
        
        conditions["companyUid"] = company and company.getUid()
        conditions["endTime"] = {"$gte":int(time.time()-300)}
        
        events = evtMgr.findCurrentEvents(conditions=conditions)
        
        evtUids = [evt.getUid() for  evt in events]
        rs["idsmark"] = md5.new("".join(evtUids)).hexdigest().upper()
        
        if  len(events) == 1:
            rs["label"] = events[0].label
            rs["message"] = events[0].message
            rs["count"] = 1
            
        elif len(events) > 1:
            count = len(events) 
            rs["label"] = "Netbase事件通知"
            rs["message"] = "近5分钟，您的监控项目产生了%s条事件" %count
            rs["count"] = count
            
        return rs
        
    def confirmEvents(self, eventIds=[]):
        evtMgr = xutils.getEventManager()
        fg = evtMgr.confirmEvents(eventIds=eventIds)
        return fg
    
    