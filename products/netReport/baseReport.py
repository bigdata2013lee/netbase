#coding=utf-8
class BaseReport(object):
    """
        报表基类
    """
    def __init__(self,prd,rgh,monitorObjs,splitDate):
        """
                初始化报表基类
        """
        self.prd=prd
        self.rgh=rgh
        self.splitDate=splitDate
        self.monitorObjs=monitorObjs
    
    def getMonitorPerfDatas(self,monitorObj,dsName,dpName,cpt=""):
        """
                获取监控对象性能数据
        """
        baseTpl = monitorObj.getBaseTemplate()
        if not baseTpl:
            return []
        tableName = monitorObj._getPerfTablName(baseTpl.getUid(),dsName,dpName,cpt)
        datas =self.prd.getPerfDataByTimeUnit(monitorObj, tableName)
        return datas
    
    def perfTrendReport(self,topTenData):
        """
                性能趋势报表
        """
        perfTrendValue={}
        for topData in topTenData:
            title=topData.get("title")
            datas=topData.get("datas")
            perfTrendValue[title]=self.trendProcess(datas,self.getWithinAvgValue)
        return perfTrendValue

    def perfTop(self,perfDatas):
        """
                性能Top
        """
        perfTopValues=[]
        for monitorObj,values in perfDatas.iteritems():
            title=monitorObj.titleOrUid()
            result=[value.get("value") for value in  values if value.get("value")]
            if not result:continue
            totalAvg=sum(result)/len(result)
            perfTopValues.append(dict(title=title,avgValue=totalAvg,datas=values))
        return sorted(perfTopValues,key=lambda x:x.get("avgValue"),reverse=True)[:10]
    
    def trendProcess(self,resultValues,function):
        """
                趋势处理
        """
        trendReportResult=[]
        if not resultValues:return trendReportResult
        for IntervalDate in self.splitDate:
            avgValue,resultValues=function(resultValues,IntervalDate)
            trendReportResult.append(avgValue)
        return trendReportResult
        
    def getWithinAvgValue(self,resultValues,IntervalDate):
        """
                间隔时间段内的平均值
        """
        count=0
        avgValue=0
        intervalValues=[]
        firstTime=IntervalDate.get("firstTime")
        lastTime=IntervalDate.get("lastTime")
        for i in xrange(len(resultValues)):
            _id=resultValues[i].get("_id")
            value=resultValues[i].get("value")
            if firstTime>_id:continue
            if not firstTime<=_id<=lastTime:
                count=i
                break
            if value is None:continue
            intervalValues.append(value)
        if intervalValues:
            sumValue=sum([j for j in intervalValues])
            avgValue=sumValue/len(intervalValues)
        return avgValue,resultValues[count:]
    
    def getWithinRatioValue(self,resultValues,IntervalDate):
        """
                间隔时间段内的比率值
        """
        count=0
        availability=0
        intervalValues=[]
        firstTime=IntervalDate.get("firstTime")
        lastTime=IntervalDate.get("lastTime")
        for i in xrange(len(resultValues)):
            _id=resultValues[i].get("_id")
            value=resultValues[i].get("value")
            if firstTime>_id:continue
            if not firstTime<=_id<=lastTime:
                count=i
                break
            if value is None:continue
            intervalValues.append(value)
        if intervalValues:
            commonCount=len([k for k in intervalValues if k==1])
            availability=commonCount*100/float(len(intervalValues))
        return availability,resultValues[count:]
 
    def getReport(self):
        """
                得到报表(所有子类必须重写该方法)
        """
        pass
            
    
    
    
