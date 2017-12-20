#coding=utf-8
from products.netReport.baseReport import BaseReport
class MemReport(BaseReport):
    """
        内存报表
    """
    def getMemPerfValues(self):
        """
                得到Mem性能值
        """
        memPerfDatas={}
        for monitorObj in self.monitorObjs:
            memPerfValue=self.getMonitorPerfDatas(monitorObj,"Mem","Mem")
            memPerfDatas[monitorObj]=memPerfValue
        return memPerfDatas

    def getReport(self):
        """
        Mem报表
        """
        memPerfDatas=self.getMemPerfValues()
        topTenMems=self.perfTop(memPerfDatas)
        avgMemTrendValue=self.perfTrendReport(topTenMems)
        avgMemTrendLineFilePath=self.rgh.makeMemTrendGraph(avgMemTrendValue,"内存平均利用率趋向图","avgMemTrendLineFilePath")
        [topTenMem.pop("datas") for topTenMem in topTenMems]
        return topTenMems,avgMemTrendLineFilePath
        
        
        
        