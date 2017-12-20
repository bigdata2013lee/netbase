#coding=utf-8
from products.netReport.baseReport import BaseReport
class CpuReport(BaseReport):
    """
    CPU报表
    """
    def getCpuPerfValues(self):
        """
                得到CPU性能值
        """
        cpuPerfDatas={}
        for monitorObj in self.monitorObjs:
            cpuPerfValue=self.getMonitorPerfDatas(monitorObj,"CPU","CPU")
            cpuPerfDatas[monitorObj]=cpuPerfValue
        return cpuPerfDatas

    def getReport(self):
        """
        CPU报表
        """
        cpuPerfDatas=self.getCpuPerfValues()
        topTenCpus=self.perfTop(cpuPerfDatas)
        avgCpuTrendValue=self.perfTrendReport(topTenCpus)
        avgCpuTrendLineFilePath=self.rgh.makeCPUTrendGraph(avgCpuTrendValue,"CPU平均利用率趋向图","avgCpuTrendLineFilePath")
        [topTenCpu.pop("datas") for topTenCpu in topTenCpus]
        return topTenCpus,avgCpuTrendLineFilePath
        
        
        
        