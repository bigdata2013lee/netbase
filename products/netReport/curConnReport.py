#coding=utf-8
from products.netReport.baseReport import BaseReport
class CurConnReport(BaseReport):
    """
        当前连接数报表
    """
    def getCurConnPerfValues(self):
        """
                得到连接数性能值
        """
        curConnPerfDatas={}
        for monitorObj in self.monitorObjs:
            curConnPerfValue=self.getMonitorPerfDatas(monitorObj,"Conn","CurrentConn")
            curConnPerfDatas[monitorObj]=curConnPerfValue
        return curConnPerfDatas

    def getReport(self):
        """
                连接数报表
        """
        curConnPerfDatas=self.getCurConnPerfValues()
        topTenCurConns=self.perfTop(curConnPerfDatas)
        avgCurConnTrendValue=self.perfTrendReport(topTenCurConns)
        avgConnTrendLineFilePath=self.rgh.makeConnTrendGraph(avgCurConnTrendValue,"连接数趋向图","avgConnTrendLineFilePath")
        [topTenCurConn.pop("datas") for topTenCurConn in topTenCurConns]
        return topTenCurConns,avgConnTrendLineFilePath