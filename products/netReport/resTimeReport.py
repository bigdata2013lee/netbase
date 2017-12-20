#coding=utf-8
from products.netReport.baseReport import BaseReport
class ResTimeReport(BaseReport):
    """
        站点响应时间报表
    """
    def _webSiteStatisticsPerfValue(self,details):
        """
                得到站点的统计性能值(平均响应时间求最大值)
        """
        if not details:return {}
        hvDetails=[detail for detail in details if detail.get("avgValue") is not None]
        if hvDetails:
            return sorted(hvDetails,key=lambda x:x.get("avgValue"),reverse=True)[0]
        return details[0]
    
    def _webSiteCptPerfValue(self,webSite):
        """
                站点收集点响应时间性能数据
        """
        details=[]
        cptAvgValue=None
        for cpt in webSite.collectPoints:
            datas=self.getMonitorPerfDatas(webSite,"http","time",cpt.getUid())
            perfValues=[data.get("value") for data in datas if data.get("value")]
            if perfValues:cptAvgValue=sum(perfValues)/len(perfValues)
            details.append(dict(avgValue=cptAvgValue,datas=datas))
        cptPerfStatistics=self._webSiteStatisticsPerfValue(details)
        return cptPerfStatistics
        
    def _webSitePerfValues(self):
        """
                站点响应时间性能数据
        """
        resTimePerfDatas=[]
        for monitorObj in self.monitorObjs:
            title=monitorObj.titleOrUid()
            cptPerfStatistics=self._webSiteCptPerfValue(monitorObj)
            cptPerfStatistics.update(dict(title=title))
            resTimePerfDatas.append(cptPerfStatistics)
        return resTimePerfDatas

    def _webSiteResTimeTop(self,resTimePerfDatas):
        """
        web站点响应时间的排行
        """
        return sorted(resTimePerfDatas,key=lambda x:x.get("avgValue"),reverse=True)[:10]
    
    def _webSiteResTimeTrend(self,restWebSiteTops):
        """
                站点响应时间趋势图
        """
        resTimeTrendValue={}
        for restWebSiteTop in restWebSiteTops:
            title=restWebSiteTop.get("title")
            rtPerfs=restWebSiteTop.get("datas")
            resTimeTrendValue[title]=self.trendProcess(rtPerfs,self.getWithinAvgValue)
        return resTimeTrendValue

    def getReport(self):
        """
                站点响应时间报表
        """
        resTimePerfDatas=self._webSitePerfValues()
        resTimeTops=self._webSiteResTimeTop(resTimePerfDatas)
        avgResTimeTrendValue=self._webSiteResTimeTrend(resTimeTops)
        avgResTimeTrendLineFilePath=self.rgh.makeResTimeTrendGraph(avgResTimeTrendValue,"站点平均响应时间趋向图","avgResTimeTrendLineFilePath")
        [resTimeTop.pop("datas") for resTimeTop in resTimeTops]
        return resTimeTops,avgResTimeTrendLineFilePath