#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold
"""
cpu 利用率        1.3.6.1.4.1.28557.2.2.1.3
        
memory 总数        1.3.6.1.4.1.28557.2.2.1.4
        
当前已用的memory        1.3.6.1.4.1.28557.2.2.1.5
        
系统支持的最大session 数        1.3.6.1.4.1.28557.2.2.1.6
        
当前建立的session 数        1.3.6.1.4.1.28557.2.2.1.7
        
sysHAStatus        1.3.6.1.4.1.28557.2.2.1.8 //可用性状态
"""
def addSessionDataSource(t):

    ds = SnmpDataSource("Conn")
    ds.set("execCycle", 60)
    
    dp = DataPoint("CurConn")
    dp.set("type", "GUAGE")
    dp.set("oid", "1.3.6.1.4.1.28557.2.2.1.7")
    ds.addDataPoint(dp)
    
    mdp = DataPoint("maxConn")
    mdp.set("type", "GUAGE")
    mdp.set("oid", " 1.3.6.1.4.1.28557.2.2.1.6")
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
    dp.set("oid", "1.3.6.1.4.1.28557.2.2.1.3")
    dp.set("type", "GUAGE")
    dp.addThreshold(maxt)
    
    ds.addDataPoint(dp)
    t.addDataSource(ds)
    
def addMemDataSource(t):
    ds = SnmpDataSource("Mem")
    ds.set("execCycle", 60)
    
    mfdp = DataPoint("totalMem")
    mfdp.set("oid", " 1.3.6.1.4.1.28557.2.2.1.4")
    mfdp.set("type", "GUAGE")
    ds.addDataPoint(mfdp)

    mdp = DataPoint("Mem")
    mdp.set("type", "RPN")
    mdp.set("oid","1.3.6.1.4.1.28557.2.2.1.5")
    mdp.set("rpn","value=100-(float(r.value)*100/(float(r.pv('Mem','totalMem', 100000)))")
    
    maxt=MaxThreshold("maxMem")
    maxt.set("max", 90)
    maxt.set("zname", "最大内存使用率")
    maxt.set("description","已使用内存占系统总内存的最大百分比，通常设置在80~90之间")
    maxt.set("format","设备%(title)s内存使用百分比达到设定的最大值%(max)s")
    mdp.addThreshold(maxt)
    
    ds.addDataPoint(mdp)
    
    t.addDataSource(ds)
    
def addsysHAStatusDataSource(t):
    ds = SnmpDataSource("sysHAStatus")
    ds.set("execCycle", 60)
    
    dp = DataPoint("sysHAStatus")
    dp.set("oid", "1.3.6.1.4.1.28557.2.2.1.8")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    t.addDataSource(ds)
    
def createHILLSTONETpl():
    t=Template("BaseTpl_HILLSTONE")
    t.isBaseTpl = True
    t._saveObj()
    addsysHAStatusDataSource(t)
    addSessionDataSource(t)
    addMemDataSource(t)
    addCPUDataSource(t)
       
if __name__=="__main__":
    createHILLSTONETpl()