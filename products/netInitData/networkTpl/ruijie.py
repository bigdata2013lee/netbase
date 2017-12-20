#coding=utf-8
#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold
"""
Utilization:使用，利用
CPU 占用率：    平均5秒    1.3.6.1.4.1.4881.1.1.10.2.36.1.1.1.O  //平均5秒钟使用率
    平均1分    1.3.6.1.4.1.4881.1.1.10.2.36.1.1.2.O        //平均1分钟使用率
    平均5分    1.3.6.1.4.1.4881.1.1.10.2.36.1.1.3.O        //平均5分钟使用率
        
//MEMORY 占用率        
SYSMEM    CurrentUtilization    1.3.6.1.4.1.4881.1.1.10.2.35.1.1.1.3.1 //当前占用率
     LowestUtilization    1.3.6.1.4.1.4881.1.1.10.2.35.1.1.1.4.1   //最低占用率
    LargestUtilization    1.3.6.1.4.1.4881.1.1.10.2.35.1.1.1.5.1//最高占用率
        
large pa     CurrentUtilization    1.3.6.1.4.1.4881.1.1.10.2.35.1.1.1.3.2
    LowestUtilization    1.3.6.1.4.1.4881.1.1.10.2.35.1.1.1.4.2
"""

def addCpuLoadDataSource(t):

    ds = SnmpDataSource("cpuLoad")
    ds.set("execCycle", 60)
    
    #1分钟负载数据点
    m1dp = DataPoint("1MinLoad")
    m1dp.set("oid", "1.3.6.1.4.1.4881.1.1.10.2.36.1.1.2.O")
    m1dp.set("type", "GUAGE")
    
    #5分钟CPU负载数据点
    m5dp = DataPoint("5MinLoad")
    m5dp.set("oid", "1.3.6.1.4.1.4881.1.1.10.2.36.1.1.3.O")
    m5dp.set("type", "GUAGE")
    
    #5secCPU负载数据点
    ms5dp = DataPoint("5secLoad")
    ms5dp.set("oid", "1.3.6.1.4.1.4881.1.1.10.2.36.1.1.1.O")
    ms5dp.set("type", "GUAGE")
        
    maxt=MaxThreshold("maxLoad")
    maxt.set("max", 0.9)
    maxt.set("zname", "CPU最大负载")
    maxt.set("description","一段时间内CPU的负载值的最大限制")
    maxt.set("format","设备%(title)sCPU达到最大负载%(max)s")
    
    m5dp.addThreshold(maxt)
    
    ds.addDataPoint(m1dp)
    ds.addDataPoint(m5dp)
    ds.addDataPoint(ms5dp)
    
    t.addDataSource(ds)
    
def addMemDataSource(t):
    ds = SnmpDataSource("Mem")
    ds.set("execCycle", 60)
    
    ldp = DataPoint("lowestMem")
    ldp.set("oid", "1.3.6.1.4.1.4881.1.1.10.2.35.1.1.1.4.1")
    ldp.set("type", "GUAGE")
    ds.addDataPoint(ldp)
    
    dp = DataPoint("largesMem")
    dp.set("oid", "1.3.6.1.4.1.4881.1.1.10.2.35.1.1.1.5.1")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)

    mdp = DataPoint("Mem")
    mdp.set("type", "GUAGE")
    mdp.set("oid","1.3.6.1.4.1.4881.1.1.10.2.35.1.1.1.3.1")
    
    maxt=MaxThreshold("maxMem")
    maxt.set("max", 90)
    maxt.set("zname", "最大内存使用率")
    maxt.set("description","已使用内存占系统总内存的最大百分比，通常设置在80~90之间")
    maxt.set("format","设备%(title)s内存使用百分比达到设定的最大值%(max)s")
    mdp.addThreshold(maxt)
    
    ds.addDataPoint(mdp)
    
    t.addDataSource(ds)

def addPaDataSource(t):
    
    ds = SnmpDataSource("Pa")
    ds.set("execCycle", 60)
    
    ldp = DataPoint("currentPa")
    ldp.set("oid", "1.3.6.1.4.1.4881.1.1.10.2.35.1.1.1.3.2")
    ldp.set("type", "GUAGE")
    ds.addDataPoint(ldp)
    
    dp = DataPoint("lowestPa")
    dp.set("oid", "1.3.6.1.4.1.4881.1.1.10.2.35.1.1.1.4.2")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    
    t.addDataSource(ds)
def createRuijieTpl():
    t=Template("BaseTpl_Ruijie")
    t.isBaseTpl = True
    t._saveObj()
    addCpuLoadDataSource(t)
    addMemDataSource(t)
    addPaDataSource(t)
       
if __name__=="__main__":
    createRuijieTpl()