from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource,CmdDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold

def startCreateCheckPointSNMPtemplate():
    """
    创建Check_Point模板
    """
    t = Template("CheckPoint")
    
    t._saveObj()
    
    addLinuxSNMPCPUDataSource(t)
    
    addCpuLoadDataSource(t)
    
    addFwPackageInfoDataSource(t)
    addFwConnNumDataSource(t)
    addFwlAcceptInfoDataSource(t)
    addHaStatesDataSource(t)


def addFwPackageInfoDataSource(t):
    """
    创建设备信息数据源
    """
    #数据源设备信息
    ds = SnmpDataSource("FwPackageInfo")
    ds.set("execCycle",60)

    #防火墙通过包数量
    dp = DataPoint("fwAccepted")
    dp.set("valueType", "Integer")
    dp.set("oid", "1.3.6.4.1.2620.1.1.4")
    ds.addDataPoint(dp)
    #防火墙拒包数数量
    dp = DataPoint("fwRejected")
    dp.set("valueType", "Integer")
    dp.set("oid", "1.3.6.4.1.2620.1.1.5")
    ds.addDataPoint(dp)
    #防火墙丢弃包数
    dp = DataPoint("fwDropped")
    dp.set("valueType", "Integer")
    dp.set("oid", "1.3.6.4.1.2620.1.1.6")
    ds.addDataPoint(dp)
    t.addDataSource(ds)
def addFwConnNumDataSource(t):
    ds = SnmpDataSource("FwPackageInfo")
    ds.set("execCycle",60)
    #防火墙连接数
    dp = DataPoint("fwNumConn")
    dp.set("valueType", "Integer")
    dp.set("oid", "1.3.6.4.1.2620.1.1.25.3")
    ds.addDataPoint(dp)
    #未知数据
    dp = DataPoint("fwPeakNunConn")
    dp.set("valueType", "Integer")
    dp.set("oid", "1.3.6.4.1.2620.1.1.25.4")
    ds.addDataPoint(dp)
    t.addDataSource(ds)
def addFwlAcceptInfoDataSource(t):
    ds = SnmpDataSource("FwlAcceptInfo")
    ds.set("execCycle",60)
    #防火墙接口进包数
    dp = DataPoint("fwlfaccepPcktsln")
    dp.set("valueType", "Integer")
    dp.set("oid", "1.3.6.1.4.1.2620.1.1.25.5.1.5")
    ds.addDataPoint(dp)
    #防火墙接口出包数
    dp = DataPoint("fwlfaccepPcktsout")
    dp.set("valueType", "Integer")
    dp.set("oid", "1.3.6.1.4.1.2620.1.1.25.5.1.6")
    ds.addDataPoint(dp)
    #进流量
    dp = DataPoint("fwAcceptBytesln")
    dp.set("valueType", "Integer")
    dp.set("type","RPN")
    dp.set("oid", "1.3.6.1.4.1.2620.1.1.25.5.1.7")
    dp.set("rpn","value=(r.value/8/1024/1024)")
    maxt = MaxThreshold("maxAcceptIn")
    maxt.set("max",90)
    maxt.set("format","设备%(title)s内存最大进流量为%(max)s")
    dp.addThreshold(maxt)
    ds.addDataPoint(dp)
    #出流量
    dp = DataPoint("fwAcceptBytesOut")
    dp.set("valueType", "Integer")
    dp.set("type","RPN")
    dp.set("oid", "1.3.6.1.4.1.2620.1.1.25.5.1.8")
    dp.set("rpn","value=(r.value/8/1024/1024)")
    maxt = MaxThreshold("maxAcceptOut")
    maxt.set("max",90)
    maxt.set("format","设备%(title)s内存最大出流量为%(max)s")
    dp.addThreshold(maxt)
    ds.addDataPoint(dp)
    t.addDataSource(ds)
def addHaStatesDataSource(t):
    ds = SnmpDataSource("HaStates")
    ds.set("execCycle",60)
    #HA状态
    dp = DataPoint("haState")
    dp.set("valueType", ("active", "not active", "stand-by", "unknown HA state"))
    dp.set("oid", "1.3.6.1.4.1.2620.1.5.6")
    ds.addDataPoint(dp)
    #HA端口状态(up/down）
    dp = DataPoint("hastatus")
    dp.set("valueType", "String")
    dp.set("oid", "1.3.6.1.4.1.2620.1.5.12.1.4")
    ds.addDataPoint(dp)
    #memTotalReal
    dp = DataPoint("memTotalReal")
    dp.set("oid", "1.3.6.1.4.1.2620.1.6.7.4.4.0")
    ds.addDataPoint(dp)
    #未知
    dp = DataPoint("unknowPoint")
    dp.set("oid", "1.3.6.1.4.1.2620.1.6.7.4.3.0")
    ds.addDataPoint(dp)
    t.addDataSource(ds)
def addLinuxSNMPCPUDataSource(t):
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
    
def addLinuxSNMPMemDataSource(t):
    #数据源内存,有RPN
    mds = SnmpDataSource("Mem")
    mds.set("execCycle", 60)
    
    #总内存数据点
    tmdp = DataPoint("totalMem")
    tmdp.set("oid", "1.3.6.1.4.1.2021.4.5.0")
    mds.addDataPoint(tmdp)
    
    #设置内存占有率数据点，实际使用内存数/总的内存数等于内存使用率
    mdp = DataPoint("Mem")
    mdp.set("type", "RPN")
    mdp.set("oid", "1.3.6.1.4.1.2021.4.6.0")
    mdp.set("rpn","value=100-(r.value*100/float(r.pv('Mem','totalMem', 100000)))")
    
    maxt=MaxThreshold("maxMem")
    maxt.set("max", 90)
    maxt.set("format","设备%(title)s内存最大使用百分比%(max)s")
    mdp.addThreshold(maxt)
    
    mds.addDataPoint(mdp)
    
    #设置总Swap数据点
    tsdp = DataPoint("totalSwap")
    tsdp.set("oid", "1.3.6.1.4.1.2021.4.3.0")
    mds.addDataPoint(tsdp)
    
    #设置可用Swap数据点
    masdp = DataPoint("memAvailSwap")
    masdp.set("oid", "1.3.6.1.4.1.2021.4.4.0")
    mds.addDataPoint(masdp)
    
    #设置内存buffer
    mbdp = DataPoint("memBuffer")
    mbdp.set("oid", "1.3.6.1.4.1.2021.4.14.0")
    mds.addDataPoint(mbdp)
    
    #设置内存Cached数据点
    mcdp = DataPoint("memCached")   
    mcdp.set("oid", "1.3.6.1.4.1.2021.4.15.0")
    mds.addDataPoint(mcdp)
    
    t.addDataSource(mds)
    return t  
def startCreatCmdTemplate():
    """
    创建命令行模板
    """
    #创建模板
    t = Template("BaseTpl_CmdLinux")
    t.isBaseTpl = True
    t._saveObj()
    
    #本地命令who数据源
    dswho = CmdDataSource("who")
    dswho.set("cmd", "cmd='who'")
    dswho.set("parser","who")
    dswho.set("execType","script")
    #解析who命令的数据点,可以比对
    dpwho = DataPoint("who")
    dpwho.set("type","GUAGE")
    dpwho.set("valueType", "String")
    dpwho.set("type", "Compare")
    #添加数据点到数据源
    dswho.addDataPoint(dpwho)
    #添加数据源到模板
    t.addDataSource(dswho)
    
    #ssh命令ifconfig数据源
    dsifc= CmdDataSource("ifconfig")
    dsifc.set("cmd", "cmd='ifconfig'")
    dsifc.set("execType","ssh")
    dsifc.set("parser","ifconfig")
    #解析ifconfig下的地址数据点
    dpaddr = DataPoint("addr")
    dpaddr.set("type","GUAGE")
    dpaddr.set("valueType","String")
    #解析ifconfig下的包数据点
    dppack = DataPoint("packets")
    dppack.set("type","GUAGE")
    dppack.set("valueType","Num")
    #添加数据点到数据源
    dsifc.addDataPoint(dpaddr)
    dsifc.addDataPoint(dppack)
    
    #script命令ping数据源
    dsping= CmdDataSource("ping")
    dsping.set("cmd", "cmd='ping -n -c 3 -w 10 '+mo.manageIp")
    dsping.set("execType","script")
    dsping.set("parser","ping")
    
    #解析ping下的avgRtt数据点
    dpavgrtt= DataPoint("avgRtt")
    dpavgrtt.set("type","GUAGE")
    dpavgrtt.set("valueType","Num")
    
    #解析ping下的minRtt数据点
    dpminrtt= DataPoint("minRtt")
    dpminrtt.set("type","GUAGE")
    dpminrtt.set("valueType","Num")
    
    #解析ping下的maxRtt数据点
    dpmaxrtt= DataPoint("maxRtt")
    dpmaxrtt.set("type","GUAGE")
    dpmaxrtt.set("valueType","Num")

    #解析ping下的mdevRtt数据点
    dpmdevrtt= DataPoint("mdevRtt")
    dpmdevrtt.set("type","GUAGE")
    dpmdevrtt.set("valueType","Num")
    
    #解析ping下的pingLoss数据点
    dppingloss= DataPoint("pingLoss")
    dppingloss.set("type","GUAGE")
    dppingloss.set("valueType","Num")
    dppingloss.set("unit","Percent")
    
    #解析ping下的pingReceived数据点
    dppingreceived= DataPoint("pingReceived")
    dppingreceived.set("type","GUAGE")
    dppingreceived.set("valueType","Num")
    
    #添加数据点到数据源
    dsping.addDataPoint(dpavgrtt)
    dsping.addDataPoint(dpminrtt)
    dsping.addDataPoint(dpmaxrtt)
    dsping.addDataPoint(dpmdevrtt)
    dsping.addDataPoint(dppingloss)
    dsping.addDataPoint(dppingreceived)
    
    #添加数据源到模板
    t.addDataSource(dsping)

    return t

#创建window SNMP模板
def startCreateWindowSNMPTemplate():
    """
    创建Window SNMP 模块
    """
    t = Template("BaseTpl_Window")
    t.isBaseTpl = True
    t._medata["pluginSettings"] = dict(interface="InterfaceMap", process="HRSWRunMap", fileSystem="HRFileSystemMap")
    t._saveObj()
    #系统信息
    addDeviceInfoDataSource(t)
    addWindowSNMPCPUDataSource(t)
    addWindowSNMPMemDataSource(t)
def addDeviceInfoDataSource(t):
    """
    创建设备信息数据源
    """
    #数据源设备信息
    dds = SnmpDataSource("DeviceInfo")
    dds.set("execCycle", 60)
    
    #设备名称数据点
    ddp = DataPoint("deviceName")
    ddp.set("valueType", "String")
    ddp.set("oid", ".1.3.6.1.2.1.1.5.0")
    dds.addDataPoint(ddp)
    
    #系统更新时间数据点
    tdp = DataPoint("SysUpTime")
    tdp.set("oid", "1.3.6.1.2.1.1.3.0")
    tdp.set("valueType", "String")
    dds.addDataPoint(tdp)   
    
    t.addDataSource(dds)
   
    
def addWindowSNMPCPUDataSource(t):
    """
    windowCPU数据源
    """ 
    cds = SnmpDataSource("CPU")
    cds.set("execCycle", 60)
    
    cdp = DataPoint("CPU")
    cdp.set("oid", "1.3.6.1.4.1.9600.1.1.5.1.5.6.95.84.111.116.97.108")
    cdp.set("type", "GUAGE")
    
    maxt=MaxThreshold("maxCpu")
    maxt.set("max", 85)
    maxt.set("format","设备%(title)sCPU最大值为%(max)s")
    cdp.addThreshold(maxt)
    
    cds.addDataPoint(cdp)
    t.addDataSource(cds)
    
    
    
def addWindowSNMPMemDataSource(t):
    """
    window内存数据源
    """ 
    #内存
    mds = SnmpDataSource("Mem")
    mds.set("execCycle", 60)
    
    #总内存数据点
    tmdp = DataPoint("totalMem")
    tmdp.set("oid", "1.3.6.1.2.1.25.2.2.0")
    mds.addDataPoint(tmdp)
    
    #设置realMem为默认内存
    mdp = DataPoint("Mem")
    mdp.set("oid", "1.3.6.1.4.1.9600.1.1.2.2.0")
    mdp.set("type", "RPN")
    mdp.set("rpn","value=100-(r.value*100/float(r.pv('Mem','totalMem', 10000000)))")
    rmaxt = MaxThreshold("maxRealMem")
    rmaxt.set("max",80)
    rmaxt.set("format","设备%(title)s内存最大使用百分比%(max)s")
    mdp.addThreshold(rmaxt)

    mds.addDataPoint(mdp)
    t.addDataSource(mds) 
if __name__ == '__main__':
    startCreatCmdTemplate()
    startCreateCheckPointSNMPtemplate()
    startCreateWindowSNMPTemplate()