# -*- coding: utf-8 -*-
from django.http import HttpResponse
from products.netModel.templates.template import  Template
from products.netModel.templates.ds import SnmpDataSource, WmiDataSource, CmdDataSource
from products.netWebAPI.base import BaseApi

def getDataSources(tpl):
    if not tpl.dataSources:return []
    dataSources = []
    for dsName, ds in  tpl.dataSources.items():
        dsTmp = ds._toDict()
        dsType = ds.getType()
        otherStr = []
        if dsType == "SnmpDataSource":
            pass
        elif dsType == "CmdDataSource":
            otherStr.append(u"命令=%s" % ds.cmd)
            otherStr.append(u"执行方式=%s" % ds.execType)
            otherStr.append(u"执行周期=%s" % ds.execCycle)
        elif dsType == "WmiDataSource":
            otherStr.append(u"命令=%s" % ds.cmd)
            otherStr.append(u"命名空间=%s" % ds.nameSpace)
            otherStr.append(u"源类型=%s" % ds.sourceType)
            otherStr.append(u"执行周期=%s" % ds.execCycle)
        dsTmp["other"] = u";".join(otherStr)
        
        dataSources.append(dsTmp)
    return dataSources

class ManagerApi(BaseApi):
        
    
    def saveTemplates(self, tplUid, title, description):
        u"""
            保存模板
        """
        tpl = Template._loadObj(tplUid)
        find = tpl is not None
        if not find:
            tpl = Template(tplUid)
            tpl._saveObj()
            
        tpl.title = title
        tpl.description = description
        return tpl.getUid()
    
    
    def searchTemplates(self):
        datasource = {'results':[]}
        for tpl in Template._findObjects():
            tempDict = {
               "id":tpl.getUid(),
               "title":tpl.titleOrUid(),
               "description":tpl.description,
            }
            datasource['results'].append(tempDict)
    
        return datasource
    
    
    def ajaxGetDataSources(self, tplUid):   
        u"""获取数据源"""
        tpl = Template._loadObj(tplUid)
        dataSources = getDataSources(tpl)
        return {"results":dataSources}
    
    
    def ajaxGetDataPoints(self, tplUid, dsName):
        u"""
        通过数据源得到数据点
        """
        result = {"results":[]}
        tpl = Template._loadObj(tplUid)
        ds = tpl.getDataSource(dsName)
        
        if ds:
            result["results"] = ds.dataPoints.values()
        return result
    
    
    def ajaxGetThresholds(self, tplUid, dsName, dpName):
        u"""
        通过数据点得到阀值
        """
        result = {"results":[]}
        tpl = Template._loadObj(tplUid)
        ds = tpl.getDataSource(dsName)
    
        if ds:
            dataPoint = ds.dataPoints.get(dpName, {})
            if dataPoint:
                thresholds = dataPoint.get("thresholds", [])
                for thName, th in thresholds.items():
                    otherStr = []
                    if th.get("min", ""):otherStr.append(u"最小值:%s" % th.get("min"))
                    if th.get("max", ""):otherStr.append(u"最大值:%s" % th.get("max"))
                    if th.get('type') == 'StatusThreshold' and  th.get("statusExp", ""):otherStr.append(u"状态表达式:%s" % th.get("statusExp"))
                    th["other"] = u";".join(otherStr)
    
                    result["results"].append(th)
    
        return result
    
    
    def saveDataSource(self, tplUid, ds):
        dsName = ds.get('uname')
        tpl = Template._loadObj(tplUid)
        dsObj = tpl.getDataSource(dsName)
        if not dsObj:
            if ds.get("__type") == "SnmpDataSource":
                dsObj = SnmpDataSource(dsName)
            elif ds.get("__type") == "CmdDataSource":
                dsObj = CmdDataSource(dsName)
            elif ds.get("__type") == "WmiDataSource":
                dsObj = WmiDataSource(dsName)
                
        dsObj.monitored = ds.get("monitored", False)
        dsObj.uname = dsName
        
        if dsObj.getType() == "SnmpDataSource":
            pass
            
        if dsObj.getType() == "CmdDataSource":
            dsObj.cmd = ds.get("cmd", "")
            dsObj.execType = ds.get("execType", "ssh")
            dsObj.execCycle = ds.get("execCycle", 300)
        
        if dsObj.getType() == "WmiDataSource":
            dsObj.cmd = ds.get("cmd", "")
            dsObj.nameSpace = ds.get("nameSpace", "")
            dsObj.sourceType = ds.get("sourceType", "WMI")
            dsObj.execCycle = ds.get("execCycle", 300)
            
    
        tpl.addDataSource(dsObj)
        return "Save dataSource success!"
    
    
    def deleteDataSource(self, tplUid, ds):
        tpl = Template._loadObj(tplUid)
        tpl.deleteDataSource(ds.get("uname"))
        return "Delete dataSource success!"

    
    def saveDataPoint(self, tplUid, dsName, dp):
        tpl = Template._loadObj(tplUid)
        ds = tpl.dataSources[dsName]
        if not ds: return HttpResponse("not ok")
        dpObj = {
              "uname":dp.get("uname"),
              "type":dp.get("type"),
              
        }
        if ds.getType() == "SnmpDataSource":
            dpObj.update({"oid":dp.get("oid")})
        
        tpl.addDataPoint(dsName, dpObj)
        return "OK"

    
    def deleteDataPoint(self, tplUid, dsName, dpName):
        tpl = Template._loadObj(tplUid)
        tpl.deleteDataPoint(dsName, dpName)
        return "OK"
    
    
    def saveThreshold(self, tplUid, dsName, dpName, threshold):
        tpl = Template._loadObj(tplUid)
        tpl.addDataPointThreshold(dsName, dpName, threshold)
        return "OK"
     
    
    def deleteThreshold(self, tplUid, dsName, dpName, thresholdName):
        tpl = Template._loadObj(tplUid)
        tpl.deleteDataPointThreshold(dsName, dpName, thresholdName)
        return "OK"
         
    
    def deleteTemplate(self, tplUid):
        tpl = Template._loadObj(tplUid)
        tpl.remove()
        return "OK"

