#coding=utf-8
import time
import json
from products.netReport.timeUtil import TimeUtil
from products.netUtils.xutils import importClass
from products.netReport.reportGraph import ReportGraph
from products.netReport.reportData import ReportData
defaultRange={"day":86400,"3day":86400*3,"week":604800,"month":2592000}
class ReportBuild(object):
    """
        报表生成
    """
    def __init__(self,report):
        self.report=report
        self.startTime,self.endTime=self.reportTimeRange()
        
    def getBuildedReport(self):
        """
                得到生成后的报表
        """
        reportResults={}
        prd=ReportData(self.startTime,self.endTime)
        splitDate=self.getSplitDate()
        dateString=self.getDateString(splitDate)
        rgh=ReportGraph(dateString)
        reportConditions=self.report.conditions
        for reportType,objs in reportConditions.iteritems():
            reportClass= importClass("products.netReport.%sReport"%reportType,
                                     "%sReport"%(reportType[0].upper()+reportType[1:]))
            reportObj=reportClass(prd,rgh,objs,splitDate)
            reportResults[reportType]=reportObj.getReport()
        return json.dumps(reportResults)

    def getDateString(self,splitDate):
        """
                得到字符窜格式的日期
        """
        dateString=[i.get("date","") for i in splitDate]
        return dateString

    def getSplitDate(self):
        """
                得到分割日期
        """
        tu=TimeUtil()
        splitDate=tu.calculateSplitDate(self.startTime,self.endTime)  
        splitDate.reverse()
        return splitDate  
        
    def reportTimeRange(self):
        """
                得到时间范围
        """
        endTime=int(time.time())
        timeRange = self.report.timeRange
        reportTime=str(timeRange.get("defaultTime",""))
        if reportTime:
            timestamp=defaultRange[reportTime]
            return endTime-timestamp,endTime
        customTime=timeRange.get("customTime")
        startTime=time.mktime(time.strptime(customTime.get("startTime"),"%Y/%m/%d"))
        endTime=time.mktime(time.strptime(customTime.get("endTime"),"%Y/%m/%d"))+24*3600
        if endTime>=time.time():endTime=time.time()
        return startTime,endTime
        

        