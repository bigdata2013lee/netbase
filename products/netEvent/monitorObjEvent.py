#coding=utf-8
import time
from products.netUtils import xutils
from products.netPerData import manager
class MonitorObjEvent(object):
    """
    监控对象事件类
    """
    def monitorObjAvailability(self,monitorObj, start, end):
        """
        得到监控对象的可用性
        ＠start:开始时间
        ＠end:结束时间
        """
        statusResults=self._monitorObjStatusValues(monitorObj, start, end)
        availability=self._monitorObjAvailabilityRatio(statusResults)
        return availability
    
    def getScoreAlgorithm(self,monitorObj,componentType,severity,score):
        """
                得到评分算法
        """
        count=1
        if componentType=="Website":
            count=len(monitorObj.collectPoints) or count
        if int(severity)==5:
            score-=score/count
        else:
            score-=0.5*score/count
        return score

    def monitorObjScore(self,monitorObj,timeRange=600):
        """
        监控对象的评分(昨天)
        ＠monitorObj:监控对象
        """
        score=100
        status="unknown"
        severity={"$gte":3}
        start, end=time.time()-timeRange,time.time()
        componentType=monitorObj.getComponentType()
        if componentType=="Website":
            cpts=monitorObj.collectPoints
            for cpt in cpts:
                status=cptStatus=monitorObj.getCptStatus(cpt)
                if cptStatus!="unknown":break
        else:status=monitorObj.getStatus()
        if status=="unknown":return None
        conditions=self._monitorObjEventConditions(monitorObj,severity,start,end)
        eventResults=self._monitorObjCurrentEvents(conditions)
        for event in eventResults:
            severity=event.severity
            score=self.getScoreAlgorithm(monitorObj,componentType,severity,score)
            if score<=0:return 0
        return score
    
    def _monitorObjEventConditions(self,monitorObj,severity=3,sTime=None,eTime=None):
        """
        得到监控对象事件的条件
        """
        conditions={}
        moUid=monitorObj.getUid()
        componentType=monitorObj.getComponentType()
        if sTime and eTime: conditions={"$and":[{"firstTime":{"$lte":eTime}},{"endTime":{"$gte":sTime}}]}
        conditions.update(dict(moUid=moUid,componentType=componentType,severity=severity))
        return conditions
    
    def _monitorObjRatio(self,eventResults,start,end):
        """
        得到监控对象事件的比率情况
        """
        #事件之间的正常时间
        _rangeTime=0
        length=len(eventResults)
        if not length>0:return 1
        _firstTime=eventResults[0].firstTime
        _endTime=eventResults[0].endTime
        if not length==1:
            for i in xrange(length):
                if not i<length-1:break
                if eventResults[i].endTime>=eventResults[i+1].endTime:
                    eventResults[i+1].endTime=eventResults[i].endTime
                else:
                    if eventResults[i].endTime<eventResults[i+1].firstTime:
                        _rangeTime+=eventResults[i+1].firstTime-eventResults[i].endTime
                _endTime=eventResults[i+1].endTime
        if time.time()-_endTime<=5*60 and time.time()-end<=5*60:end=_endTime
        _totalTime=end-start
        _rTime=max(_firstTime,start)-start+_rangeTime+end-min(_endTime,end)
        ratio=_rTime/float(_totalTime)
        return ratio
    
    def _monitorObjStatusValues(self,monitorObj, start, end):
        """
        监控对象的状态值
        """
        createTime=monitorObj.createTime
        if end<=createTime:return []
        if createTime>start:start=createTime
        if monitorObj.getComponentType()=="IpInterface":
            statusResults=manager.getIpInterfaceEventStatusValues(monitorObj, start, end)
        else:
            statusResults=manager.getEventStatusValues(monitorObj, start, end)
        return statusResults

    def _monitorObjAvailabilityRatio(self,statusResults):
        """
        监控对象的可用性比率
        """
        if not statusResults:return None
        availabilityCount=[i.get("value") for i in statusResults if i.get("value",0)==1]
        availability=len(availabilityCount)/float(len(statusResults))
        return availability
        
    def _monitorObjTotalEvents(self,conditions):
        """
        得到监控对象的当前事件和历史事件
        ＠conditions:事件查询条件
        """
        eventResults=self._monitorObjCurrentEvents(conditions)
        historyResults=self._monitorObjHistoryEvents(conditions)
        totalEvents=eventResults+historyResults
        return sorted(totalEvents,key=lambda x:x.firstTime,reverse=False)

    def _monitorObjCurrentEvents(self,conditions):
        """
        监控对象当前事件
        ＠conditions:事件查询条件
        """
        evtMgr = xutils.getEventManager()
        eventResults=evtMgr.findCurrentEvents(conditions=conditions)
        return eventResults
    
    def _monitorObjHistoryEvents(self,conditions):
        """
        监控对象历史事件
        ＠conditions:事件查询条件
        """
        evtMgr = xutils.getEventManager()
        historyResults=evtMgr.findHistoryEvents(conditions=conditions)
        return historyResults
    