#coding=utf-8
from products.netReport.baseReport import BaseReport
class EventReport(BaseReport):
    def getMonitorEvents(self):
        """
                得到监控对象事件
        """
        eventDatas={}
        for monitorObj in self.monitorObjs:
            eventResults=self.prd._monitorObjEvents(monitorObj,3)
            eventDatas[monitorObj]=eventResults
        return eventDatas
    
    def eventTop(self,eventDatas):
        """
                事件排行
        """
        eventTenTops=[]
        for monitorObj,eventResults in eventDatas.iteritems():
            title=monitorObj.titleOrUid()
            eventTop={"title":title,5:0,4:0,3:0,"Count":0}
            for event in eventResults:
                severity=event.severity
                eventTop[severity]+=1
                eventTop["Count"]+=1
            eventTenTops.append(eventTop)
        return sorted(eventTenTops,key=lambda x:(x.get(5),x.get(4),x.get(3)),reverse=True)[:10]
    
    def getReport(self):
        """
                事件报表
        """
        eventDatas=self.getMonitorEvents()
        eventTenTops=self.eventTop(eventDatas)
        escountMultipleBarFilePath,escountPieFilePath=self.rgh.makeEscountGraph(eventTenTops)
        return escountMultipleBarFilePath,escountPieFilePath