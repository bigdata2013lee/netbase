#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold
"""
15minuteLoad    15minuteLoad_15minuteLoad    1.3.6.1.4.1.2021.10.1.3.3    //CPU15分钟负载
1minuteLoad    1minuteLoad_1minuteLoad    1.3.6.1.4.1.2021.10.1.3.1    //CPU1分钟负载
5minuteLoad    5minuteLoad_5minuteLoad    1.3.6.1.4.1.2021.10.1.3.2         //CPU5分钟负载
diskFreeAvail    diskFreeAvail_diskFreeAvail    1.3.6.1.4.1.2620.1.6.7.3.5.0//剩余可用磁盘
diskFreeTotal    diskFreeTotal_diskFreeTotal    1.3.6.1.4.1.2620.1.6.7.3.4.0//剩余磁盘总量
diskPercent    diskPercent_diskPercent    1.3.6.1.4.1.2620.1.6.7.3.3.0      //磁盘使用率
diskTotal    diskTotal_diskTotal    1.3.6.1.4.1.2620.1.6.7.3.6.0            //磁盘总量
fwNumConn   fwNumConn_fwNumConn    1.3.6.1.4.1.2620.1.1.25.3.0           //防火墙当前连接数
fwPeakNumConn    fwPeakNumConn    1.3.6.1.4.1.2620.1.1.25.4                //峰值连接数
//memActiveReal    memActiveReal_memActiveReal    1.3.6.1.4.1.2620.1.6.7.4.4.0  //使用的物理内存
//memActiveVirtual    memActiveVirtual_memActiveVirtual    1.3.6.1.4.1.2620.1.6.7.4.2.0//使用的虚拟内存
"""
def addCPUDataSource(t):

    cds = SnmpDataSource("CPU")
    cds.set("execCycle", 60)
    
    cdp = DataPoint("CPU")
    cdp.set("type", "RPN")
    cdp.set("oid", "1.3.6.1.4.1.2021.11.11.0")
    cdp.set("rpn","value=100-float(r.pv('CPU','freeCpu',100))")
    
    #CPU最大阀值
    cmaxt=MaxThreshold("maxCpu")
    cmaxt.set("max", 90)
    cmaxt.set("zname", "最大CPU使用率")
    cmaxt.set("description","已使用的CPU资源占系统CPU总资源的最大百分比，通常设置为80～90之间")
    cmaxt.set("format","设备%(title)sCPU使用百分比达到设定的最大值%(max)s")
    cdp.addThreshold(cmaxt)
    cds.addDataPoint(cdp)

    fcdp = DataPoint("freeCpu")
    fcdp.set("oid", ".1.3.6.1.4.1.2021.11.11.0")
    fcdp.set("type", "GUAGE")
    cds.addDataPoint(fcdp)

    #添加CPU数据源
    t.addDataSource(cds)
    
def addConnDataSource(t):
    ds = SnmpDataSource("Conn")
    ds.set("execCycle", 60)
    
    mfdp = DataPoint("CurConn")
    mfdp.set("oid", "1.3.6.1.4.1.2620.1.1.25.3.0")
    mfdp.set("type", "GUAGE")
    ds.addDataPoint(mfdp)
    
    mfdp = DataPoint("fwPeakNumConn")
    mfdp.set("oid", "1.3.6.1.4.1.2620.1.1.25.4")
    mfdp.set("type", "GUAGE")
    ds.addDataPoint(mfdp)
    
    t.addDataSource(ds)
    
def addMemDataSource(t):
    ds = SnmpDataSource("Mem")
    ds.set("execCycle", 60)
    
    mfdp = DataPoint("memActiveVirtual")
    mfdp.set("oid", "1.3.6.1.4.1.2620.1.6.7.4.2.0")
    mfdp.set("type", "GUAGE")
    ds.addDataPoint(mfdp)

    mdp = DataPoint("Mem")
    mdp.set("type", "GUAGE")
    mdp.set("oid","1.3.6.1.4.1.2620.1.6.7.4.4.0")
    
    maxt=MaxThreshold("maxMem")
    maxt.set("max", 90)
    maxt.set("zname", "最大内存使用率")
    maxt.set("description","已使用内存占系统总内存的最大百分比，通常设置在80~90之间")
    maxt.set("format","设备%(title)s内存使用百分比达到设定的最大值%(max)s")
    mdp.addThreshold(maxt)
    
    ds.addDataPoint(mdp)
    
    t.addDataSource(ds)
    
def addCpuLoadDataSource(t):

    ds = SnmpDataSource("cpuLoad")
    ds.set("execCycle", 60)
    
    #1分钟负载数据点
    m1dp = DataPoint("1MinLoad")
    m1dp.set("oid", "1.3.6.1.4.1.2021.10.1.3.1")
    m1dp.set("type", "GUAGE")
    
    #5分钟CPU负载数据点
    m5dp = DataPoint("5MinLoad")
    m5dp.set("oid", "1.3.6.1.4.1.2021.10.1.3.2")
    m5dp.set("type", "GUAGE")
    
    #15分钟CPU负载数据点
    ms5dp = DataPoint("15MinLoad")
    ms5dp.set("oid", "1.3.6.1.4.1.2021.10.1.3.3")
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

def addDiskDataSource(t):
    ds = SnmpDataSource("Disk")
    ds.set("execCycle", 60)
    
    dp1 = DataPoint("diskFreeAvail")
    dp1.set("oid", "1.3.6.1.4.1.2620.1.6.7.3.5.0")
    dp1.set("type", "GUAGE")
    ds.addDataPoint(dp1)
    
    dp2 = DataPoint("diskFreeTotal")
    dp2.set("oid", "1.3.6.1.4.1.2620.1.6.7.3.4.0")
    dp2.set("type", "GUAGE")
    ds.addDataPoint(dp2)
    
    dp3 = DataPoint("diskPercent")
    dp3.set("oid", "1.3.6.1.4.1.2620.1.6.7.3.3.0")
    dp3.set("type", "GUAGE")
    ds.addDataPoint(dp3)
    
    dp4 = DataPoint("diskTotal")
    dp4.set("oid", "1.3.6.1.4.1.2620.1.6.7.3.6.0")
    dp4.set("type", "GUAGE")
    ds.addDataPoint(dp4)
    
    t.addDataSource(ds)
    
def createCheckpointR70Tpl():
    t=Template("BaseTpl_CheckpointR70")
    t.isBaseTpl = True
    t._saveObj()
    addDiskDataSource(t)
    addCpuLoadDataSource(t)
    addMemDataSource(t)
    addConnDataSource(t)
    addCPUDataSource(t)
    
       
if __name__=="__main__":
    createCheckpointR70Tpl()