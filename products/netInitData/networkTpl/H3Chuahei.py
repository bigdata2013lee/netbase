#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold
"""
hw:hardware，即硬件
cpu    CPU近5秒利用率 %    1.3.6.1.4.1.2011.6.1.1.1.2.65536                     //CPU5秒钟利用率
    hwCpuCostRatePer1Min %    1.3.6.1.4.1.2011.6.1.1.1.3.65536 //CPU1分钟利用率
    hwCpuCostRatePer5Min %    1.3.6.1.4.1.2011.6.1.1.1.4.65536 //CPU5分钟利用率
        
MemoryUtilization    hwMemSize Bytes    1.3.6.1.4.1.2011.6.1.2.1.1.2.65536 //硬件总内存
    hwMemFree Bytes    1.3.6.1.4.1.2011.6.1.2.1.1.3.65536//硬件剩余内存
    h3cEntityExtMemUsage %    1.3.6.1.4.1.2011.10.2.6.1.1.1.1.8.65536//实体分机内存使用
"""
def addMemDataSource(t):
    ds = SnmpDataSource("Mem")
    ds.set("execCycle", 60)
    
    mfdp = DataPoint("memFree")
    mfdp.set("oid", "1.3.6.1.4.1.2011.6.1.2.1.1.3.65536")
    mfdp.set("type", "GUAGE")
    ds.addDataPoint(mfdp)
    
    dp = DataPoint("h3cEntityExtMemUsage")
    dp.set("oid", "1.3.6.1.4.1.2011.10.2.6.1.1.1.1.8.65536")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)

    mdp = DataPoint("Mem")
    mdp.set("type", "RPN")
    mdp.set("oid","1.3.6.1.4.1.2011.6.1.2.1.1.2.65536")
    mdp.set("rpn","value=float(r.value)*100/(float(r.pv('Mem','memFree', 100000))+float(r.value))")
    
    maxt=MaxThreshold("maxMem")
    maxt.set("max", 90)
    maxt.set("zname", "最大内存使用率")
    maxt.set("description","已使用内存占系统总内存的最大百分比，通常设置在80~90之间")
    maxt.set("format","设备%(title)s内存使用百分比达到设定的最大值%(max)s")
    mdp.addThreshold(maxt)
    
    ds.addDataPoint(mdp)
    
    t.addDataSource(ds)
def addCPUDataSource(t):

    ds = SnmpDataSource("CPU")
    ds.set("execCycle", 60)
    
    maxt=MaxThreshold("maxCpu")
    maxt.set("max", 90)
    maxt.set("zname", "最大CPU使用率")
    maxt.set("description","已使用的CPU资源占系统CPU总资源的最大百分比，通常设置为80～90之间")
    maxt.set("format","设备%(title)sCPU使用百分比达到设定的最大值%(max)s")
    
    dp = DataPoint("CPU")
    dp.set("oid", "1.3.6.1.4.1.2011.6.1.1.1.2.65536")
    dp.set("type", "GUAGE")
    dp.addThreshold(maxt)
    
    ds.addDataPoint(dp)
    
    dp2 = DataPoint("CPUPer1Min")
    dp2.set("oid", "1.3.6.1.4.1.2011.6.1.1.1.3.65536")
    dp2.set("type", "GUAGE")
    ds.addDataPoint(dp2)
    
    dp3 = DataPoint("CPUPer5Min")
    dp3.set("oid", "1.3.6.1.4.1.2011.6.1.1.1.4.65536")
    dp3.set("type", "GUAGE")
    ds.addDataPoint(dp3)
    
    t.addDataSource(ds)
    
def createH3ChuaheiTpl():
    t=Template("BaseTpl_H3Chuahei")
    t.isBaseTpl = True
    t._saveObj()
    addCPUDataSource(t)
    addMemDataSource(t)
    
if __name__=="__main__":
    createH3ChuaheiTpl()