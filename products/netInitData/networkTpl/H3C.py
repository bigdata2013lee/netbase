#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold
"""
CpuUsedPerc    CpuUsedPerc_CpuUsedPerc    1.3.6.1.4.1.2011.10.2.6.1.1.1.1.6.7//CPU 使用率
MemoryTotal    MemoryTotal_MemoryTotal    1.3.6.1.4.1.2011.10.2.6.1.1.1.1.10.7//总内存
MemoryUsedPerc    MemoryUsedPerc_MemoryUsedPerc    1.3.6.1.4.1.2011.10.2.6.1.1.1.1.8.7//内存使用率
Temperature    Temperature_Temperature    1.3.6.1.4.1.2011.10.2.6.1.1.1.1.12.1//温度
UpTemperature    UpTemperature_UpTemperature    1.3.6.1.4.1.2011.10.2.6.1.1.1.1.13.1
"""
def addTempDataSource(t):
    ds = SnmpDataSource("Temp")
    ds.set("execCycle", 60)
    
    dp1 = DataPoint("CPU")
    dp1.set("oid", "1.3.6.1.4.1.2011.10.2.6.1.1.1.1.12.1")
    dp1.set("type", "GUAGE")
    ds.addDataPoint(dp1)
    
    dp2 = DataPoint("CPU")
    dp2.set("oid", "1.3.6.1.4.1.2011.10.2.6.1.1.1.1.13.1")
    dp2.set("type", "GUAGE")
    ds.addDataPoint(dp2)
    
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
    dp.set("oid", "1.3.6.1.4.1.2011.10.2.6.1.1.1.1.6.7")
    dp.set("type", "GUAGE")
    dp.addThreshold(maxt)
    
    ds.addDataPoint(dp)
    
    t.addDataSource(ds)

def addMemDataSource(t):
    ds = SnmpDataSource("Mem")
    ds.set("execCycle", 60)
    
    mfdp = DataPoint("memTotal")
    mfdp.set("oid", "1.3.6.1.4.1.2011.10.2.6.1.1.1.1.10.7")
    mfdp.set("type", "GUAGE")
    ds.addDataPoint(mfdp)

    mdp = DataPoint("Mem")
    mdp.set("type", "GUAGE")
    mdp.set("oid","1.3.6.1.4.1.2011.10.2.6.1.1.1.1.8.7")
    
    maxt=MaxThreshold("maxMem")
    maxt.set("max", 90)
    maxt.set("zname", "最大内存使用率")
    maxt.set("description","已使用内存占系统总内存的最大百分比，通常设置在80~90之间")
    maxt.set("format","设备%(title)s内存使用百分比达到设定的最大值%(max)s")
    mdp.addThreshold(maxt)
    
    ds.addDataPoint(mdp)
    
    t.addDataSource(ds)
    
def createH3CTpl():
    t=Template("BaseTpl_H3C")
    t.isBaseTpl = True
    t._saveObj()
    addMemDataSource(t)
    addCPUDataSource(t)
    addTempDataSource(t)
    
if __name__=="__main__":
    createH3CTpl()