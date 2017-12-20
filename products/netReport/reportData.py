#coding=utf-8
from products.netModel.mongodbManager import getNetPerfDB
from products.netPerData import manager
from products.netUtils import xutils
class ReportData(object):
    """
        报表数据
    """
    
    def __init__(self,startTime,endTime):
        """
                初始化
        """
        self.endTime=endTime
        self.startTime=startTime
    
    def getPerfDataByTimeUnit(self,monitorObj,tableName):
        """
                得到一定时间段内的性能数据
        """
        #获取性能数据
        perfDatas=self._getPerfData(monitorObj,tableName)
        return sorted(perfDatas,key=lambda x:x.get("_id"),reverse=False)

    def _getPerfData(self,monitorObj,tableName):
        """
                得到性能数据
        """
        datas = []
        #得到对象的收集器,数据库名和创建时间
        dbName = monitorObj._getPerfDbName()
        conditions = {'_id':{"$lte": self.endTime,"$gte":self.startTime}}
        try:
            db =getNetPerfDB(dbName)
        except Exception:
            return datas
        table = db[tableName]
        cursor = table.find(conditions)
        for data in cursor:
            datas.append(data)
        return datas
    
    def diskUtilization(self,filesystem,usedCapacity):
        "使用率"
        if not filesystem.capacity: return 0
        return usedCapacity*100/float(filesystem.capacity)
    
    def diskUsedCapacity(self,filesystem,blockSize):
        """
                已用磁盘
        """
        dbName = filesystem._getPerfDbName()
        tableName = filesystem._getPerfTablName("FileSystem", "Used", "usedBlocks")
        val = manager.getEndPerfValue(dbName,tableName,self.endTime)
        if val is None: return 0
        return val*blockSize
    
    def _webSiteCptStatusValues(self,website,cpt):
        """
                站点对象某个收集点的状态值
        """
        startTime=self.startTime
        createTime=website.createTime
        if self.endTime<=createTime:return []
        if createTime>self.startTime:startTime=createTime
        statusResults=manager.getCptEventStatusValues(website,cpt,startTime,self.endTime)
        return statusResults
    
    def _monitorObjStatusValues(self,monitorObj):
        """
                监控对象的状态值
        """
        startTime=self.startTime
        createTime=monitorObj.createTime
        if self.endTime<=createTime:return []
        if createTime>self.startTime:startTime=createTime
        statusResults=manager.getEventStatusValues(monitorObj,startTime,self.endTime)
        return statusResults
    
    def _monitorObjEvents(self,monitorObj,severity=3):
        """
                监控对象某个事件段内的所有事件
        """
        conditions={}
        severity={"$gte":severity}
        moUid=monitorObj.getUid()
        componentType=monitorObj.getComponentType()
        if self.startTime and self.endTime: conditions={"$and":[{"firstTime":{"$lte":self.endTime}},{"endTime":{"$gte":self.startTime}}]}
        conditions.update(dict(severity=severity))
        conditions.update({"$or":[{"device":moUid},{"moUid":moUid, "componentType": componentType}]})
        evtMgr = xutils.getEventManager()
        eventResults=evtMgr.findEvents(conditions)
        return eventResults
    
