#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold
"""
heap:堆
//Memory    Memory_Memory    1.3.6.1.4.1.2636.3.1.13.1.11.9.1.0.0 //使用的内存
jnxFruTemp    jnxFruTemp_jnxFruTemp    1.3.6.1.4.1.2636.3.1.15.1.9.9.1.0.0 //温度
jnxFwddHeapUsage    jnxFwddHeapUsage_jnxFwddHeapUsage    1.3.6.1.4.1.2636.3.34.1.3.0 //堆使用率
jnxFwddRtThreadsCPUUsage    jnxFwddRtThreadsCPUUsage_jnxFwddRtThreadsCPUUsage    1.3.6.1.4.1.2636.3.34.1.2.0
jnxHrStoragePercentUsed    jnxHrStoragePercentUsed_jnxHrStoragePercentUsed    1.3.6.1.4.1.2636.3.31.1.1.1.1.1
jnxOperatingCPU    jnxOperatingCPU_jnxOperatingCPU    1.3.6.1.4.1.2636.3.1.13.1.8.9.1.0.0 //CPU运作
jnxOperatingHeap    jnxOperatingHeap_jnxOperatingHeap    1.3.6.1.4.1.2636.3.1.13.1.12.1.1.0.0 //堆运作
jnxOperatingTemp    jnxOperatingTemp_jnxOperatingTemp    1.3.6.1.4.1.2636.3.1.13.1.7.9.1.0.0//温度
"""
def addTempDataSource(t):
    
    ds = SnmpDataSource("Temp")
    ds.set("execCycle", 60)
    
    ndp = DataPoint("FruTemp")
    ndp.set("oid", "1.3.6.1.4.1.2636.3.1.15.1.9.9.1.0.0")
    ndp.set("type", "GUAGE")
    ds.addDataPoint(ndp)
    
    dp = DataPoint("OperatingTemp")
    dp.set("oid", "1.3.6.1.4.1.2636.3.1.13.1.7.9.1.0.0")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    
    t.addDataSource(ds)
    
def addHeapDataSource(t):

    ds = SnmpDataSource("Heap")
    ds.set("execCycle", 60)
    
    ndp = DataPoint("FwddHeap")
    ndp.set("oid", "1.3.6.1.4.1.2636.3.34.1.3.0")
    ndp.set("type", "GUAGE")
    ds.addDataPoint(ndp)
    
    dp = DataPoint("OperatingHeap")
    dp.set("oid", "1.3.6.1.4.1.2636.3.1.13.1.12.1.1.0.0")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    
    t.addDataSource(ds)
    
def addCPUDataSource(t):

    ds = SnmpDataSource("CPU")
    ds.set("execCycle", 60)
    
    ndp = DataPoint("CPU")
    ndp.set("oid", "1.3.6.1.4.1.2636.3.34.1.2.0")
    ndp.set("type", "GUAGE")
    ds.addDataPoint(ndp)
    
    maxt=MaxThreshold("maxCpu")
    maxt.set("max", 90)
    maxt.set("zname", "最大CPU使用率")
    maxt.set("description","已使用的CPU资源占系统CPU总资源的最大百分比，通常设置为80～90之间")
    maxt.set("format","设备%(title)sCPU使用百分比达到设定的最大值%(max)s")
    
    dp = DataPoint("CPU")
    dp.set("oid", "1.3.6.1.4.1.2636.3.1.13.1.8.9.1.0.0")
    dp.set("type", "GUAGE")
    dp.addThreshold(maxt)
    
    ds.addDataPoint(dp)
    t.addDataSource(ds)
    
def addMemDataSource(t):
    ds = SnmpDataSource("Mem")
    ds.set("execCycle", 60)

    mdp = DataPoint("Mem")
    mdp.set("type", "GUAGE")
    mdp.set("oid","1.3.6.1.4.1.2636.3.1.13.1.11.9.1.0.0")
    
    maxt=MaxThreshold("maxMem")
    maxt.set("max", 90)
    maxt.set("zname", "最大内存使用率")
    maxt.set("description","已使用内存占系统总内存的最大百分比，通常设置在80~90之间")
    maxt.set("format","设备%(title)s内存使用百分比达到设定的最大值%(max)s")
    mdp.addThreshold(maxt)
    
    ds.addDataPoint(mdp)
    
    t.addDataSource(ds)
    
def createJuniper_J_SeriesTpl():
    t=Template("BaseTpl_Juniper_J_Series")
    t.isBaseTpl = True
    t._saveObj()
    addTempDataSource(t)
    addHeapDataSource(t)
    addCPUDataSource(t)
    addMemDataSource(t)
if __name__=="__main__":
    createJuniper_J_SeriesTpl()