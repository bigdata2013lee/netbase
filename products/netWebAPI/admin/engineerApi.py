#coding=utf-8
from products.netWebAPI.base import BaseApi
from products.netModel.user.engineerUser import EngineerUser
from products.netUtils import jsonUtils
from products.netModel.user.user import User 
import time
import types
import re
from products.netPublicModel.userControl import UserControl
from products.netPublicModel.modelManager import ModelManager as MM
from products.netEvent.event import Event
from products.netModel.idcProvider import IdcProvider
from products.netModel.ticket.serviceNote import ServiceNote

class EngineerApi(BaseApi):
    
    def delNote(self, note):
        sn = ServiceNote._loadObj(note["_id"])
        if not sn: return "fail"
        sn.remove()
        return "成功删除服务单"
    
    def addNote(self, note, enguid):
        sn = ServiceNote()
        sn.title = note["title"]
        user = User._loadObj(note["user"])
        eng = EngineerUser._loadObj(enguid)
        sn.engineer = eng
        sn.startTime = time.time()
        if not user: return "fail"
        sn.user = user
        sn._saveObj()
        return "成功添加服务单"
        
    
    def auditNote(self, note):
        sn = ServiceNote._loadObj(note["_id"])
        if not sn : return "fail"
        sn.summary = note["summary"]
        sn.procedure = note["procedure"]
        sn.title = note["title"]
        sn.status = 1
        return "成功提交服务单审核"
    
    def  editNote(self, note):
        sn = ServiceNote._loadObj(note["_id"])
        if not sn : return "fail"
        sn.summary = note["summary"]
        sn.procedure = note["procedure"]
        sn.title = note["title"]
        return "保存成功"
    
    def getCustomers(self, uid):
        
        eng = EngineerUser._loadObj(uid)
        if not eng: return []
        def updict(obj):
            company = obj.ownCompany
            return {"ownCompany": company and company.titleOrUid()}
        
        return jsonUtils.jsonDocList(eng.users, updict = updict, ignoreProperyties=["password", "last_login"])

    
    
    def getServiceNotes(self, engUid,  pageData, conditions={}):
        _pageData = pageData or {"skip":0}
        eng = EngineerUser._loadObj(engUid)
        if not eng: return {"total":0, "results":[]}
        
        for name, val in conditions.items():
            if type(val) in types.StringTypes and val.find("regex:") == 0:
                val = val.replace("regex:", "")
                conditions[name] = re.compile(val)
                
        def updict(obj):
            user = obj.user
            return {"user": user and user.titleOrUid()}
        
        conditions.update({"engineer": eng._getRefInfo()})
        notes = ServiceNote._findObjects(conditions=conditions, skip=_pageData["skip"], limit=_pageData['limit'], sortInfo=_pageData["sort"])
        count = ServiceNote._getDbTable().find(conditions).count()
        ret = {"total":count, "results":jsonUtils.jsonDocList(notes, updict=updict)}
        return ret
    
    
    def getCustomerIssues(self, customerUid):
        conditions = {}
        customer = User._loadObj(customerUid)
        company = customer and customer.ownCompany 
        if not company: return []
        
        conditions.update({"companyUid":company.getUid(),"severity":{"$gte":3}})
        evtMgr = MM.getMod("eventManager")
        events = evtMgr.findCurrentEvents(conditions=conditions,sortInfo={"endTime": -1} , limit=100)
        def updict(obj):
            return dict(
                serviceNoteUid=obj._medata.get("serviceNoteUid", None)
            )
        return jsonUtils.jsonDocList(events, updict=updict)
    
    
    
    def createServiceNote(self, serviceNote, customerUid):
        customer = User._loadObj(customerUid)
        eng = UserControl.getUser()
        eventId = serviceNote.get("eventId","")
        if not eventId: return "fail"
        if not customer: return "fail"
        
        sn = ServiceNote()
        sn.__extMedata__(serviceNote)
        
        sn.user = customer
        sn.engineer = eng
        sn.startTime = int(time.time());
        sn._saveObj()
        
        evt = Event._loadObj(eventId)
        if evt: 
            evt._medata["serviceNoteUid"] = sn.getUid()
            evt._saveObj()
            
        return "成功创建服务单"
        
    def getEngineers(self, idcProviderId):
        provider = IdcProvider._loadObj(idcProviderId)
        if not  provider: return []
        
        engs = provider._getRefMeObjects("idcProvider", EngineerUser)
        return jsonUtils.jsonDocList(engs, ignoreProperyties=["password", "last_login"])
    
    
        
        
        
        