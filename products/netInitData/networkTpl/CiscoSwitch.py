#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold
"""
1min_cpu    1min_cpu_1min_cpu    1.3.6.1.4.1.9.2.1.57.0
5min_cpu    5min_cpu_5min_cpu    1.3.6.1.4.1.9.2.1.56.0
5sec_cpu    5sec_cpu_5sec_cpu    1.3.6.1.4.1.9.2.1.58.0//CPU负载
CiscoMemoryPoolLargestFree    CiscoMemoryPoolLargestFree_CiscoMemoryPoolLargestFree    1.3.6.1.4.1.9.9.48.1.1.1.7.1
//内存池中最大剩余内存，内存池是一种动态分配内存的方式
ciscoMemoryPoolFree    ciscoMemoryPoolFree_ciscoMemoryPoolFree    1.3.6.1.4.1.9.9.48.1.1.1.6.1
//内存池中剩余内存
ciscoMemoryPoolUsed    ciscoMemoryPoolUsed_ciscoMemoryPoolUsed    1.3.6.1.4.1.9.9.48.1.1.1.5.1
//内存池中被使用的内存
icmpInRedirects    icmpInRedirects_icmpInRedirects    1.3.6.1.2.1.5.7.0 //系统收到的“重定向”消息
icmpOutEchos    icmpOutEchos_icmpOutEchos    1.3.6.1.2.1.5.21.0//系统收到的“请求回应”消息
ipInReceives    ipInReceives_ipInReceives    1.3.6.1.2.1.4.3.0//系统接收的所有IP数据包，包括出错的包
tcpOutRsts    tcpOutRsts_tcpOutRsts    1.3.6.1.2.1.6.15.0//系统发送的包含RST标志的TCP数据段
tcpOutSeqs    tcpOutSeqs_tcpOutSeqs    1.3.6.1.2.1.6.10.0//系统发送的TCP数据段总数
tcpRetransSeqs    tcpRetransSeqs_tcpRetransSeqs    1.3.6.1.2.1.6.11.0//系统中重传的数据段总数
"""
def addTcpDataSource(t):
    ds = SnmpDataSource("tcp")
    ds.set("execCycle", 60)
    
    dp1 = DataPoint("tcpOutRsts")
    dp1.set("oid", "1.3.6.1.2.1.6.15.0")
    dp1.set("type", "GUAGE")
    ds.addDataPoint(dp1)
    
    dp2 = DataPoint("tcpOutSeqs")
    dp2.set("oid", "1.3.6.1.2.1.6.10.0")
    dp2.set("type", "GUAGE")
    ds.addDataPoint(dp2)
    
    dp3 = DataPoint("tcpRetransSeqs")
    dp3.set("oid", "1.3.6.1.2.1.6.11.0")
    dp3.set("type", "GUAGE")
    ds.addDataPoint(dp3)
    
    t.addDataSource(ds)
    
def addIpInDataSource(t):
    ds = SnmpDataSource("IpIn")
    ds.set("execCycle", 60)
    
    dp = DataPoint("ipInReceives")
    dp.set("oid", "1.3.6.1.2.1.4.3.0")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    
    t.addDataSource(ds)
    
def addIcmpDataSource(t):
    ds = SnmpDataSource("Icmp")
    ds.set("execCycle", 60)
    
    dp1 = DataPoint("icmpInRedirects")
    dp1.set("oid", "1.3.6.1.2.1.5.7.0")
    dp1.set("type", "GUAGE")
    ds.addDataPoint(dp1)
    
    dp2 = DataPoint("icmpOutEchos")
    dp2.set("oid", "1.3.6.1.2.1.5.21.0")
    dp2.set("type", "GUAGE")
    ds.addDataPoint(dp2)
    
    t.addDataSource(ds)
      
def addCpuLoadDataSource(t):

    ds = SnmpDataSource("cpuLoad")
    ds.set("execCycle", 60)
    
    #1分钟负载数据点
    m1dp = DataPoint("1MinLoad")
    m1dp.set("oid", "1.3.6.1.4.1.9.2.1.57.0")
    m1dp.set("type", "GUAGE")
    
    #5分钟CPU负载数据点
    m5dp = DataPoint("5MinLoad")
    m5dp.set("oid", "1.3.6.1.4.1.9.2.1.56.0")
    m5dp.set("type", "GUAGE")
    
    #15分钟CPU负载数据点
    ms5dp = DataPoint("5secLoad")
    ms5dp.set("oid", "1.3.6.1.4.1.9.2.1.58.0")
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
    
    mfdp = DataPoint("largestMemFree")
    mfdp.set("oid", "1.3.6.1.4.1.9.9.48.1.1.1.7.1")
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
    
def createCiscoSwitchTpl():
    t=Template("BaseTpl_CiscoSwitch")
    t.isBaseTpl = True
    t._saveObj()
    addMemDataSource(t)
    addCpuLoadDataSource(t)
    addIcmpDataSource(t)
    addIpInDataSource(t)
    addTcpDataSource(t)
    
       
if __name__=="__main__":
    createCiscoSwitchTpl()