#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold
"""
clientCurConns    sysClientCurConns_sysClientCurConns    1.3.6.1.4.1.3375.2.1.1.2.1.8.0//client当前连接数
clientIn_bps    sysClientIn_f5CCurConns    1.3.6.1.4.1.3375.2.1.1.2.1.3.0
clientMaxConn    sysClientMaxConn_1PSServerBytesIn    1.3.6.1.4.1.3375.2.1.1.2.1.6.0//client最大连接数
clientNewConn    sysClientNewConn_sysClientNewConn    1.3.6.1.4.1.3375.2.1.1.2.1.7.0//client新建连接数
clientOut_bps    sysClientOut_bps_f5CsslCurConns    1.3.6.1.4.1.3375.2.1.1.2.1.5.0
failoverUnitMask    sysFailoverUnitMask_sysFailoverUnitMask    1.3.6.1.4.1.3375.2.1.1.1.1.19.0
serverCurConn    sysServerCurConn_sysServerCurConn    1.3.6.1.4.1.3375.2.1.1.2.1.15.0//server当前连接数
serverIn_bps    sysServerIn_bps_f5SCurConns    1.3.6.1.4.1.3375.2.1.1.2.1.10.0
serverMaxConn    sysServerMaxConn_f5ifBytesIn    1.3.6.1.4.1.3375.2.1.1.2.13.0//server最大连接数
serverNewConn    sysServerNewConn_sysServerNewConn    1.3.6.1.4.1.3375.2.1.1.2.1.14.0//server新建连接数
serverOut_bps    sysServerOut_bps_F5SsslCurConns    1.3.6.1.4.1.3375.2.1.1.2.1.12.0
statMemoryTotal    sysStatMemoryTotal_sysStatMemoryTotal    1.3.6.1.4.1.3375.2.1.1.2.1.44//总内存
statMemoryUsed    sysStatMemoryUsed_sysStatMemoryUsed    1.3.6.1.4.1.3375.2.1.1.2.1.45//使用的内存
statTmIdleCycles    sysStatTmIdleCycles_sysStatTmIdleCycles    1.3.6.1.4.1.3375.2.1.1.2.1.42
statTmTotalCycles    sysStatTmTotalCycles_sysStatTmTotalCycles    1.3.6.1.4.1.3375.2.1.1.2.1.41
"""
def addFailDataSource(t):
    ds = SnmpDataSource("Fail")
    ds.set("execCycle", 60)
    
    dp = DataPoint("failoverUnitMask")
    dp.set("oid", "1.3.6.1.4.1.3375.2.1.1.1.1.19.0")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    
    t.addDataSource(ds)

def addMemDataSource(t):
    ds = SnmpDataSource("Mem")
    ds.set("execCycle", 60)
    
    mfdp = DataPoint("memTotal")
    mfdp.set("oid", "1.3.6.1.4.1.3375.2.1.1.2.1.44")
    mfdp.set("type", "GUAGE")
    ds.addDataPoint(mfdp)

    mdp = DataPoint("Mem")
    mdp.set("type", "RPN")
    mdp.set("oid","1.3.6.1.4.1.3375.2.1.1.2.1.45")
    mdp.set("rpn","value=float(r.value)*100/(float(r.pv('Mem','memTotal', 100000))")
    
    maxt=MaxThreshold("maxMem")
    maxt.set("max", 90)
    maxt.set("zname", "最大内存使用率")
    maxt.set("description","已使用内存占系统总内存的最大百分比，通常设置在80~90之间")
    maxt.set("format","设备%(title)s内存使用百分比达到设定的最大值%(max)s")
    mdp.addThreshold(maxt)
    
    ds.addDataPoint(mdp)
    
    t.addDataSource(ds)
    
def addClientDataSource(t):
    ds = SnmpDataSource("Client")
    ds.set("execCycle", 60)
    
    dp1 = DataPoint("CurConns")
    dp1.set("oid", "1.3.6.1.4.1.3375.2.1.1.2.1.8.0")
    dp1.set("type", "GUAGE")
    ds.addDataPoint(dp1)
    
    dp2 = DataPoint("In_bps")
    dp2.set("oid", "1.3.6.1.4.1.3375.2.1.1.2.1.3.0")
    dp2.set("type", "GUAGE")
    ds.addDataPoint(dp2)
    
    dp3 = DataPoint("MaxConn")
    dp3.set("oid", "1.3.6.1.4.1.3375.2.1.1.2.1.6.0")
    dp3.set("type", "GUAGE")
    ds.addDataPoint(dp3)
    
    dp4 = DataPoint("NewConn")
    dp4.set("oid", "1.3.6.1.4.1.3375.2.1.1.2.1.7.0")
    dp4.set("type", "GUAGE")
    ds.addDataPoint(dp4)
    
    dp5 = DataPoint("Out_bps")
    dp5.set("oid", "1.3.6.1.4.1.3375.2.1.1.2.1.5.0")
    dp5.set("type", "GUAGE")
    ds.addDataPoint(dp5)
    
    t.addDataSource(ds)
    
def addConnDataSource(t): 
    ds = SnmpDataSource("Conn")
    ds.set("execCycle", 60)
    
    dp1 = DataPoint("CurConn")
    dp1.set("oid", "1.3.6.1.4.1.3375.2.1.1.2.1.15.0")
    dp1.set("type", "GUAGE")
    ds.addDataPoint(dp1)
    
    dp3 = DataPoint("MaxConn")
    dp3.set("oid", "1.3.6.1.4.1.3375.2.1.1.2.13.0")
    dp3.set("type", "GUAGE")
    ds.addDataPoint(dp3)
    
    dp4 = DataPoint("NewConn")
    dp4.set("oid", "1.3.6.1.4.1.3375.2.1.1.2.1.14.0")
    dp4.set("type", "GUAGE")
    ds.addDataPoint(dp4)
    
    t.addDataSource(ds)
      
def addServerDataSource(t):
    ds = SnmpDataSource("Server")
    ds.set("execCycle", 60)
    
    dp2 = DataPoint("In_bps")
    dp2.set("oid", "1.3.6.1.4.1.3375.2.1.1.2.1.10.0")
    dp2.set("type", "GUAGE")
    ds.addDataPoint(dp2)

    dp5 = DataPoint("Out_bps")
    dp5.set("oid", "1.3.6.1.4.1.3375.2.1.1.2.1.12.0")
    dp5.set("type", "GUAGE")
    ds.addDataPoint(dp5)
    
    t.addDataSource(ds)
    
def addStatTmDataSource(t):
    ds = SnmpDataSource("StatTm")
    ds.set("execCycle", 60)
    
    dp1 = DataPoint("IdleCycles")
    dp1.set("oid", "1.3.6.1.4.1.3375.2.1.1.2.1.42")
    dp1.set("type", "GUAGE")
    ds.addDataPoint(dp1)
    
    dp2 = DataPoint("TotalCycles")
    dp2.set("oid", "1.3.6.1.4.1.3375.2.1.1.2.1.41")
    dp2.set("type", "GUAGE")
    ds.addDataPoint(dp2)
    
    t.addDataSource(ds)
    
def createF5BigIPTpl():
    t=Template("BaseTpl_F5BigIP")
    t.isBaseTpl = True
    t._saveObj()
    addStatTmDataSource(t)
    addServerDataSource(t)
    addClientDataSource(t)
    addMemDataSource(t)
    addFailDataSource(t)
    addConnDataSource(t)
     
if __name__=="__main__":
    createF5BigIPTpl()
 