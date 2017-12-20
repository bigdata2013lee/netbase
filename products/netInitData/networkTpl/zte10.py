#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold
"""
cpu在两分中内使用率        1.3.6.1.4.1.3902.3.3.1.1.5
        
cpu在五秒钟的使用率        1.3.6.1.4.1.3902.3.3.1.1.6
        
cpu在三十秒钟的使用率        1.3.6.1.4.1.3902.3.3.1.1.7
        
cpu在三十秒钟的最高使用率        1.3.6.1.4.1.3902.3.3.1.1.8
        
单元所有的物理内存大小        1.3.6.1.4.1.3902.3.3.1.1.3
        
PowerStatus        1.3.6.1.4.1.3902.3.200.2.1.2  //电源状态
        
FanStatus        1.3.6.1.4.1.3902.3.200.1.1.2    //风扇状态
        
        
Temperature        1.3.6.1.4.1.3902.3.200.2.1.3.2 //温度
"""
def addDiskMemDataSource(t):
    ds = SnmpDataSource("Disk")
    ds.set("execCycle", 60)
    
    dp = DataPoint("diskTotal")
    dp.set("oid", "1.3.6.1.4.1.3902.3.3.1.1.3")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    
    t.addDataSource(ds)
    
def addPowerStatusDataSource(t):
    ds = SnmpDataSource("powerStatus")
    ds.set("execCycle", 60)
    
    dp = DataPoint("powerStatus")
    dp.set("oid", "1.3.6.1.4.1.3902.3.200.2.1.2")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    t.addDataSource(ds)

def addTemperatureDataSource(t):
    ds = SnmpDataSource("temperature")
    ds.set("execCycle", 60)
    
    dp = DataPoint("temperature")
    dp.set("oid", "1.3.6.1.4.1.3902.3.200.2.1.3.2")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    t.addDataSource(ds)
    
def addFanStatusDataSource(t):
    ds = SnmpDataSource("fanStatus")
    ds.set("execCycle", 60)
    
    dp = DataPoint("fanStatus")
    dp.set("oid", "1.3.6.1.4.1.3902.3.200.1.1.2")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    t.addDataSource(ds)  
    
def addCpuLoadDataSource(t):

    ds = SnmpDataSource("cpuLoad")
    ds.set("execCycle", 60)
    
    m1dp = DataPoint("2MinLoad")
    m1dp.set("oid", " 1.3.6.1.4.1.3902.3.3.1.1.5")
    m1dp.set("type", "GUAGE")
    
    m5dp = DataPoint("30secLoad")
    m5dp.set("oid", " 1.3.6.1.4.1.3902.3.3.1.1.7")
    m5dp.set("type", "GUAGE")
    
    ms5dp = DataPoint("5secLoad")
    ms5dp.set("oid", "1.3.6.1.4.1.3902.3.3.1.1.6")
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
    
def createZTE10Tpl():
    t=Template("BaseTpl_ZTE10")
    t.isBaseTpl = True
    t._saveObj()
    addCpuLoadDataSource(t)
    addFanStatusDataSource(t)
    addDiskMemDataSource(t)
    addTemperatureDataSource(t)
    addPowerStatusDataSource(t)
       
if __name__=="__main__":
    createZTE10Tpl()