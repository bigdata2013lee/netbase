#coding=utf-8
from products.netUtils import jsonUtils
from products.netWebAPI.base import BaseApi, apiAccessSettings
from products.netModel.device import Device
from products.netModel.website import Website
from products.netModel.templates.template import Template
from products.netPublicModel.modelManager import ModelManager
from products.netModel.network import Network


def _getMoType(cType):

    from products.netModel.middleware.mwBase import MwBase
    moTypes = [Device, Website, Network] + MwBase.getSubMwClss() + Device.getSubComponentTypes()
    for  cls in moTypes:
        if cls.__name__ == cType: return cls
    return None
    
class ThresholdApi(BaseApi):
    
    def  getMoThresholds(self, uid, cType):
        cls = _getMoType(cType)
        if not cls: return {}
        mo = cls._loadObj(uid)
        if not mo: return {}
        
        ths = mo.objThresholds
        return ths
        
    @apiAccessSettings("edit")
    def setMoThresholds(self, uid, cType, thresholds):
        cls = _getMoType(cType)
        if not cls: return "warn:保存失败"
        mo = cls._loadObj(uid)
        if not mo: return "warn:保存失败"
        
        ths = mo.objThresholds
        
        for key, val in thresholds.items():
            ths.get(key, {}).update(val)
            
        mo.objThresholds = ths
        return "保存成功"
        
        
    def getMoTemplates(self, moUid, moType="Device"):
        dr = ModelManager.getMod("dataRoot")
        mo = dr.getMonitorObjByTypeAndUid(moUid, moType)
        if not mo:return []
        
        tpls = mo.templates
        return jsonUtils.jsonDocList(tpls)
        
        
    def getExtendTemplates(self):
        conditions={"tplType":"extend"}
        tpls = Template._findObjects(conditions=conditions)
        return jsonUtils.jsonDocList(tpls)
    
    @apiAccessSettings("edit")
    def bindTpl(self, moUid, moType, tplUid):
        dr = ModelManager.getMod("dataRoot")
        mo = dr.getMonitorObjByTypeAndUid(moUid, moType)
        
        if not mo: return "warn:绑定模板失败,监控对象不存在"
        tpl = Template._loadObj(tplUid)
        if not tpl: return "warn:绑定模板失败,模板不存在"
        mo.bindTemplate(tpl)
        
        return "绑定模板成功"
    
    
    @apiAccessSettings("edit")
    def unbindTpl(self, moUid, moType, tplUid):
        dr = ModelManager.getMod("dataRoot")
        mo = dr.getMonitorObjByTypeAndUid(moUid, moType)
        
        if not mo: return "warn:取消绑定模板失败,监控对象不存在"
        tpl = Template._loadObj(tplUid)
        if not tpl: return "warn:取消绑定模板失败,模板不存在"
        if tpl.tplType=="base": return "warn:不能解绑基础模板"
        mo.unbindTemplate(tpl)
        
        return "取消绑定模板成功"
                