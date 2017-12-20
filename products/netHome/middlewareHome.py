#coding=utf-8
import time
from products.netPublicModel.userControl import UserControl
from products.netHome.timeIntervalUtil import TimeIntervalUtil
from products.netEvent.monitorObjEvent import MonitorObjEvent
from products.netModel.middleware.mwApache import MwApache
from products.netModel.middleware.mwTomcat import MwTomcat
from products.netModel.middleware.mwNginx import MwNginx

class MiddlewareHome(MonitorObjEvent):
    """
    web站点首页
    """
    def __init__(self,midClass=None):
        """
        初始化方法
        """
        self.midClass=midClass
        self.allmids=self.getAllmids()
    
    def getAllmids(self):
        """
        得到用户下的所有站点
        """
        if self.midClass is None:return []
        ws = self.midClass.getAllMonitorObjs()
        return ws
    
    def getAvailabilitysTops(self,limit=10,timeRange=3600):
        """
        得到站点可用性的Top n线性分布
        """
        topAvailabilitys={}
        tiu=TimeIntervalUtil()
        IntervalTimes=tiu.getIntervalTime(timeRange)
        availMiddlewareTops=self._middlewareAvailabilitysTop(timeRange)[:limit]
        for availMiddleware in availMiddlewareTops:
                topAvailability=[]
                mid=availMiddleware.get("mobj")
                hostName=availMiddleware.get("hostName")
                for IntervalTime in IntervalTimes:
                    start, end=IntervalTime.get("firstTime"),IntervalTime.get("lastTime")
                    availability=self.monitorObjAvailability(mid, start, end)
                    topAvailability.append(availability)
                topAvailabilitys[hostName]=topAvailability
        strTime=[IntervalTime.get("date") for IntervalTime in IntervalTimes]
        return {"rs":topAvailabilitys,"strTime":strTime}
    def getMiddlewareDistribution(self,limit=5,timeRange=3600):
        """
        得到站点可用性,延时情况分布图
        """
        from products.netUtils.distributionGraph import DistributionGraph
        delayAvailability={}
        dg=DistributionGraph()
        start, end=time.time()-timeRange,time.time()
        for mid in self.allmids:
            hostName=mid.getManageId()
            availability=self.monitorObjAvailability(mid, start, end)            
            delay=1-self._middlewareDelay(mid, start, end)
            if availability is not None:
                unavailability=1-availability
                delayAvailability[hostName]=(unavailability*100,delay*100,(1-unavailability-delay)*100)
            else:
                delayAvailability[hostName]=(0,0,0)
        distributionDatas=dict(sorted(delayAvailability.iteritems(),key=lambda x:x[1],reverse=True)[:limit])
        return dg.makeWebSiteDistributionGraph(distributionDatas)
    
    def _middlewareAvailabilitysTop(self,timeRange=3600):
        """
        web站点可用性的排行
        """
        availWebSiteTops=[]
        start, end=time.time()-timeRange,time.time()
        for mid in self.allmids:
            hostName=mid.getManageId()
            availability=self.monitorObjAvailability(mid, start, end)
            availWebSiteTops.append(dict(mobj=mid,hostName=hostName,availability=availability))
        return sorted(availWebSiteTops,key=lambda x:x.get("availability"),reverse=False)
    
    def _middlewareDelay(self,mid,start, end):
        severity={"$gte":3,"$lt":5}
        conditions=self._monitorObjEventConditions(mid,severity,start, end)
        eventResults=self._monitorObjTotalEvents(conditions)
        delay=self._monitorObjRatio(eventResults, start, end)
        return delay
    
if __name__=="__main__":
    from products.netPublicModel.startNetbaseApp import startApp
    startApp()
    UserControl.login("netbase","netbase")
    wsh=MiddlewareHome()
    