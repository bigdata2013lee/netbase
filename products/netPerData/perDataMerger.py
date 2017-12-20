#coding=utf-8
import time
from products.netModel.mongodbManager import getNetPerfDB
from netmerger import MergerData
from products.netUtils.mcClient import getPerfDataByTimeUnitCacheDecorator

class PerDataMerger(object):
    """
        性能数据合并和展示
    """
    
    mergeTimeDict={"day":[5,1*24*60*60],"week":[30,7*24*60*60],"month":[180,30*24*60*60]}

    @getPerfDataByTimeUnitCacheDecorator
    def getPerfDataByTimeUnit(self,collector,dbName,tableName,createTime,timeUnit):
        """
                得到一定时间单位内的性能数据
        """
        self.md=MergerData()
        mergeTime=self.mergeTimeDict[timeUnit][0]
        self.startTime=time.time()-self.mergeTimeDict[timeUnit][1]
        if self.startTime<createTime:self.startTime=createTime
        func=getattr(self,"_perfOne%s"%timeUnit.capitalize())
        perfDatas=func(collector,dbName,tableName,mergeTime)
        perfDatas=sorted(perfDatas,key=lambda x:x.get("_id"),reverse=False)
        self.__addBeValues(perfDatas, mergeTime)
        return self.__perfReduce(self.__fillPerfValue,perfDatas,mergeTime,[])
    
    def _perfOneDay(self,collector,dbName,tableName,mergeTime):
        """
                得到当前数据
        """
        rangeTime=None
        perfDatas = self._getPerfData(collector,dbName,tableName,mergeTime,rangeTime)
        return perfDatas
    
    def _perfOneWeek(self,collector,dbName,tableName,mergeTime):
        """
                得到一周的数据
        """
        rangeTime=30
        perfDatas = self._getPerfData(collector,dbName,tableName,mergeTime,rangeTime)
        dayDatas=self._perfOneDay(collector, dbName, tableName,mergeTime)
        perfDatas.extend(self.md._mergeData(dayDatas,rangeTime))
        return perfDatas
    
    def _perfOneMonth(self,collector,dbName,tableName,mergeTime):
        """
                得到一个月的数据
        """
        rangeTime=180
        perfDatas = self._getPerfData(collector,dbName,tableName,mergeTime,rangeTime)
        dayDatas=self._perfOneWeek(collector, dbName, tableName,mergeTime)
        perfDatas.extend(self.md._mergeData(dayDatas, rangeTime))
        return perfDatas

    def _getPerfData(self,collector,dbName,tableName,mergeTime,rangeTime):
        """
                得到性能数据
        """
        datas = []
        etime=self.md._getDivTime(time.time(),mergeTime)*mergeTime*60
        if self.startTime>=etime:return datas
        stime=self.md._getDivTime(self.startTime,mergeTime)*mergeTime*60
        conditions = {'_id':{"$lt": etime,"$gt":stime}, 'range':rangeTime}#原始数据
        try:
            db =getNetPerfDB(dbName)
        except Exception:
            return datas
        table = db[tableName]
        cursor = table.find(conditions)
        for data in cursor:
            datas.append(data)
        return datas
    
    def __fillPerfValue(self,x,y,mergeTime):
        """
                性能补值
        """
        value=y.get("value")
        _idy=y.get("_id")*1000
        if not x:return [[_idy,value]]
        _idx=x[-1][0]
        for i in xrange(1,int(_idy-_idx)/(mergeTime*60*1000)):
            x.append([_idx+mergeTime*i*60*1000,None])
        x.append([_idy,value])
        return x
    
    def __addBeValues(self,iterable,mergeTime):
        """
                添加首尾的值
        """
        if not iterable or iterable[0].get("_id")-mergeTime*60>self.startTime:
            _id=(self.md._getDivTime(self.startTime,mergeTime)+0.5)*mergeTime*60
            iterable.insert(0,dict(_id=_id,value=None))
        if iterable[-1].get("_id")+mergeTime*60<time.time():
            _id=(self.md._getDivTime(time.time(),mergeTime)+0.5)*mergeTime*60
            iterable.append(dict(_id=_id,value=None))

    def __perfReduce(self,function,iterable,mergeTime,initializer=None):
        """
                性能换算
        """
        it = iter(iterable)
        if initializer is None:
            initializer = next(it)
        accum_value = initializer
        for x in iterable:
            accum_value = function(accum_value,x,mergeTime)
        return accum_value