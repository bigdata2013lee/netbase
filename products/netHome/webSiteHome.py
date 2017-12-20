#coding=utf-8
import time
from products.netModel.website import Website
from products.netPerData import manager
from products.netPublicModel.userControl import UserControl
from products.netModel.mongodbManager import getNetPerfDB
from products.netHome.timeIntervalUtil import TimeIntervalUtil
from products.netEvent.monitorObjEvent import MonitorObjEvent
class WebSiteHome(MonitorObjEvent):
    """
    web站点首页
    """
    def __init__(self,webSiteClass=None):
        """
        初始化方法
        """
        self.webSiteClass=webSiteClass
        self.allWebSites=self.getAllWebSites()
    
    def getAllWebSites(self):
        """
        得到用户下的所有站点
        """
        #conditions = {}
        #UserControl.addCtrlCondition(conditions)
        if self.webSiteClass is None:return []
        ws = self.webSiteClass.getAllMonitorObjs()
        #ws = Website._findObjects(conditions)
        return ws
    
    def getWebSiteStatusAvailability(self,timeRange=3600):
        """
            得到所有站点的状态可用性列表
        """
        statusAvailabilitys=[]
        start, end=time.time()-timeRange,time.time()
        for webSite in self.allWebSites:
            _id = webSite.getUid()
            hostName=webSite.getManageId()
            statusAvailability=self.getWebSiteCptStatusAvailability(webSite,start, end)
            statusAvailability.update(dict(hostName=hostName))
            statusAvailability.update(dict(_id=_id))
            statusAvailabilitys.append(statusAvailability)
        return statusAvailabilitys
    
    def getWebSiteCptStatusAvailability(self,webSite,start, end):
        """
                得到站点所有收集点的状态可用性
        """
        details=[]
        cpts=webSite.collectPoints
        statusCount={"up":0,"down":0,"unknown":0}
        for cpt in cpts:
            cptTitle=cpt.titleOrUid()
            cptStatus=webSite.getCptStatus(cpt)
            statusCount[cptStatus]+=1
            cptAvailability=self.monitorWebSiteCptAvailability(webSite,cpt,start, end)
            details.append(dict(cptTitle=cptTitle,cptStatus=cptStatus,cptAvailability=cptAvailability))
        availability=self._webSiteStatisticsAvailability(details).get("cptAvailability")
        status=self._webSiteStatisticsStatus(statusCount)
        return dict(availability=availability,status=status,details=details)
    
    def _webSiteAvailabilitysTop(self,timeRange=3600):
        """
        web站点可用性的排行
        """
        availWebSiteTops=[]
        start, end=time.time()-timeRange,time.time()
        for webSite in self.allWebSites:
            hostName=webSite.getManageId()
            details=self._getWebSiteCptAvailability(webSite, start, end)
            cptStatistics=self._webSiteStatisticsAvailability(details)
            availWebSiteTops.append(dict(mobj=webSite,hostName=hostName,mcpt=cptStatistics.get("mcpt"),
                                                        availability=cptStatistics.get("cptAvailability")))
        return sorted(availWebSiteTops,key=lambda x:x.get("availability"),reverse=False)

    
    def _getWebSiteCptAvailability(self,webSite,start, end):
        """
                得到站点所有收集点的可用性
        """
        details=[]
        cpts=webSite.collectPoints
        for cpt in cpts:
            cptTitle=cpt.titleOrUid()
            cptAvailability=self.monitorWebSiteCptAvailability(webSite,cpt,start, end)
            details.append(dict(mcpt=cpt,cptTitle=cptTitle,cptAvailability=cptAvailability))
        return details
    
    def _webSiteStatisticsAvailability(self,details):
        """
                    站点的统计可用性(求所有收集点中可用性最低)
        """
        if not details:return {}
        hvDetails=[detail for detail in details if detail.get("cptAvailability") is not None]
        if hvDetails:
            return sorted(hvDetails,key=lambda x:x.get("cptAvailability"),reverse=False)[0]
        return details[0]
    
    def _webSiteStatisticsStatus(self,statusCount):
        """
                站点的统计状态
        """
        if statusCount["up"]>0:status="up"
        elif statusCount["down"]>0:status="down"
        else:status="unknown"
        return status
        
    def monitorWebSiteCptAvailability(self,website,cpt,start, end):
        """
            得到监控对象收集点可用性
            ＠start:开始时间
            ＠end:结束时间
        """
        statusResults=self._monitorWebSiteCptStatusValues(website,cpt,start, end)
        availability=self._monitorObjAvailabilityRatio(statusResults)
        return availability
    
    def _monitorWebSiteCptStatusValues(self,website,cpt,start, end):
        """
                站点对象某个收集点的状态值
        """
        createTime=website.createTime
        if end<=createTime:return []
        if createTime>start:start=createTime
        statusResults=manager.getCptEventStatusValues(website,cpt,start, end)
        return statusResults
        
        
    def getWebSiteEventList(self,limit=100):
        """
        得到站点当前事件列表
        """
        webSiteEvents=[]
        for webSite in self.allWebSites:
            severity={"$gte":3}
            hostName=webSite.getManageId()
            componentType=webSite.getComponentType()
            conditions=self._monitorObjEventConditions(webSite,severity)
            eventResults=self._monitorObjCurrentEvents(conditions)
            for event in eventResults:
                webSiteEvent=dict(hostName=hostName,
                                                        severity=event.severity,
                                                        firstTime=event.firstTime,
                                                        endTime=event.endTime,
                                                        componentType=componentType,
                                                        message=event.message)
                webSiteEvents.append(webSiteEvent)
        allEvents=sorted(webSiteEvents,key=lambda x:(x.get("endTime"),x.get("severity")),reverse=True)
        return allEvents[:limit]
    
    def getAvailabilitysTops(self,limit=10,timeRange=3600):
        """
                得到站点可用性的Top n线性分布
        """
        topAvailabilitys={}
        tiu=TimeIntervalUtil()
        IntervalTimes=tiu.getIntervalTime(timeRange)
        availWebSiteTops=self._webSiteAvailabilitysTop(timeRange)[:limit]
        for availWebSite in availWebSiteTops:
                topAvailability=[]
                webSite=availWebSite.get("mobj")
                hostName=availWebSite.get("hostName")
                mcpt=availWebSite.get("mcpt")
                if not mcpt:continue
                cptTitle=mcpt.titleOrUid()
                for IntervalTime in IntervalTimes:
                    start, end=IntervalTime.get("firstTime"),IntervalTime.get("lastTime")
                    availability=self.monitorWebSiteCptAvailability(webSite, mcpt, start, end)
                    topAvailability.append(availability)
                topAvailabilitys["%s线路:%s"%(cptTitle,hostName)]=topAvailability
        strTime=[IntervalTime.get("date") for IntervalTime in IntervalTimes]
        return {"rs":topAvailabilitys,"strTime":strTime}
    
    def getResponesTimeTops(self,limit=10,timeRange=3600):
        """
        得到站点响应时间的Top n
        """
        topPerfs={}
        tiu=TimeIntervalUtil()
        IntervalTimes=tiu.getIntervalTime(timeRange)
        restWebSiteTops=self._webSiteResponseTimeTop(timeRange)[:limit]
        for restWebSiteTop in restWebSiteTops:
            topPerfValues=[]
            webSite=restWebSiteTop.get("mobj")
            hostName=restWebSiteTop.get("hostName")
            mcpt=restWebSiteTop.get("mcpt")
            if not mcpt:continue
            cptTitle=mcpt.titleOrUid()
            for IntervalTime in IntervalTimes:
                start,end=IntervalTime.get("firstTime"),IntervalTime.get("lastTime")
                avgValue,maxValue,lastValue=self._webSiteCptPerfValue(webSite,mcpt,start, end)
                topPerfValues.append(avgValue)
            topPerfs["%s线路:%s"%(cptTitle,hostName)]=topPerfValues
        strTime=[IntervalTime.get("date") for IntervalTime in IntervalTimes]
        return {"rs":topPerfs,"strTime":strTime}
        
    def getWebSiteReponseTime(self,timeRange=3600):
        """
                得到站点的当前响应时间和平均响应时间
        """
        webSitePerfs=[]
        start,end=time.time()-timeRange,time.time()
        for webSite in self.allWebSites:
            hostName=webSite.getManageId()
            _id = webSite.getUid()
            details=self._webSitePerfValue(webSite, start, end)
            cptPerfStatistics=self._webSiteStatisticsPerfValue(details)
            [detail.pop("mcpt") for detail in details]
            webSitePerfs.append(dict(hostName=hostName,_id=_id,avgValue=cptPerfStatistics.get("cptAvgValue"),
                                        lastValue=cptPerfStatistics.get("cptLastValue"),details=details))
        return webSitePerfs
    
    def _webSiteStatisticsPerfValue(self,details):
        """
                    得到站点的统计性能值(平均响应时间求最大值)
        """
        if not details:return {}
        hvDetails=[detail for detail in details if detail.get("cptAvgValue") is not None]
        if hvDetails:
            return sorted(hvDetails,key=lambda x:x.get("cptAvgValue"),reverse=True)[0]
        return details[0]
        
    
    def getCptPerValues(self,mobj,cpt,conditions):
        """
                    获取某站点的某个收集点的一定时间段内的性能值
        """
        datas = []
        dbName=mobj._getPerfDbName()
        db =getNetPerfDB(dbName)
        tpl=mobj.getBaseTemplate()
        tableName = mobj._getPerfTablName(tpl.getUid(), "http", "time",cpt.getUid())
        table = db[tableName]
        cursor = table.find(conditions)
        for data in cursor:
            datas.append(data)
        return datas
    
    def getWebSiteDistribution(self,limit=5,timeRange=3600):
        """
        得到站点可用性,延时情况分布图
        """
        from products.netUtils.distributionGraph import DistributionGraph
        delayAvailability={}
        dg=DistributionGraph()
        start, end=time.time()-timeRange,time.time()
        for webSite in self.allWebSites:
            hostName=webSite.getManageId()
            availability=self.monitorObjAvailability(webSite, start, end)            
            delay=1-self._webSiteDelay(webSite, start, end)
            if availability is not None:
                unavailability=1-availability
                delayAvailability[hostName]=(unavailability*100,delay*100,(1-unavailability-delay)*100)
            else:
                delayAvailability[hostName]=(0,0,0)
        distributionDatas=dict(sorted(delayAvailability.iteritems(),key=lambda x:x[1],reverse=True)[:limit])
        return dg.makeWebSiteDistributionGraph(distributionDatas)

    
    def _webSiteResponseTimeTop(self,timeRange=3600):
        """
        web站点响应时间的排行
        """
        restWebSiteTops=[]
        start, end=time.time()-timeRange,time.time()
        for webSite in self.allWebSites:
            hostName=webSite.getManageId()
            details=self._webSitePerfValue(webSite, start, end)
            cptPerfStatistics=self._webSiteStatisticsPerfValue(details)
            restWebSiteTops.append(dict(mobj=webSite,hostName=hostName,mcpt=cptPerfStatistics.get("mcpt"),
                                                            avgValue=cptPerfStatistics.get("cptAvgValue")))
        return sorted(restWebSiteTops,key=lambda x:x.get("avgValue"),reverse=False)
    
    def _webSitePerfValue(self,webSite,start, end):
        """
                    站点所有收集点的性能数据
        """
        details=[]
        cpts=webSite.collectPoints
        for cpt in cpts:
            cptTitle=cpt.titleOrUid()
            cptAvgValue,cptMaxValue,cptLastValue=self._webSiteCptPerfValue(webSite,cpt,start, end)
            details.append(dict(mcpt=cpt,cptTitle=cptTitle,cptAvgValue=cptAvgValue,cptLastValue=cptLastValue))
        return details
  
    def _webSiteCptPerfValue(self,webSite,cpt,start, end):
        """
                    某收集点一个时间段内性能的平均值,最大值,最近值
        """
        conditions=self._webSitePerfConditions(start, end)
        datas=self.getCptPerValues(webSite,cpt,conditions)
        perfValues=[data.get("value") for data in datas]
        if not perfValues:return (None,None,None)
        avgValue=sum(perfValues)/len(perfValues)
        maxValue=max(perfValues)
        lastValue =perfValues[-1]
        return avgValue,maxValue,lastValue

    def _webSiteDelay(self,webSite,start, end):
        """
        站点的延时分布
    @webSite站点对象
        ＠start:开始时间
        ＠end:结束时间
        """
        severity={"$gte":3,"$lt":5}
        conditions=self._monitorObjEventConditions(webSite,severity,start, end)
        eventResults=self._monitorObjTotalEvents(conditions)
        delay=self._monitorObjRatio(eventResults, start, end)
        return delay

    def _webSitePerfConditions(self,start, end):
        """
        得到站点性能的条件
        """
        conditions = {"_id":{"$gte":start, "$lte":end}}
        return conditions
        
if __name__=="__main__":
    from products.netPublicModel.startNetbaseApp import startApp
    startApp()
    UserControl.login("netbase","netbase")
    wsh=WebSiteHome()
    