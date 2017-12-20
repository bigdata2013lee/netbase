#coding=utf-8

import time
from products.netModel import  mongodbManager as dbManager
from products.netUtils.mcClient import getPerfValueCacheDecorator, getEventStatusValueCacheDecorator
from products import sysStaticConf



@getPerfValueCacheDecorator
def getPerfValue(dbName, tableName, NoneVal=None):
    """
    获取性能数据
    @param NoneVal: <int>为Null时，指定输出的默认值
    @param pefValueTimeRange: 与当前时间相距N(秒)的值仍有效
    """
    
    pefValueTimeRange = sysStaticConf.get('selectTimeRange', 'pefValueTimeRange')
    try:
        db = dbManager.getNetPerfDB(dbName)
    except Exception, e:
        print e
        return NoneVal
    
    table = db[tableName]
    condition = {'_id': {'$gte':time.time() - pefValueTimeRange}} #在N时间内的数据中，找到最近的一条
    
    cursor = table.find(condition).sort('_id', -1)
    val = NoneVal
    for data in cursor:
        val = data.get('value', NoneVal)
        break
    
    return val


def getPerfValues(dbName, tableName, sTime, eTime=None, NoneVal=None):
    """
    获取一段时间内性能数据
    """
    if not  eTime: eTime = time.time()
    try:
        db = dbManager.getNetPerfDB(dbName)
    except Exception, e:
        print e
        return []
    
    table = db[tableName]
    condition = {"$and":[{'_id': {'$gt':sTime}},{'_id': {'$lte':eTime}}]} #时间范围
    
    cursor = table.find(condition).sort('_id', 1)
    rs = []
    for data in cursor:
        _data = {"time":data.get('_id', 0), "val":data.get('value', NoneVal)}
        rs.append(_data)
    
    return rs

def getEndPerfValue(dbName,tableName,endTime,NoneVal=None):
    """
        获取一段时间内的最新性能数据
    @param NoneVal: <int>为Null时，指定输出的默认值
    @param pefValueTimeRange: 与当前时间相距N(秒)的值仍有效
    """
    pefValueTimeRange = sysStaticConf.get('selectTimeRange', 'pefValueTimeRange')
    try:
        db = dbManager.getNetPerfDB(dbName)
    except Exception, e:
        print e
        return NoneVal
    
    table = db[tableName]
    condition = {'_id': {'$gte':endTime-pefValueTimeRange}}
    cursor = table.find(condition).sort('_id', -1) 
    for data in cursor:
        val=data.get('value', NoneVal)
        if val!=NoneVal:return data.get('value', NoneVal)
    return NoneVal

def getStatusValue(dbName, tableName, recordId, NoneVal=None):
    """
    获取状态\字符数据结果
    @param coll: <collector>
    @param dbName: <string> == moUid
    @param recordId: <string> == "|".join tpl+ds+dp   
    """
    statusValueTimeRange = sysStaticConf.get('selectTimeRange', 'statusValueTimeRange')
    try:
        db = dbManager.getNetPerfDB(dbName)
    except Exception, e:
        print e
        return NoneVal
    
    table = db[tableName]
    
    condition = {"_id":recordId, "timeId": {"$gte":time.time() - statusValueTimeRange}}
    cursor = table.find(condition).sort("timeId",-1)
    for data in cursor:
        return data.get('value', NoneVal)
    return NoneVal
    
@getEventStatusValueCacheDecorator
def getEventStatusValue(dbName, tableName, timeRange=600, NoneVal=-1):
    """
    获取状态事件值
    @param coll: <collector>
    @param dbName: <string> == ctype-moUid
    """
    try:
        db = dbManager.getNetPerfDB(dbName)
    except Exception, e:
        print e
        return NoneVal
    
    table = db[tableName]
    
    condition = {"_id": {"$gte":time.time() - timeRange}}
    cursor = table.find(condition).sort("_id",-1)
    val = NoneVal
    for data in cursor:
        val = data.get('value', NoneVal)
        break
    
    return val


def getEventStatusValues(mo, startTime, endTime=None):
    """
    获取监控对象一段时间状态事件值
    @param mo: 监控对象
    @param startTime: 开始时间
    @param endTime: 结束时间  默认当前时间
    @return: list<{"_id":var1, "value":var2}>
    """
    dbName = mo._getPerfDbName()
    tableName = mo._getStatusTableName()
    try:
        db = dbManager.getNetPerfDB(dbName)
    except Exception, e:
        print e
        return []
    
    table = db[tableName]
   
    condition ={"_id": {"$gte":startTime}} if not endTime else \
                      {"$and":[{"_id": {"$gte":startTime}}, {"_id": {"$lte":endTime}}]}
    
    cursor = table.find(condition)
    rs = [data for data in cursor]
    return rs

def getCptEventStatusValues(mo,cpt,startTime, endTime=None):
    """
        获取监控对象收集点一段时间状态事件值
    @param mo: 监控对象
    @param startTime: 开始时间
    @param endTime: 结束时间  默认当前时间
    @return: list<{"_id":var1, "value":var2}>
    """
    if not mo:return []
    dbName = mo._getPerfDbName()
    if not cpt:return []
    tableName = mo._getStatusTableName(cptUid=cpt.getUid())

    try:
        db = dbManager.getNetPerfDB(dbName)
    except Exception, e:
        print e
        return []
    table = db[tableName]
   
    condition ={"_id": {"$gte":startTime}} if not endTime else \
                      {"$and":[{"_id": {"$gte":startTime}}, {"_id": {"$lte":endTime}}]}
    
    cursor = table.find(condition)
    rs = [data for data in cursor]
    return rs

def getIpInterfaceEventStatusValues(mo, startTime, endTime=None):
    """
    获取监控对象(接口)一段时间状态事件值
    @param mo: 监控对象(接口)
    @param startTime: 开始时间
    @param endTime: 结束时间  默认当前时间
    @return: list<{"_id":var1, "value":var2}>
    """
    dbName = mo._getPerfDbName()
    tableName = mo._getPerfTablName("ethernetCsmacd", "Status", "ifOperStatus")
    try:
        db = dbManager.getNetPerfDB(dbName)
    except Exception, e:
        print e
        return []
    
    table = db[tableName]
   
    condition ={"_id": {"$gte":startTime}} if not endTime else \
                      {"$and":[{"_id": {"$gte":startTime}}, {"_id": {"$lte":endTime}}]}
    
    cursor = table.find(condition)
    rs = [data for data in cursor]
    return rs


