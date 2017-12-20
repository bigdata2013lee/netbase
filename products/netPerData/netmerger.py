#coding=utf-8
import os
import time
import re
import logging
from twisted.internet import reactor
from products.netUtils.cmdBase import CmdBase
from products.netModel.mongodbManager import getNetPerfDB,getPerfDataBaseNames
log = logging.getLogger("netmerge")
class CountObj(object):
    """
        合并数据统计
    """
    def __init__(self):
        self._val=0
        self._count=0

    def sum(self,value):
        """
                求和
        """
        if value is None: return self._val
        self._count+=1
        self._val+=value
        return self._val
    
    def avg(self):
        """
                求平均
        """
        return self._val/self._count

class MergerData(object):
    """
        数据合并类
    """
    
    def perfDbNames(self):
        """
                性能数据库名称
        """
        perfDbNames=[]
        monitors=["Bootpo","Device","FileSystem","IpInterface","IpService","Process","Website"]
        dbNames=getPerfDataBaseNames()
        if dbNames is None:return None
        for dbName in dbNames:
            if dbName.split("-",1)[0] in monitors:
                perfDbNames.append(dbName)
        return perfDbNames
    
    def getTableObjs(self,dbName):
        """
                得到某一个库中的所有性能表对象
        """
        tableObjs=[]
        db=getNetPerfDB(dbName)
        tablesName=db.collection_names()
        pattern = r'^\w+\:\w+\|\w+\|\w+$' #性能数据表名格式
        tbNames = filter(lambda tbName:  re.match(pattern, tbName) is not None, tablesName)
        if not tbNames:return  None
        for tbName in tbNames:
            tableObjs.append(db[tbName])
        return tableObjs
    
    def getStatusTableObjs(self,dbName):
        """
        得到某一个库中的所有状态表对象
        """
        tableObjs=[]
        db=getNetPerfDB(dbName)
        tablesName=db.collection_names()
        pattern = r'^\w+\:status$' #性能数据表名格式
        tbNames = filter(lambda tbName:  re.match(pattern, tbName) is not None, tablesName)
        if not tbNames:return  None
        for tbName in tbNames:
            tableObjs.append(db[tbName])
        return tableObjs
           
    
    def _deleteAfterOneMonth(self,table):
        """
                删除1个月前的状态数据
        """
        ltime=30*24*60*60 #1个月的时间差
        conditions = {'_id':{"$lt": time.time()-ltime}}
        table.remove(conditions)
    
    def mergerPerfData(self):
        """
                性能数据合并
        """
        perfDbNames=self.perfDbNames()
        if perfDbNames is None:return
        for dbName in perfDbNames:
            tableObjs=self.getTableObjs(dbName)
            if tableObjs is not None:
                for tableObj in tableObjs:
                    print "merger table %s" %str(tableObj)
                    self._mergerOneWeek(tableObj)
                    self._mergerOneMonth(tableObj)
                    self._mergerHalfYear(tableObj)
                    self._deleteSixMonth(tableObj)

  
        log.info("数据合并完成!")

    def  removeStatusData(self):
        "删除状态表中的过期数据"
        perfDbNames=self.perfDbNames()
        if perfDbNames is None: return
        for dbName in perfDbNames:
            statusTableObjs = self.getStatusTableObjs(dbName)
            for statusTableObj in statusTableObjs or  []:
                self._deleteAfterOneMonth(statusTableObj)
                    
                    
            
    def _getOldData(self,table,conditions):
        """
                得到老数据
        """
        _oldDatas = []
        cursor = table.find(conditions).sort("_id", 1)
        for odata in cursor:
            _oldDatas.append(odata)
        return _oldDatas
    
    def _mergerOneWeek(self,table):
        """
                合并一天到一周之间的数据(30分钟)
        """
        rangeTime=30#分钟
        ltime=1*24*60*60#一天的时间差
        stime=self._getDivTime(time.time(),rangeTime)*rangeTime*60
        conditions = {'_id':{"$lt": stime-ltime}, 'range':None}#早于一周小于一个月的数据
        oldDatas = self._getOldData(table, conditions)
        mergeDatas=self._mergeData(oldDatas, rangeTime)
        self.__deleteOldPerDatas(table,oldDatas)
        self.__insertMergePerfDatas(table, mergeDatas)
        
    
    def _mergerOneMonth(self,table,trange=30):
        """
                合并一周到一个月之间的数据
        """
        rangeTime=180 #三个小时
        ltime=7*24*60*60 #一周的时间差
        gtime=30*24*60*60 #一个月的时间差
        stime=self._getDivTime(time.time(),rangeTime)*rangeTime*60
        conditions = {'_id':{"$lt": stime-ltime,"$gt":stime-gtime}, 'range':trange}
        oldDatas = self._getOldData(table, conditions)
        mergeDatas=self._mergeData(oldDatas, rangeTime)
        self.__deleteOldPerDatas(table,oldDatas)
        self.__insertMergePerfDatas(table, mergeDatas)
    
    def _mergerHalfYear(self,table,trange=180):
        """
                合并一月到六个月之间的数据
        """
        rangeTime=60*24 #一天
        ltime=30*24*60*60 #一个月的时间差
        gtime=6*30*24*60*60 #六个月的时间差
        stime=self._getDivTime(time.time(),rangeTime)*rangeTime*60
        conditions = {'_id':{"$lt": stime-ltime,"$gt":stime-gtime}, 'range':trange}
        oldDatas = self._getOldData(table, conditions)
        mergeDatas=self._mergeData(oldDatas, rangeTime)
        self.__deleteOldPerDatas(table,oldDatas)
        self.__insertMergePerfDatas(table, mergeDatas)
    
    def _deleteSixMonth(self,table,trange=60*24):
        """
                删除六个月以上的数据
        """
        ltime=6*30*24*60*60 #六个月的时间差
        conditions = {'_id':{"$lt": time.time()-ltime}, 'range':trange}
        table.remove(conditions)

    def _mergeData(self,datas,rangeTime):
        """
                数据合并
        """
        mergeDatas=[]
        _dictDatas={}
        for data in datas:
            timeId=data.get("_id")
            __divValue=self._getDivTime(timeId,rangeTime)
            countObj = _dictDatas.get(__divValue,CountObj())
            countObj.sum(data['value'])
            _dictDatas[__divValue] = countObj
            
        for key, countObj in _dictDatas.items():
            timeId =(key+0.5)*rangeTime*60
            mergeDatas.append({
               "_id": timeId, 'value': countObj.avg(), 'range':rangeTime
            })
        
        return sorted(mergeDatas,key=lambda x:x.get("_id"),reverse=False)
                
    def _getDivTime(self,timeId,rangeTime):
        """
                对时间整除
        """
        __divValue=int(timeId)/(rangeTime*60)
        return __divValue
    
    def __insertMergePerfDatas(self,table,datas):
        """
                插入合并后的性能数据
        """
        if not datas: return
        bsize = 200
        while datas:
            batch = datas[:bsize]
            table.insert(batch)
            datas = datas[bsize:]
    
    def __deleteOldPerDatas(self,table, datas):
        """
                删除原有的性能数据
        """
        if not datas: return
        conditions = {"_id":{"$in":[]}}
        bsize = 200
        while datas:
            batch = datas[:bsize]
            conditions['_id']['$in'] = [ d['_id'] for d in batch]
            table.remove(conditions)
            datas = datas[bsize:]
    

    
class netmerger(CmdBase):
    """
        合并数据守护进程类
    """
    mergerCycleTime=6*3600
    
    def __init__(self):
        CmdBase.__init__(self)
        
    def startMerger(self):
        """
                开始合并(每六小时合并一次)
        """
        log.info("开始数据合并!")
        md=MergerData()
        md.mergerPerfData()
        
        log.info("开始状态数据清理!")
        md.removeStatusData()
        reactor.callLater(self.mergerCycleTime,self.startMerger)
        
        
    def run(self):
        """
                执行
        """
        self.startMerger()
        reactor.run()

if __name__=="__main__":
    nm=netmerger()
    nm.run()
        
    