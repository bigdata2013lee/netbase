#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold
"""
session ：会话
CPUload5s      1.3.6.1.4.1.89.35.1.112  //CPU5秒钟负载
    
CPUload60s      1.3.6.1.4.1.89.35.1.113 //CPU60秒钟负载
    
LastHttpSession    1.3.6.1.4.1.89.35.1.40.29.20.1.19 //最近一次http会话
    
TotalHttpSession    1.3.6.1.4.1.89.35.1.40.29.20.1.18 //总的http会话
    
 newConnection      1.3.6.1.4.1.89.35.1.40.29.23.1.4 //新建连接数
"""

def addCpuLoadDataSource(t):

    ds = SnmpDataSource("cpuLoad")
    ds.set("execCycle", 60)
    
    #1分钟负载数据点
    m1dp = DataPoint("1MinLoad")
    m1dp.set("oid", "1.3.6.1.4.1.89.35.1.113")
    m1dp.set("type", "GUAGE")
    
    #5secCPU负载数据点
    ms5dp = DataPoint("5secLoad")
    ms5dp.set("oid", "1.3.6.1.4.1.89.35.1.112")
    ms5dp.set("type", "GUAGE")
        
    maxt=MaxThreshold("maxLoad")
    maxt.set("max", 0.9)
    maxt.set("zname", "CPU最大负载")
    maxt.set("description","一段时间内CPU的负载值的最大限制")
    maxt.set("format","设备%(title)sCPU达到最大负载%(max)s")
    
    m1dp.addThreshold(maxt)
    
    ds.addDataPoint(m1dp)
    ds.addDataPoint(ms5dp)
    
    t.addDataSource(ds)
    
def addConnDataSource(t):
    ds = SnmpDataSource("Conn")
    ds.set("execCycle", 60)

    mdp = DataPoint("CurConn")
    mdp.set("type", "GUAGE")
    mdp.set("oid", "1.3.6.1.4.1.89.35.1.40.29.23.1.4")
    
    maxt = MaxThreshold("maxConn")
    maxt.set("max", 90)
    maxt.set("zname", "最大连接数")
    maxt.set("description", "当前连接数最大值")
    maxt.set("format", "设备%(title)s最大连接数达到设定的最大值%(max)s")
    mdp.addThreshold(maxt)
    
    ds.addDataPoint(mdp)
    t.addDataSource(ds)
    
def addSessionDataSource(t):

    ds = SnmpDataSource("session")
    ds.set("execCycle", 60)
    
    dp = DataPoint("LastHttpSession")
    dp.set("type", "GUAGE")
    dp.set("oid", "1.3.6.1.4.1.89.35.1.40.29.20.1.19")
    ds.addDataPoint(dp)
    
    mdp = DataPoint("TotalHttpSession")
    mdp.set("type", "GUAGE")
    mdp.set("oid", "1.3.6.1.4.1.89.35.1.40.29.20.1.18")
    ds.addDataPoint(mdp)
    
    t.addDataSource(ds)

def createRedwareTpl():
    t=Template("BaseTpl_Redware")
    t.isBaseTpl = True
    t._saveObj()
    addCpuLoadDataSource(t)
    addSessionDataSource(t)
    addConnDataSource(t)
       
if __name__=="__main__":
    createRedwareTpl()