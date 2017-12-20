#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource

from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold


##----------check_point------------------------------------------------------------
#防护墙过包，拒包，丢包数
fwPcktsOids = dict(
            
    fwAcceptedOid       = "1.3.6.1.4.1.2620.1.1.4.0",#int >
    fwRejectedOid       = "1.3.6.1.4.1.2620.1.1.5.0",#int >
    fwDroppedOid        = "1.3.6.1.4.1.2620.1.1.6.0" #int >
)
#防火墙连接数
connOids = dict(
             
    currentSession        = "1.3.6.1.4.1.2620.1.1.25.3.0",#int >
    fwPeakNumConnOid    = "1.3.6.1.4.1.2620.1.1.25.4.0" #int >
)

#防火墙接口流量
fwlStreamOids = dict(
           
    fwAcceptPcktsln1     = "1.3.6.1.4.1.2620.1.1.25.5.1.5.1.0",#int
    fwAcceptPcktsln2= "1.3.6.1.4.1.2620.1.1.25.5.1.5.2.0",#int
    fwAcceptPcktsln3= "1.3.6.1.4.1.2620.1.1.25.5.1.5.3.0",#int
    fwAcceptPcktsln4= "1.3.6.1.4.1.2620.1.1.25.5.1.5.4.0",#int
    fwAcceptPcktsout1    = "1.3.6.1.4.1.2620.1.1.25.5.1.6.1.0",#int
    fwAcceptPcktsout2= "1.3.6.1.4.1.2620.1.1.25.5.1.6.2.0",#int
    fwAcceptPcktsout3= "1.3.6.1.4.1.2620.1.1.25.5.1.6.3.0",#int
    fwAcceptPcktsout4= "1.3.6.1.4.1.2620.1.1.25.5.1.6.4.0",#int
    fwAcceptBytesln1     = "1.3.6.1.4.1.2620.1.1.25.5.1.7.1.0",#int
    fwAcceptBytesln2= "1.3.6.1.4.1.2620.1.1.25.5.1.7.2.0",#int
    fwAcceptBytesln3= "1.3.6.1.4.1.2620.1.1.25.5.1.7.3.0",#int
    fwAcceptBytesln4= "1.3.6.1.4.1.2620.1.1.25.5.1.7.4.0",#int
    fwAcceptBytesOut1   = "1.3.6.1.4.1.2620.1.1.25.5.1.8.1.0",#int
    fwAcceptBytesOut2= "1.3.6.1.4.1.2620.1.1.25.5.1.8.2.0", #int
    fwAcceptBytesOut3= "1.3.6.1.4.1.2620.1.1.25.5.1.8.3.0", #int
    fwAcceptBytesOut4= "1.3.6.1.4.1.2620.1.1.25.5.1.8.4.0" #int
)

#HA状态,HA端口状态
haStatesOids = dict(

    haIPiOid        = "1.3.6.1.4.1.2620.1.5.12.1.3",           
    haStateOid      = "1.3.6.1.4.1.2620.1.5.6",
    hastatusOid     = "1.3.6.1.4.1.2620.1.5.12.1.4"
)

#mem
memOids = dict(
          
    memTotalReal    = "1.3.6.1.4.1.2620.1.6.7.1.3.0",#负数
    memActiveReal   = "1.3.6.1.4.1.2620.1.6.7.1.4.0",#int
    memFreeReal     = "1.3.6.1.4.1.2620.1.6.7.1.5.0",#负数
    memTotalReal64  = "1.3.6.1.4.1.2620.1.6.7.4.3.0",#stringnum
    memActiveReal64 = "1.3.6.1.4.1.2620.1.6.7.4.4.0",#stringnum
    memFreeReal64   = "1.3.6.1.4.1.2620.1.6.7.4.5.0" #stringnum
)
#磁盘
diskOids = dict(
       
    diskPercent     = "1.3.6.1.4.1.2620.1.6.7.3.3.0",#int
    diskFreeTotal   = "1.3.6.1.4.1.2620.1.6.7.3.4.0",#stringnum
    diskFreeAvail   = "1.3.6.1.4.1.2620.1.6.7.3.5.0",#stringnum
    diskTotal       = "1.3.6.1.4.1.2620.1.6.7.3.6.0"#stringnum
)
#router
routOids = dict(
      
    routingDest1     = "1.3.6.1.4.1.2620.1.6.6.1.2.1.0",#int
    routingDest2= "1.3.6.1.4.1.2620.1.6.6.1.2.2.0",#int
    routingDest3= "1.3.6.1.4.1.2620.1.6.6.1.2.3.0",#int
    routingDest4= "1.3.6.1.4.1.2620.1.6.6.1.2.4.0",#int
    routingDest5= "1.3.6.1.4.1.2620.1.6.6.1.2.5.0",#int
    routingDest6= "1.3.6.1.4.1.2620.1.6.6.1.2.6.0",#int
    routingMask1     = "1.3.6.1.4.1.2620.1.6.6.1.3.1.0",#int
    routingMask2= "1.3.6.1.4.1.2620.1.6.6.1.3.2.0",#int
    routingMask3= "1.3.6.1.4.1.2620.1.6.6.1.3.3.0",#int
    routingMask4= "1.3.6.1.4.1.2620.1.6.6.1.3.4.0",#int
    routingMask5= "1.3.6.1.4.1.2620.1.6.6.1.3.5.0",#int
    routingMask6= "1.3.6.1.4.1.2620.1.6.6.1.3.6.0",#int
    routingGatweway1 = "1.3.6.1.4.1.2620.1.6.6.1.4.1.0", #int
    routingGatweway2= "1.3.6.1.4.1.2620.1.6.6.1.4.2.0", #int
    routingGatweway3= "1.3.6.1.4.1.2620.1.6.6.1.4.3.0", #int
    routingGatweway4= "1.3.6.1.4.1.2620.1.6.6.1.4.4.0", #int
    routingGatweway5= "1.3.6.1.4.1.2620.1.6.6.1.4.5.0", #int
    routingGatweway6= "1.3.6.1.4.1.2620.1.6.6.1.4.6.0", #int
)
#floodGate队列
floodGateOids = dict(
                     
    fgPendPcktsIn       = "1.3.6.1.4.1.2620.1.3.9.1.10",
    fgPendPcktsOut      = "1.3.6.1.4.1.2620.1.3.9.1.11",
    fgPendBytesIn       = "1.3.6.1.4.1.2620.1.3.9.1.12",
    fgPendBytesOut      = "1.3.6.1.4.1.2620.1.3.9.1.13",
    fgAvrRateIn         = "1.3.6.1.4.1.2620.1.3.9.1.6",
    fgAvrRateOut        = "1.3.6.1.4.1.2620.1.3.9.1.7"
)
#cpvTnl
cpvTnlOids = dict(
                  
    cpvTnlMonStatus     = "1.3.6.1.4.1.2620.1.2.11.1.2",
    cpvTnlMonCurrAddr   = "1.3.6.1.4.1.2620.1.2.11.1.3"
)
#FwSS-http
fwssHttpOids = dict(
          
    httpSessCount       = "1.3.6.1.4.1.2620.1.1.26.9.1.11.0",#int
    httpSessCurr        = "1.3.6.1.4.1.2620.1.1.26.9.1.10.0",#int
    httpSslSessCount    = "1.3.6.1.4.1.2620.1.1.26.9.1.27.0",#int
    httpPort            = "1.3.6.1.4.1.2620.1.1.26.9.1.3.0", #int
    httpTunneledCount   = "1.3.6.1.4.1.2620.1.1.26.9.1.33.0",#int
    httpIsAlive         = "1.3.6.1.4.1.2620.1.1.26.9.1.38.0" #int
)
#fwss-smpt
fwssSmptOids = dict(

    smptSessCurr        = "1.3.6.1.4.1.2620.1.1.26.9.6.10.0",#int
    smptfSessCount      = "1.3.6.1.4.1.2620.1.1.26.9.6.11.0" #int
)
#内核kernel memory
fwKmemOids = dict(
       
    sysPhyMemory        = "1.3.6.1.4.1.2620.1.1.26.2.1.0", #int
    avaPhyMemory        = "1.3.6.1.4.1.2620.1.1.26.2.2.0", #int
    bytesInternalUse    = "1.3.6.1.4.1.2620.1.1.26.2.11.0",#int >
    allocOperations     = "1.3.6.1.4.1.2620.1.1.26.2.13.0",#int >
    freeOperations      = "1.3.6.1.4.1.2620.1.1.26.2.14.0",#int >
    bytesUsed           = "1.3.6.1.4.1.2620.1.1.26.2.4.0", #int >
    bytesUnused            = "1.3.6.1.4.1.2620.1.1.26.2.7.0"  #int
)


#----创建模板------------------------------------------------------------------------------
def createCheckPointTemplate():
    t = Template("BaseTpl_CheckPoint")
    t.isBaseTpl = True
    t._saveObj()
    addFwPcktsSnmpDataSource(t)
    addFwConnSnmpDataSource(t)
    addFwlStreamSnmpDataSource(t)
    addHaStatesSnmpDataSource(t)
    addMemDataSource(t)
    addDiskSnmpDataSource(t)
    addRouterSnmpDataSource(t)
    addFloodGateSnmpDataSource(t)
    addCpvTnlSnmpDataSource(t)
    addFwssHttpSnmpDataSource(t)
    addFwssSmtpSnmpDataSource(t)
    addFwKmemSnmpDataSource(t)
    addSNMPCPUDataSource(t)
    addCpuLoadDataSource(t)

#防火墙过包，拒包，丢包数
def addFwPcktsSnmpDataSource(t, fwPcktsOids=fwPcktsOids):
    ds = SnmpDataSource("FwPckts")
    ds.set("execCycle", 60)
    
    createDataPoint(ds, "fwAccepted", fwPcktsOids.get("fwAcceptedOid"), "GUAGE",{})
    createDataPoint(ds, "fwRejected", fwPcktsOids.get("fwRejectedOid"), "GUAGE",{})
    createDataPoint(ds, "fwDropped",  fwPcktsOids.get("fwDroppedOid"),  "GUAGE",{})
    t.addDataSource(ds)
    
#防火墙连接数
def addFwConnSnmpDataSource(t, fwConnOids=connOids):
    ds = SnmpDataSource("Connections")
    ds.set("execCycle", 60)
    
    createDataPoint(ds, "currentSession", fwConnOids.get("currentSession"), "GUAGE",{})
    createDataPoint(ds, "fwPeakNumConn", fwConnOids.get("fwPeakNumConnOid"), "GUAGE",{})   
    t.addDataSource(ds)
    
#防火墙接口流量
def addFwlStreamSnmpDataSource(t, fwlStreamOids=fwlStreamOids):
    ds = SnmpDataSource("FwlStream")
    ds.set("execCycle", 60)
    
    for k ,v in fwlStreamOids.items():
        createDataPoint(ds, k, v, "GUAGE", {})
    t.addDataSource(ds)
    
#HA状态,HA端口状态
def addHaStatesSnmpDataSource(t, haStatesOids=haStatesOids):
    ds = SnmpDataSource("HaState")
    ds.set("execCycle", 60)
    
    createDataPoint(ds, "haState", haStatesOids.get("haStateOid"), "GUAGE",{})
    createDataPoint(ds, "hastatus", haStatesOids.get("hastatusOid"), "GUAGE",{})
    createDataPoint(ds, "haIP", haStatesOids.get("haIPiOid"), "GUAGE",{})
    t.addDataSource(ds)

#内存  
def addMemDataSource(t, memOids=memOids):
    ds = SnmpDataSource("Mem")
    ds.set("execCycle", 60)
    createDataPoint(ds, "memTotalReal", memOids.get("memTotalReal"), "ABSOLUTE",{})
    createDataPoint(ds, "memActiveReal", memOids.get("memActiveReal"), "GUAGE",{})
    createDataPoint(ds, "memFreeReal", memOids.get("memFreeReal"), "ABSOLUTE",{})
    createDataPoint(ds, "totalMem", memOids.get("memTotalReal64"), "GUAGE",{})
    createDataPoint(ds, "activeMem", memOids.get("memActiveReal64"), "GUAGE",{})
    #设置内存占有率数据点，实际使用内存数/总的内存数等于内存使用率
    mdp = DataPoint("Mem")
    mdp.set("type", "RPN")
    mdp.set("oid","1.3.6.1.4.1.2620.1.6.7.4.5.0")
    mdp.set("rpn","value=100-(float(r.value)*100/float(r.pv('Mem','totalMem', 100000)))")
    
    maxt=MaxThreshold("maxMem")
    maxt.set("max", 90)
    maxt.set("format","设备%(title)s内存最大使用百分比%(max)s")
    mdp.addThreshold(maxt)
    
    ds.addDataPoint(mdp)
    
    t.addDataSource(ds)
#磁盘
def addDiskSnmpDataSource(t, diskOids=diskOids):
    ds = SnmpDataSource("Disk")
    ds.set("execCycle", 60)
    
    createDataPoint(ds, "diskPercent", diskOids.get("diskPercent"), "GUAGE",{})
    createDataPoint(ds, "diskFreeTotal", diskOids.get("diskFreeTotal"), "GUAGE",{})
    createDataPoint(ds, "diskFreeAvail", diskOids.get("diskFreeAvail"), "GUAGE",{})
    createDataPoint(ds, "diskTotal", diskOids.get("diskTotal"), "GUAGE",{})
    t.addDataSource(ds)
#路由器    
def addRouterSnmpDataSource(t, routOids=routOids):
    ds = SnmpDataSource("Rout")
    ds.set("execCycle", 60)
    
    for k ,v in routOids.items():
        createDataPoint(ds, k, v, "GUAGE", {})
    t.addDataSource(ds)
#floodgate
def addFloodGateSnmpDataSource(t, floodGateOids=floodGateOids):
    ds = SnmpDataSource("floodGate")
    ds.set("execCycle", 60)
    
    for k ,v in floodGateOids.items():
        createDataPoint(ds, k, v, "GUAGE", {})
    t.addDataSource(ds)
#CpvTnl
def addCpvTnlSnmpDataSource(t, cpvTnlOids=cpvTnlOids):
    ds = SnmpDataSource("cpvTnl")
    ds.set("execCycle", 60)
    
    for k ,v in cpvTnlOids.items():
        createDataPoint(ds, k, v, "GUAGE", {})
    t.addDataSource(ds)
#FwssHttp    
def addFwssHttpSnmpDataSource(t, fwssHttpOids=fwssHttpOids):
    ds = SnmpDataSource("fwssHttp")
    ds.set("execCycle", 60)
    
    for k ,v in fwssHttpOids.items():
        createDataPoint(ds, k, v, "GUAGE", {})
    t.addDataSource(ds)
#FwssSmtp    
def addFwssSmtpSnmpDataSource(t, fwssSmptOids=fwssSmptOids):
    ds = SnmpDataSource("fwssSmpt")
    ds.set("execCycle", 60)
    
    for k ,v in fwssSmptOids.items():
        createDataPoint(ds, k, v, "GUAGE", {})
    t.addDataSource(ds)
#内核   
def addFwKmemSnmpDataSource(t, fwKmemOids=fwKmemOids):
    ds = SnmpDataSource("fwKmem")
    ds.set("execCycle", 60)
    
    for k ,v in fwKmemOids.items():
        createDataPoint(ds, k, v, "GUAGE", {})
    t.addDataSource(ds)
    
def createDataPoint(ds, dp_name, dpOid, dptype, thdValue={}, valueType=None):    
    """
    ds: 数据源
    dp_name: 创建的数据点的名字
    dpOid:  数据点的OID
    thdValue: 阀值
    """
    dp = DataPoint(dp_name)
    dp.set("oid", dpOid)
    dp.set("type", dptype)
    if valueType : 
        dp.set("valueType", valueType) 
    if thdValue.has_key("max") and thdValue.has_key("min") and (len(thdValue) == 2):
        rangt = RangeThreshold("rangt_"+dp_name)
        rangt.set("max", thdValue.get("max"))
        rangt.set("min", thdValue.get("min"))
        rangt.set("format", dp_name +"%(title)s 超过设定的范围阀值:%(min)s~%(max)s")
        dp.addThreshold(rangt)
    elif thdValue.has_key("max") and (len(thdValue) == 1) :
        maxt = MaxThreshold("maxThread")
        maxt.set("max", thdValue.get("max"))
        maxt.set("format", dp_name + " %(title)s最大阀值为%(max)s")
        dp.addThreshold(maxt)
    elif thdValue.has_key("min") and (len(thdValue) == 1) :
        mint = MinThreshold("minThread")
        mint.set("min", thdValue.get("min"))
        mint.set("format", dp_name + " %(title)s最小阀值为%(min)s")
        dp.addThreshold(mint)
    ds.addDataPoint(dp)
   
def addSNMPCPUDataSource(t):
    """
    添加LinuxCPU数据源
    """
    #数据源CPU,有GUAGE
    cds = SnmpDataSource("CPU")
    cds.set("execCycle", 60)
    
    #用户CPU比例百分点
    ucdp = DataPoint("userCpu")
    ucdp.set("oid", ".1.3.6.1.4.1.2021.11.9.0")
    ucdp.set("type", "GUAGE")
    #CPU最大阀值
    cmaxt=MaxThreshold("maxCpu")
    cmaxt.set("max", 90)
    cmaxt.set("format","设备%(title)sCPU最大值为%(max)s")
    ucdp.addThreshold(cmaxt)
    cds.addDataPoint(ucdp)
    
    #设置系统CPU为默认CPU,百分比
    scdp = DataPoint("CPU")
    scdp.set("oid", ".1.3.6.1.4.1.2021.11.10.0")
    scdp.set("type", "GUAGE")
    scdp.addThreshold(cmaxt)
    cds.addDataPoint(scdp)
    
    #空闲CPU百分比数据点
    fcdp = DataPoint("freeCpu")
    fcdp.set("oid", ".1.3.6.1.4.1.2021.11.11.0")
    fcdp.set("type", "GUAGE")
    #CPU最小阀值
    cmint=MinThreshold("minCpu")
    cmint.set("min", 10)
    cmint.set("format","设备%(title)s空闲CPU最小百分比为%(min)s")
    fcdp.addThreshold(cmint)
    cds.addDataPoint(fcdp)

    #添加CPU数据源
    t.addDataSource(cds)
    
def  addCpuLoadDataSource(t):
    """
    创建CPU负载数据源
    """
    #负载数据源，有GUAGE
    lds = SnmpDataSource("Load")
    lds.set("execCycle", 60)
    
    #1分钟负载数据点
    m1dp = DataPoint("1MinLoad")
    m1dp.set("oid", ".1.3.6.1.4.1.2021.10.1.3.1")
    m1dp.set("type", "GUAGE")
    
    #5分钟CPU负载数据点
    m5dp = DataPoint("5MinLoad")
    m5dp.set("oid", ".1.3.6.1.4.1.2021.10.1.3.2")
    m5dp.set("type", "GUAGE")
    
    #15分钟CPU负载数据点
    m15dp = DataPoint("15MinLoad")
    m15dp.set("oid", ".1.3.6.1.4.1.2021.10.1.3.3")
    m15dp.set("type", "GUAGE")
        
    maxt=MaxThreshold("MaxLoad")
    maxt.set("max", 0.9)
    maxt.set("format","设备%(title)s最大负载%(max)s")
    
    m1dp.addThreshold(maxt)
    m5dp.addThreshold(maxt)
    m15dp.addThreshold(maxt)
    
    lds.addDataPoint(m1dp)
    lds.addDataPoint(m5dp)
    lds.addDataPoint(m15dp)
        
    t.addDataSource(lds)
    

if __name__ == '__main__':
    createCheckPointTemplate()
    
    
    
    
    
    
    
    
    
    
