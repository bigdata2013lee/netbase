#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold
""""
CpuUsedPerc         1.3.6.1.4.1.2011.6.1.1.1.4.0 //CPU使用率
Fan_value         1.3.6.1.4.1.2011.2.23.1.9.1.1.1.2.1 //风扇数据
MemoryTotal         1.3.6.1.4.1.2011.6.1.2.1.1.2.1 //总内存
MemoryAvgPerc         1.3.6.1.4.1.2011.6.1.2.1.1.2.2 //一段时间内平均使用内存
PowerSupplyStatus         1.3.6.1.4.1.2011.2.23.1.9.1.2.1.2.1 //供电状态
TemperatureStatus         1.3.6.1.4.1.2011.2.23.1.9.1.3.1.2.0.0.1 //温度状态
TemperatureValue         1.3.6.1.4.1.2011.2.23.1.9.1.3.1.3.0.0.1 //温度值
UpTemperature         1.3.6.1.4.1.2011.2.23.1.9.1.3.1.2.0.1.1 
cpu1         1.3.6.1.4.1.2011.6.1.1.1.4.1 //cpu1
cpu2         1.3.6.1.4.1.2011.6.1.1.1.4.2 //cpu2
fan_status         1.3.6.1.4.1.2011.2.23.1.9.1.1.1.1.1//风扇状态
"""
def addCPUDataSource(t):

    ds = SnmpDataSource("CPU")
    ds.set("execCycle", 60)
    
    maxt=MaxThreshold("maxCpu")
    maxt.set("max", 90)
    maxt.set("zname", "最大CPU使用率")
    maxt.set("description","已使用的CPU资源占系统CPU总资源的最大百分比，通常设置为80～90之间")
    maxt.set("format","设备%(title)sCPU使用百分比达到设定的最大值%(max)s")
    
    dp = DataPoint("CPU")
    dp.set("oid", "1.3.6.1.4.1.2011.6.1.1.1.4.0")
    dp.set("type", "GUAGE")
    dp.addThreshold(maxt)
    
    ds.addDataPoint(dp)
    
    dp2 = DataPoint("cpu1")
    dp2.set("oid", "1.3.6.1.4.1.2011.6.1.1.1.4.1")
    dp2.set("type", "GUAGE")
    ds.addDataPoint(dp2)
    
    dp3 = DataPoint("cpu2")
    dp3.set("oid", "1.3.6.1.4.1.2011.6.1.1.1.4.2")
    dp3.set("type", "GUAGE")
    ds.addDataPoint(dp3)
    
    t.addDataSource(ds)

def addMemDataSource(t):
    ds = SnmpDataSource("Mem")
    ds.set("execCycle", 60)
    
    mfdp = DataPoint("memTotal")
    mfdp.set("oid", "1.3.6.1.4.1.2011.6.1.2.1.1.2.1")
    mfdp.set("type", "GUAGE")
    ds.addDataPoint(mfdp)

    mdp = DataPoint("Mem")
    mdp.set("type", "RPN")
    mdp.set("oid","1.3.6.1.4.1.2011.6.1.2.1.1.2.2")
    mdp.set("rpn","value=float(r.value)*100/(float(r.pv('Mem','memTotal', 100000)))")
    
    maxt=MaxThreshold("maxMem")
    maxt.set("max", 90)
    maxt.set("zname", "最大内存使用率")
    maxt.set("description","已使用内存占系统总内存的最大百分比，通常设置在80~90之间")
    maxt.set("format","设备%(title)s内存使用百分比达到设定的最大值%(max)s")
    mdp.addThreshold(maxt)
    
    ds.addDataPoint(mdp)
    
    t.addDataSource(ds)
    
def addPowerSupplyDataSource(t):
    ds = SnmpDataSource("PowerSupply")
    ds.set("execCycle", 60)
    
    dp1 = DataPoint("PowerSupplyStatus")
    dp1.set("oid", "1.3.6.1.4.1.2011.2.23.1.9.1.2.1.2.1")
    dp1.set("type", "GUAGE")
    ds.addDataPoint(dp1)
    
    t.addDataSource(ds)
    
def addFanDataSource(t):
    ds = SnmpDataSource("Fan")
    ds.set("execCycle", 60)
    
    dp1 = DataPoint("fan_status")
    dp1.set("oid", "1.3.6.1.4.1.2011.2.23.1.9.1.1.1.1.1")
    dp1.set("type", "GUAGE")
    ds.addDataPoint(dp1)
    
    t.addDataSource(ds)
    
def addTempDataSource(t):
    ds = SnmpDataSource("Temp")
    ds.set("execCycle", 60)
    
    dp1 = DataPoint("Temperature")
    dp1.set("oid", "1.3.6.1.4.1.2011.2.23.1.9.1.3.1.3.0.0.1")
    dp1.set("type", "GUAGE")
    ds.addDataPoint(dp1)
    
    dp2 = DataPoint("TemperatureStatus")
    dp2.set("oid", "1.3.6.1.4.1.2011.2.23.1.9.1.3.1.2.0.0.1")
    dp2.set("type", "GUAGE")
    ds.addDataPoint(dp2)
    
    dp3 = DataPoint("UpTemperature")
    dp3.set("oid", "1.3.6.1.4.1.2011.2.23.1.9.1.3.1.2.0.1.1")
    dp3.set("type", "GUAGE")
    ds.addDataPoint(dp3)

    t.addDataSource(ds)

def createH3C_S9505Tpl():
    t=Template("BaseTpl_H3C_S9505")
    t.isBaseTpl = True
    t._saveObj()
    addTempDataSource(t)
    addFanDataSource(t)
    addPowerSupplyDataSource(t)
    addMemDataSource(t)
    addCPUDataSource(t)
    
if __name__=="__main__":
    createH3C_S9505Tpl()
