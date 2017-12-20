#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold
"""
cpuused    cpuused_cpuused    1.3.6.1.4.1.2011.2.2.4.12.0//CPU使用率
//memused    memused_memused    1.3.6.1.4.1.2011.2.2.5.1.0//内存使用
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
    dp.set("oid", "1.3.6.1.4.1.2011.2.2.4.12.0")
    dp.set("type", "GUAGE")
    dp.addThreshold(maxt)
    
    ds.addDataPoint(dp)
    t.addDataSource(ds)
    
def addMemDataSource(t):
    ds = SnmpDataSource("Mem")
    ds.set("execCycle", 60)

    mdp = DataPoint("Mem")
    mdp.set("type", "GUAGE")
    mdp.set("oid","1.3.6.1.4.1.2011.2.2.5.1.0")
    
    maxt=MaxThreshold("maxMem")
    maxt.set("max", 90)
    maxt.set("zname", "最大内存使用率")
    maxt.set("description","已使用内存占系统总内存的最大百分比，通常设置在80~90之间")
    maxt.set("format","设备%(title)s内存使用百分比达到设定的最大值%(max)s")
    mdp.addThreshold(maxt)
    
    ds.addDataPoint(mdp)
    
    t.addDataSource(ds)
    
def createHuaWeiARRouterTpl():
    t=Template("BaseTpl_HuaWeiARRouter")
    t.isBaseTpl = True
    t._saveObj()
    addCPUDataSource(t)
    addMemDataSource(t)
       
if __name__=="__main__":
    createHuaWeiARRouterTpl()