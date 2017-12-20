#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold
"""
Allocate:分配
frag：片段，碎片
nsResCpuAvg    nsResCpuAvg_nsResCpuAvg    1.3.6.1.4.1.3224.16.1.1.0  //CPU使用率
nsResCpuLast01Min    nsResCpuLast01Min_nsResCpuLast01Min    1.3.6.1.4.1.3224.16.1.2.0 //CPU1min负载
nsResCpuLast05Min    nsResCpuLast05Min_nsResCpuLast05Min    1.3.6.1.4.1.3224.16.1.3.0 //CPU5min负载
nsResCpuLast15Min    nsResCpuLast15Min_nsResCpuLast15Min    1.3.6.1.4.1.3224.16.1.4.0 //CPU15min负载
nsResMemAllocate    nsResMemAllocate_nsResMemAllocate    1.3.6.1.4.1.3224.16.2.1.0  //使用的内存
nsResMemFrag    nsResMemFrag_nsResMemFrag    1.3.6.1.4.1.3224.16.2.3.0 //内存碎片（需要减少内存碎片）
nsResMemLeft    nsResMemLeft_nsResMemLeft    1.3.6.1.4.1.3224.16.2.2.0  //剩余的内存
nsResSessAllocate    nsResSessAllocate_nsResSessAllocate    1.3.6.1.4.1.3224.16.3.2.0//成功的会话
nsResSessFailed    nsResSessFailed_nsResSessFailed    1.3.6.1.4.1.3224.16.3.4.0//失败的会话
nsResSessMaxium    nsResSessMaxium_nsResSessMaxium    1.3.6.1.4.1.3224.16.3.3.0//会话数最大值
nsrpVsdMemberStatus    nsrpVsdMemberStatus_nsResSessMaxium    1.3.6.1.4.1.3224.6.2.2.1.3.1 
//检查nsrpVsdMemberStatus的operstatus变化

"""
def addSessionDataSource(t):
    ds = SnmpDataSource("Conn")
    ds.set("execCycle", 60)
    
    mfdp = DataPoint("CurConn")
    mfdp.set("oid", "1.3.6.1.4.1.3224.16.3.2.0")
    mfdp.set("type", "GUAGE")
    ds.addDataPoint(mfdp)
    
    dp = DataPoint("SessFailed")
    dp.set("oid", "1.3.6.1.4.1.3224.16.3.4.0")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    
    dp2 = DataPoint("SessMaxium")
    dp2.set("oid", "1.3.6.1.4.1.3224.16.3.3.0")
    dp2.set("type", "GUAGE")
    ds.addDataPoint(dp2)
    
    t.addDataSource(ds)

def addMemDataSource(t):
    ds = SnmpDataSource("Mem")
    ds.set("execCycle", 60)
    
    mfdp = DataPoint("memLeft")
    mfdp.set("oid", "1.3.6.1.4.1.3224.16.2.2.0")
    mfdp.set("type", "GUAGE")
    ds.addDataPoint(mfdp)
    
    dp = DataPoint("memFrag")
    dp.set("oid", "1.3.6.1.4.1.3224.16.2.3.0")
    dp.set("type", "GUAGE")
    ds.addDataPoint(dp)
    
    dp2 = DataPoint("memberStatus")
    dp2.set("oid", "1.3.6.1.4.1.3224.6.2.2.1.3.1")
    dp2.set("type", "GUAGE")
    ds.addDataPoint(dp2)

    mdp = DataPoint("Mem")
    mdp.set("type", "RPN")
    mdp.set("oid","1.3.6.1.4.1.3224.16.2.1.0")
    mdp.set("rpn","value=100-(float(r.value)*100/(float(r.pv('Mem','memLeft', 100000))+float(r.value))")
    
    maxt=MaxThreshold("maxMem")
    maxt.set("max", 90)
    maxt.set("zname", "最大内存使用率")
    maxt.set("description","已使用内存占系统总内存的最大百分比，通常设置在80~90之间")
    maxt.set("format","设备%(title)s内存使用百分比达到设定的最大值%(max)s")
    mdp.addThreshold(maxt)
    
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
    dp.set("oid", "1.3.6.1.4.1.3224.16.1.1.0")
    dp.set("type", "GUAGE")
    dp.addThreshold(maxt)
    
    ds.addDataPoint(dp)
    t.addDataSource(ds)
 
def addCpuLoadDataSource(t):

    ds = SnmpDataSource("cpuLoad")
    ds.set("execCycle", 60)
    
    #1分钟负载数据点
    m1dp = DataPoint("1MinLoad")
    m1dp.set("oid", "1.3.6.1.4.1.3224.16.1.2.0")
    m1dp.set("type", "GUAGE")
    
    #5分钟CPU负载数据点
    m5dp = DataPoint("5MinLoad")
    m5dp.set("oid", "1.3.6.1.4.1.3224.16.1.3.0")
    m5dp.set("type", "GUAGE")
    
    #15分钟CPU负载数据点
    ms5dp = DataPoint("15MinLoad")
    ms5dp.set("oid", "1.3.6.1.4.1.3224.16.1.4.0")
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
    
def createJuniperNetScreenTpl():
    t=Template("BaseTpl_JuniperNetScreen")
    t.isBaseTpl = True
    t._saveObj()
    addCpuLoadDataSource(t)
    addCPUDataSource(t)
    addMemDataSource(t)
    addSessionDataSource(t)
       
if __name__=="__main__":
    createJuniperNetScreenTpl()