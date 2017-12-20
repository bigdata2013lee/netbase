#coding=utf-8
from products.netUtils import jsonUtils
from products.netPublicModel.userControl import UserControl
from products.netWebAPI.base import BaseApi, apiAccessSettings
from products.netModel.org.location import Location
from products.netPublicModel.modelManager import ModelManager as MM


class LocationApi(BaseApi):
    
    def listMos(self, orgUid, conditions={}):
        
        
        org = Location._loadObj(orgUid)
        rs = org.getCurMonitorObjs(conditions=conditions)
        igs=["objThresholds","snmpConfig","ipmiConfig","wmiConfig","commConfig","templates"]
        def updict(doc):
            return {"title": doc.titleOrUid(), "cpu": doc.getCpu(), "mem": doc.getMem(), "status": doc.getStatus(),
                    "moType":doc.__class__.__name__
                    }
        rs = jsonUtils.jsonDocList(rs, updict=updict, ignoreProperyties=igs)
        return rs
        
    @apiAccessSettings("add")
    def addLoc(self, title):
        user = UserControl.getUser()
        loc = Location()
        loc.title = title
        loc.ownCompany = user.ownCompany
        loc._saveObj()
        
        return "添加分组成功"
        
    @apiAccessSettings("del")
    def delLoc(self, uid):
        
        loc = Location._loadObj(uid)
        
        if not loc:
            return "warn:删除分组失败"
        
        defLoc = Location.getDefault()
        if loc == defLoc:
            return "warn:不能删除默认分组"
        
        mos = loc.getCurMonitorObjs()
        for mo in mos:
            mo.location = defLoc
        loc.remove()
        
        return "删除分组成功"
    
    
    @apiAccessSettings("edit")
    def renameLoc(self, locUid, title):
        loc = Location._loadObj(locUid)
        if not loc:
            return "warn:重命名分组失败"
        
        loc.title=title
        return "重命名分组成功"
    
    
    @apiAccessSettings("edit")
    def setLocation(self, orgUid, mos):
        loc = Location._loadObj(orgUid)
        if not loc:
            return "warn:设置分组失败"
        
        dr = MM.getMod('dataRoot')
        for _mo in mos:
            mo = dr.getMonitorObjByTypeAndUid(_mo["uid"], _mo["moType"])
            if not mo: continue
            mo.location = loc
            
        return "设置分组成功"
            
        
    def listAllNodes(self):

        conditions={}
        UserControl.addCtrlCondition(conditions)
        locs = Location._findObjects(conditions)
        igs = ["ownCompany"]
        def updict(node):
            return {}
        
        rs =  jsonUtils.jsonDocList(locs, updict=updict, ignoreProperyties=igs)
        
        return rs
       
#----------------------------------------------------------------------------------



        
        
        
        