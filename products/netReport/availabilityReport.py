#coding=utf-8
from products.netReport.baseReport import BaseReport
class AvailabilityReport(BaseReport):
    """
        可用性报表
    """    
    def _webSiteStatisticsAvailability(self,details):
        """
                站点的统计可用性(求所有收集点中可用性最低)
        """
        hvDetails=[detail for detail in details if detail.get("availability") is not None]
        if hvDetails:
            return sorted(hvDetails,key=lambda x:x.get("availability"),reverse=False)[0]
        return details[0]
    
    def _getWebSiteCptAvailability(self,webSite):
        """
                得到站点所有收集点的可用性
        """
        details=[]
        cpts=webSite.collectPoints
        for cpt in cpts:
            statusResults=self.prd._webSiteCptStatusValues(webSite,cpt)
            availability=self._monitorObjAvailabilityRatio(statusResults)
            details.append(dict(availability=availability,datas=statusResults))
        if not details:return None
        avalResults=self._webSiteStatisticsAvailability(details)
        return avalResults
    
    def _monitorObjAvailabilityRatio(self,statusResults):
        """
                监控对象的可用性比率
        """
        if not statusResults:return None
        availabilityCount=[i.get("value") for i in statusResults if i.get("value",0)==1]
        availability=len(availabilityCount)/float(len(statusResults))
        return availability*100
    
    def _monitorObjAvailability(self,monitorObj):
        """
                监控对象的可用性
        """
        if monitorObj.getComponentType()=="Website":
            avalResults=self._getWebSiteCptAvailability(monitorObj)
        else:
            statusResults=self.prd._monitorObjStatusValues(monitorObj)
            availability=self._monitorObjAvailabilityRatio(statusResults)
            avalResults=dict(availability=availability,datas=statusResults)
        return avalResults
    
    def _availabilitysTop(self):
        """
                可用性的排行
        """
        availTops=[]
        for monitorObj in self.monitorObjs:
            avalResults=self._monitorObjAvailability(monitorObj)
            if avalResults is None:continue
            title=monitorObj.titleOrUid()
            avalResults.update(dict(title=title))
            availTops.append(avalResults)
        return sorted(availTops,key=lambda x:x.get("availability"),reverse=True)[:10]
    
    def _availabilityTrendReport(self,availTops):
        """
                可用性趋势报表
        """
        availTrendValue={}
        for availTop in availTops:
            datas=availTop.get("datas")
            title=availTop.get("title")
            availTrendValue[title]=self.trendProcess(datas,self.getWithinRatioValue)
        return availTrendValue
    
    def getReport(self):
        """
                可用性报表
        """
        availTops=self._availabilitysTop()
        availTrendValue=self._availabilityTrendReport(availTops)
        availTrendLineFilePath=self.rgh.makeAvilTrendGraph(availTrendValue,"可用性趋向图","availTrendLineFilePath")
        [availTop.pop("datas") for availTop in availTops]
        return availTops,availTrendLineFilePath