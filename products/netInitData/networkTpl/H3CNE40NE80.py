#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold
"""
CpuUtilization_huawei        1.3.6.1.4.1.2011.5.25.31.1.1.1.1.5//CPU使用率
CpuUsageThreshold        1.3.6.1.4.1.2011.5.25.31.1.1.1.1.6//CPU使用率阀值
MemoryUtilization        1.3.6.1.4.1.2011.5.25.31.1.1.1.1.7//内存使用，不能计算内存使用百分比
UsageThreshold        1.3.6.1.4.1.2011.5.25.31.1.1.1.1.8//内存使用阀值
TemperatureValue        1.3.6.1.4.1.2011.5.25.31.1.1.1.1.11//温度值
hwEntitypowerVoltage        1.3.6.1.4.1.2011.5.25.31.1.1.1.1.13//硬件实体电源电压
"""
def addTempDataSource(t):
    ds = SnmpDataSource("Temp")
    ds.set("execCycle", 60)
    
    dp = DataPoint("Temperature")
    dp.set("oid", "1.3.6.1.4.1.2011.5.25.31.1.1.1.1.11")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    t.addDataSource(ds)
    
def addHwDataSource(t):
    ds = SnmpDataSource("hw")
    ds.set("execCycle", 60)
    
    dp = DataPoint("hwEntitypowerVoltage")
    dp.set("oid", "1.3.6.1.4.1.2011.5.25.31.1.1.1.1.13")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
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
    dp.set("oid", "1.3.6.1.4.1.2011.5.25.31.1.1.1.1.5")
    dp.set("type", "GUAGE")
    dp.addThreshold(maxt)
    
    ds.addDataPoint(dp)
    t.addDataSource(ds)
    
def addMemDataSource(t):
    ds = SnmpDataSource("Mem")
    ds.set("execCycle", 60)

    mdp = DataPoint("Mem")
    mdp.set("type", "GUAGE")
    mdp.set("oid","1.3.6.1.4.1.2011.5.25.31.1.1.1.1.7")
    
    maxt=MaxThreshold("maxMem")
    maxt.set("max", 90)
    maxt.set("zname", "最大内存使用率")
    maxt.set("description","已使用内存占系统总内存的最大百分比，通常设置在80~90之间")
    maxt.set("format","设备%(title)s内存使用百分比达到设定的最大值%(max)s")
    mdp.addThreshold(maxt)
    
    ds.addDataPoint(mdp)
    
    t.addDataSource(ds)
 
def createH3CNE40NE80Tpl():
    t=Template("BaseTpl_H3CNE40NE80")
    t.isBaseTpl = True
    t._saveObj()
    addMemDataSource(t)
    addCPUDataSource(t)
    addHwDataSource(t)
    addTempDataSource(t)
    
if __name__=="__main__":
    createH3CNE40NE80Tpl()