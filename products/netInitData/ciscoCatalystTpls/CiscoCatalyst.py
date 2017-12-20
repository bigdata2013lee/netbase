#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold

def addCPUDataSource(t):

    ds = SnmpDataSource("CPU")
    ds.set("execCycle", 60)
    
    maxt=MaxThreshold("maxCpu")
    maxt.set("max", 90)
    maxt.set("zname", "最大CPU使用率")
    maxt.set("description","已使用的CPU资源占系统CPU总资源的最大百分比，通常设置为80～90之间")
    maxt.set("format","设备%(title)sCPU使用百分比达到设定的最大值%(max)s")
    
    dp = DataPoint("CPU")
    dp.set("oid", "1.3.6.1.4.1.9.9.109.1.1.1.1.5.1")
    dp.set("type", "GUAGE")
    dp.addThreshold(maxt)
    
    ds.addDataPoint(dp)
    t.addDataSource(ds)
 
def addCpuLoadDataSource(t):

    ds = SnmpDataSource("cpuLoad")
    ds.set("execCycle", 60)
    
    #1分钟负载数据点
    m1dp = DataPoint("1MinLoad")
    m1dp.set("oid", "1.3.6.1.4.1.9.9.109.1.1.1.1.4")
    m1dp.set("type", "GUAGE")
    
    #5分钟CPU负载数据点
    m5dp = DataPoint("5MinLoad")
    m5dp.set("oid", "1.3.6.1.4.1.9.9.109.1.1.1.1.5")
    m5dp.set("type", "GUAGE")
    
    #15分钟CPU负载数据点
    ms5dp = DataPoint("5secLoad")
    ms5dp.set("oid", "1.3.6.1.4.1.9.9.109.1.1.1.1.3")
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
    
    mfdp = DataPoint("memFree")
    mfdp.set("oid", "1.3.6.1.4.1.9.9.48.1.1.1.6.1")
    mfdp.set("type", "GUAGE")
    ds.addDataPoint(mfdp)

    mdp = DataPoint("Mem")
    mdp.set("type", "RPN")
    mdp.set("oid","1.3.6.1.4.1.9.9.48.1.1.1.5.1")
    mdp.set("rpn","value=float(r.value)*100/(float(r.pv('Mem','memFree', 100000))+float(r.value))")
    
    maxt=MaxThreshold("maxMem")
    maxt.set("max", 90)
    maxt.set("zname", "最大内存使用率")
    maxt.set("description","已使用内存占系统总内存的最大百分比，通常设置在80~90之间")
    maxt.set("format","设备%(title)s内存使用百分比达到设定的最大值%(max)s")
    mdp.addThreshold(maxt)
    
    ds.addDataPoint(mdp)
    
    t.addDataSource(ds)
    
def addMemDataSource2(t):
    ds = SnmpDataSource("Mem")
    ds.set("execCycle", 60)
    
    mfdp = DataPoint("memFree")
    mfdp.set("oid", "1.3.6.1.4.1.9.9.109.1.1.1.1.13")
    mfdp.set("type", "GUAGE")
    ds.addDataPoint(mfdp)

    mdp = DataPoint("Mem")
    mdp.set("type", "RPN")
    mdp.set("oid","1.3.6.1.4.1.9.9.109.1.1.1.1.12")
    mdp.set("rpn","value=float(r.value)*100/(float(r.pv('Mem','memFree', 100000))+float(r.value))")
    
    maxt=MaxThreshold("maxMem")
    maxt.set("max", 90)
    maxt.set("zname", "最大内存使用率")
    maxt.set("description","已使用内存占系统总内存的最大百分比，通常设置在80~90之间")
    maxt.set("format","设备%(title)s内存使用百分比达到设定的最大值%(max)s")
    mdp.addThreshold(maxt)
    
    ds.addDataPoint(mdp)
    
    t.addDataSource(ds)
    
def addPsuStatusDataSource(t):
    ds = SnmpDataSource("psuStatus")
    ds.set("execCycle", 60)
    
    dp = DataPoint("psuStatus")
    dp.set("oid", "1.3.6.1.4.1.9.9.13.1.5.1.3.1")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    t.addDataSource(ds)
    
def addPsuStatusDataSource2(t):
    ds = SnmpDataSource("psuStatus")
    ds.set("execCycle", 60)
    
    dp = DataPoint("psuStatus")
    dp.set("oid", "1.3.6.1.4.1.9.9.13.1.5.1.3.1003")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    t.addDataSource(ds)
    
def addFanStatusDataSource(t):
    ds = SnmpDataSource("fanStatus")
    ds.set("execCycle", 60)
    
    dp = DataPoint("fanStatus")
    dp.set("oid", "1.3.6.1.4.1.9.9.13.1.4.1.3.1004")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    t.addDataSource(ds)
    
def addFanStatusDataSource2(t):
    ds = SnmpDataSource("fanStatus")
    ds.set("execCycle", 60)
    
    dp = DataPoint("fanStatus")
    dp.set("oid", "1.3.6.1.4.1.9.9.13.1.4.1.3")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    t.addDataSource(ds)

def addCpuTemDataSource(t):
    ds = SnmpDataSource("cpuTemp")
    ds.set("execCycle", 60)
    
    dp = DataPoint("cpuTemp")
    dp.set("oid", "1.3.6.1.4.1.9.9.13.1.4.1.3.1005")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    t.addDataSource(ds)
      
    
def createCiscoCatalyst2950Tpl():
    t=Template("BaseTpl_CiscoCatalyst_2950")
    t.isBaseTpl = True
    t._saveObj()
    addCPUDataSource(t)
    addPsuStatusDataSource(t)
    addMemDataSource(t)
def createCiscoCatalyst2960Tpl():
    t=Template("BaseTpl_CiscoCatalyst_2960")
    t.isBaseTpl = True
    t._saveObj()
    addCPUDataSource(t)
    addPsuStatusDataSource(t)
    addMemDataSource(t)
    addFanStatusDataSource(t)
def createCiscoCatalyst2960G48Tpl():
    t=Template("BaseTpl_CiscoCatalyst_2960G48")
    t.isBaseTpl = True
    t._saveObj()
    addCPUDataSource(t)
    addPsuStatusDataSource(t)
    addMemDataSource(t)
    addFanStatusDataSource(t)
def createCiscoCatalyst2970Tpl():
    t=Template("BaseTpl_CiscoCatalyst_2970")
    t.isBaseTpl = True
    t._saveObj()
    addCPUDataSource(t)
    addPsuStatusDataSource(t)
    addMemDataSource(t)
def createCiscoCatalyst3750Tpl():
    t=Template("BaseTpl_CiscoCatalyst_3750")
    t.isBaseTpl = True
    t._saveObj() 
    addCPUDataSource(t)
    addPsuStatusDataSource2(t)
    addMemDataSource(t)
    addFanStatusDataSource(t)
    addCpuTemDataSource(t)
def createCiscoCatalyst6500Tpl():
    t=Template("BaseTpl_CiscoCatalyst_6500")
    t.isBaseTpl = True
    t._saveObj() 
    addCpuLoadDataSource(t)
    addMemDataSource2(t)
    addFanStatusDataSource2(t)
def createCiscoCatalyst3500Tpl():
    t=Template("BaseTpl_CiscoCatalyst_3500")
    t.isBaseTpl = True
    t._saveObj() 
    addCpuLoadDataSource(t)
    addMemDataSource(t)
    addPsuStatusDataSource2(t)
    addFanStatusDataSource(t)
    addCpuTemDataSource(t)

def createCiscoCatalystTemplate():
    createCiscoCatalyst2950Tpl()
    """
CPU Usage    1.3.6.1.4.1.9.9.109.1.1.1.1.5.1    //使用的CPU百分比
Mem Used    1.3.6.1.4.1.9.9.48.1.1.1.5.1    //使用的内存，单位unit
Mem Free    1.3.6.1.4.1.9.9.48.1.1.1.6.1    //剩余的内存，单位unit
PSU Status    1.3.6.1.4.1.9.9.13.1.5.1.3.1    //电源状态
"""
    createCiscoCatalyst2960Tpl()
    """
CPU Usage    1.3.6.1.4.1.9.9.109.1.1.1.1.5.1 
Mem Used    1.3.6.1.4.1.9.9.48.1.1.1.5.1
Mem Free    1.3.6.1.4.1.9.9.48.1.1.1.6.1
PSU Status    1.3.6.1.4.1.9.9.13.1.5.1.3.1
FAN Status    1.3.6.1.4.1.9.9.13.1.4.1.3.1004     //风扇状态
"""
    createCiscoCatalyst2960G48Tpl()
    """
CPU Usage    1.3.6.1.4.1.9.9.109.1.1.1.1.5.1
Mem Used    1.3.6.1.4.1.9.9.48.1.1.1.5.1
Mem Free    1.3.6.1.4.1.9.9.48.1.1.1.6.1
PSU Status    1.3.6.1.4.1.9.9.13.1.5.1.3.1
FAN Status    1.3.6.1.4.1.9.9.13.1.4.1.3.1004
"""
    createCiscoCatalyst2970Tpl()
    """
CPU Usage    1.3.6.1.4.1.9.9.109.1.1.1.1.5.1
Mem Used    1.3.6.1.4.1.9.9.48.1.1.1.5.1
Mem Free    1.3.6.1.4.1.9.9.48.1.1.1.6.1
PSU Status    1.3.6.1.4.1.9.9.13.1.5.1.3.1
"""
    createCiscoCatalyst3750Tpl()
    """
CPU Usage    1.3.6.1.4.1.9.9.109.1.1.1.1.5.1 
Mem Used    1.3.6.1.4.1.9.9.48.1.1.1.5.1
Mem Free    1.3.6.1.4.1.9.9.48.1.1.1.6.1
PSU Status    1.3.6.1.4.1.9.9.13.1.5.1.3.1003
CPU Temp    1.3.6.1.4.1.9.9.13.1.3.1.3.1005     //CPU温度
FAN Status     1.3.6.1.4.1.9.9.13.1.4.1.3.1004
"""
    createCiscoCatalyst6500Tpl()
    """
cpmcpuTotal1min    1.3.6.1.4.1.9.9.109.1.1.1.1.4  
cpmcpuTotal5min    1.3.6.1.4.1.9.9.109.1.1.1.1.5
cpmcpuTotal5sec    1.3.6.1.4.1.9.9.109.1.1.1.1.3  //CPU一段时间内负载
MemoryFree    1.3.6.1.4.1.9.9.109.1.1.1.1.13
MemoryUsed     1.3.6.1.4.1.9.9.109.1.1.1.1.12
TemperatureLastShutdown    1.3.6.1.4.1.9.9.13.1.3.1.5
TemperatureStatusValue    1.3.6.1.4.1.9.9.13.1.3.1.3   //温度值
TemperatureState    1.3.6.1.4.1.9.9.13.1.3.1.6    //温度状态
FanState    1.3.6.1.4.1.9.9.13.1.4.1.3
SupplyState    1.3.6.1.4.1.9.9.13.1.5.1.3    //供电状态
"""
    createCiscoCatalyst3500Tpl()
    """
CPUTotal1min     1.3.6.1.4.1.9.9.109.1.1.1.1.4
CPUTotal5min    1.3.6.1.4.1.9.9.109.1.1.1.1.5
CPUTotal5sec    1.3.6.1.4.1.9.9.109.1.1.1.1.3
MemUtilization    1.3.6.1.4.1.9.9.48.1.1.1.5.1
Mem Free    1.3.6.1.4.1.9.9.48.1.1.1.6.1
PSU Status    1.3.6.1.4.1.9.9.13.1.5.1.3.1003
CPU Temp    1.3.6.1.4.1.9.9.13.1.3.1.3.1005
FAN Status     1.3.6.1.4.1.9.9.13.1.4.1.3.1004
"""
    
if __name__=="__main__":
    createCiscoCatalystTemplate()
    