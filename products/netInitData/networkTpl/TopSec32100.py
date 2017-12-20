#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold, MinThreshold, RangeThreshold
"""
load：负载
connPerSecond    connPerSecond_connPerSecond    1.3.6.1.4.1.14331.5.5.1.4.6.0//平均每秒的连接数
cpuLoad    cpuLoad_cpuLoad    1.3.6.1.4.1.14331.5.5.1.4.2.0//CPU负载
currentConnection    currentConnection_currentConnection    1.3.6.1.4.1.14331.5.5.1.4.5.0//当前连接数
//memoryLoad    memoryLoad_memoryLoad    1.3.6.1.4.1.14331.5.5.1.4.3.0//内存负载
"""
def addCPUDataSource(t):

    ds = SnmpDataSource("CPU")
    ds.set("execCycle", 60)
    
    maxt = MaxThreshold("maxCpu")
    maxt.set("max", 90)
    maxt.set("zname", "最大CPU使用率")
    maxt.set("description", "已使用的CPU资源占系统CPU总资源的最大百分比，通常设置为80～90之间")
    maxt.set("format", "设备%(title)sCPU使用百分比达到设定的最大值%(max)s")
    
    dp = DataPoint("CPU")
    dp.set("oid", "1.3.6.1.4.1.14331.5.5.1.4.2.0")
    dp.set("type", "GUAGE")
    dp.addThreshold(maxt)
    
    ds.addDataPoint(dp)
    t.addDataSource(ds)

def addMemDataSource(t):
    ds = SnmpDataSource("Mem")
    ds.set("execCycle", 60)
    

    mdp = DataPoint("Mem")
    mdp.set("type", "GUAGE")
    mdp.set("oid", "1.3.6.1.4.1.14331.5.5.1.4.3.0")
    
    maxt = MaxThreshold("maxMem")
    maxt.set("max", 90)
    maxt.set("zname", "最大内存使用率")
    maxt.set("description", "已使用内存占系统总内存的最大百分比，通常设置在80~90之间")
    maxt.set("format", "设备%(title)s内存使用百分比达到设定的最大值%(max)s")
    mdp.addThreshold(maxt)
    
    ds.addDataPoint(mdp)
    t.addDataSource(ds)

def addConnDataSource(t):
    ds = SnmpDataSource("Conn")
    ds.set("execCycle", 60)
    
    dp = DataPoint("connPerSec")
    dp.set("type", "GUAGE")
    dp.set("oid", "1.3.6.1.4.1.14331.5.5.1.4.6.0")
    ds.addDataPoint(dp)

    mdp = DataPoint("CurConn")
    mdp.set("type", "GUAGE")
    mdp.set("oid", "1.3.6.1.4.1.14331.5.5.1.4.5.0")
    
    maxt = MaxThreshold("maxConn")
    maxt.set("max", 90)
    maxt.set("zname", "最大连接数")
    maxt.set("description", "当前连接数最大值")
    maxt.set("format", "设备%(title)s最大连接数达到设定的最大值%(max)s")
    mdp.addThreshold(maxt)
    
    ds.addDataPoint(mdp)
    t.addDataSource(ds)
    
def createTopSec32100Tpl():
    t=Template("BaseTpl_TopSec32100")
    t.isBaseTpl = True
    t._saveObj()
    addCPUDataSource(t)
    addMemDataSource(t)
    addConnDataSource(t)
       
if __name__=="__main__":
    createTopSec32100Tpl()