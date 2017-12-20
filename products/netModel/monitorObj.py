#coding=utf-8
import types
from copy import deepcopy
from products.netModel.baseModel import RefDocObject, BaseComponentModel
from products.netPerData import manager as perDataManager
from products.netModel.templates.template import Template
from products.netModel import medata
from products.netModel.eventSupport import EventSupport
from products.netUtils.cycleSettings import cycleTimes
from products.netUtils import xutils


class MonitorObj(EventSupport, BaseComponentModel):
    
    def __init__(self):
        BaseComponentModel.__init__(self)
        self.__extMedata__(dict(
            templates = [], #模板
            objThresholds = {}
        ))
     
    
    monitored = medata.plain("monitored", True) #是否监控
    intervalMinute =  medata.plain("intervalMinute", 5), #监控间隔时间
    tryCount =  medata.plain("tryCount", 0), #重试次数
    #objThresholds = medata.Dictproperty("objThresholds",{})
    
    @property
    def objThresholds(self):
        tplThresholds = self.getTplThresholds()
        objthreshes=deepcopy(self._medata["objThresholds"])
        for key in objthreshes:
            if key not in tplThresholds:
                del self._medata["objThresholds"][key]
        for key in tplThresholds:
            if key not in self._medata["objThresholds"]:
                self._medata["objThresholds"][key]=tplThresholds[key]
                
        self._saveProperty2("objThresholds", self._medata.get("objThresholds",{}))  
        
        return self._medata["objThresholds"]
    
    @objThresholds.setter
    def objThresholds(self, thresholds):
        if not thresholds: thresholds = {}
        self._saveProperty2("objThresholds", thresholds)

    
    @property
    def templates(self):
        """
            获取所有模板对象
        """
        templates = RefDocObject.instRefList(self._medata["templates"])
        return templates
    
    def getTemplate(self, tplUid):
        """
        获取监控对象绑定的某一个模板
        @param tplUid: 模板标识名
        @return: <Template>模板
        """
        if not tplUid: return None
        tpl = Template(tplUid)
        if tpl._getRefInfo() not in self._medata["templates"]: return None
        
        return Template._loadObj(tplUid)
            
        
    def bindTemplate(self, tpl):
        """
            添加/绑定一个模板
            @param tpl: type->Template
        """
        if not tpl: return self
        if tpl._getRefInfo in self._medata['templates']: return self
        self._medata['templates'].append(tpl._getRefInfo())
        self._saveProperty2('templates', list(set(self._medata['templates'])))
        return self

    
    def unbindTemplate(self, tpl):
        """
            删除/解绑一个模板
            @param tpl: type->string|Template
        """
        if not tpl: return self
        if type(tpl) in types.StringTypes:
            tplName = tpl 
            tpl = self.getTemplate(tplName)
            if not tpl: return self
        
        tplRefInfo = tpl._getRefInfo() 
        if tplRefInfo in self._medata['templates']: self._medata['templates'].remove(tplRefInfo)
        self._saveProperty('templates')    
        return self
    
    def getAllTemplates(self):
        "得到所有的模板"
        return self.templates
    
        
    def getBaseTemplate(self):
        """
        获取基础模板
        """
        for tpl in self.templates:
            if tpl and tpl.isBaseTpl:return tpl
        return None
    
    def _getEventStatusValue(self, NoneVal=-1):
        """
        获取状态事件值
        @note: 容差时间 默认3周期时间 具体配置在products/netUtils/cycleSettings.py
        """
        dbName = self._getPerfDbName()
        tableName = self._getStatusTableName()
        timeRange = cycleTimes.get(self.getComponentType(), 180) * 3; #默认3周期时间 
        return perDataManager.getEventStatusValue(dbName, tableName, timeRange=timeRange, NoneVal=NoneVal)
    
    def getStatus(self):
        val = self._getEventStatusValue()
        status = {1:"up", 0: "down"}
        return status.get(val, "unknown")
    
    
    def _getPerfDbName(self):
        """
        生成监控对象的性能数据库名
        格式为ComponentType_0~9
        @note: 对象的UID须为16进制的
        """
        uid = self.getUid()
        return xutils.fixPerfDbName(uid, self.getComponentType())
    
    def _getPerfTablName(self, tplName, dsName, dpName, cptUid=""):
        """
        生成监控对象的性能表名
        @param cptUid: 收集点的UID 
        @note: 只针对有收集点的对象，需要传递此参数 
        """
        uid = self.getUid()
        tableName = "|".join([tplName, dsName, dpName])
        if cptUid: tableName += "|cpt_%s" %cptUid
        return "%s:%s" %(uid, tableName)
    
    def _getStatusTableName(self, cptUid=""):
        """
        获取收集器中的事件状态表名
        """
        tableName = "%s:status" %self.getUid()
        if cptUid: tableName += "|cpt_%s" %cptUid
        return tableName
    
    def getPerfValue(self, tplName, dsName, dpName, cptUid=""):
        """
        获取性能数据
        @param tplName: tplName
        @param dsName: dsName
        @param dpName: dpName
        """
        dbName = self._getPerfDbName()
        tableName = self._getPerfTablName(tplName, dsName, dpName, cptUid=cptUid)
        return perDataManager.getPerfValue(dbName, tableName)
    
    def getPerfValues(self, tplName, dsName, dpName, sTime, eTime=None, cptUid=""):
        """
        获取一段时间范围性能数据
        @param tplName: tplName
        @param dsName: dsName
        @param dpName: dpName
        """
        dbName = self._getPerfDbName()
        tableName = self._getPerfTablName(tplName, dsName, dpName, cptUid=cptUid)
        return perDataManager.getPerfValues(dbName, tableName, sTime, eTime=eTime)
    
    def getStatusValue(self, tplName, dsName, dpName, cptUid=""):
        """
        获取状态数据
        @param tplName: tplName
        @param dsName: dsName
        @param dpName: dpNam
        """
        dbName = self._getPerfDbName()
        tableName = "%s:string_status_datas" %self.getUid()
        recordId = "|".join([tplName, dsName, dpName])
        if cptUid: recordId += "|cpt_%s" %cptUid
        return perDataManager.getStatusValue(dbName, tableName, recordId)
        
        

    def remove(self):
        BaseComponentModel.remove(self)
        from products.netPublicModel.modelManager import ModelManager as MM
        dr = MM.getMod('dataRoot')
        dr.fireEvent("removeMonitorObj", obj=self)
    
    def getTplThresholds(self):
        tplThresholds = {}
        templates = self.getAllTemplates()
        for tpl in templates:
            tplThresholds.update(tpl.thresholds)
        return tplThresholds
    @classmethod
    def getMonitorObjByUid(cls,uid):
        """
                功能:通过uid获取监控对象
                参数:监控对象uid
        """
        return cls._loadObj(uid)
        
