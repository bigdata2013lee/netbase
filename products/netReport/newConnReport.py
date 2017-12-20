#coding=utf-8
from products.netReport.baseReport import BaseReport
class NewConnReport(BaseReport):
    """
        新建连接数报表
    """
    def getNewConnPerfValues(self):
        """
                得到新建连接数性能值
        """
        newConnPerfDatas={}
        for monitorObj in self.monitorObjs:
            newConnPerfValue=self.getMonitorPerfDatas(monitorObj,"Conn","NewConn")
            newConnPerfDatas[monitorObj]=newConnPerfValue
        return newConnPerfDatas

    def getReport(self):
        """
                新建连接数报表
        """
        newConnPerfDatas=self.getNewConnPerfValues()
        topTenNewConns=self.perfTop(newConnPerfDatas)
        avgNewConnTrendValue=self.perfTrendReport(topTenNewConns)
        avgNewConnTrendLineFilePath=self.rgh.makeNewConnTrendGraph(avgNewConnTrendValue,"新建连接数趋向图","avgNewConnTrendLineFilePath")
        [topTenNewConn.pop("datas") for topTenNewConn in topTenNewConns]
        return topTenNewConns,avgNewConnTrendLineFilePath