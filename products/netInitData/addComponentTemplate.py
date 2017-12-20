#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.ds import SnmpDataSource,CmdDataSource
from products.netModel.templates.threshold import MaxThreshold, StatusThreshold
def createInterfaceTemplate():
    """
    创建接口模板
    """
    t = Template("ethernetCsmacd")
    t.isBaseTpl = True
    t._saveObj()

    #数据源CPU
    ds = SnmpDataSource("Throughs")
    ds.set("execCycle", 60)
    dp0 = DataPoint("ifInOctets")
    dp0.set("oid", "1.3.6.1.2.1.2.2.1.10")
    dp0.set("type", "DERIVE")
    dp0.set("unit","Bit")
    maxs=MaxThreshold("maxInOctets")
    maxs.set("max",20)
    maxs.set("severity", 3)
    maxs.set("zname", "最大进流量")
    maxs.set("description","接口当前进流量占自定义带宽的最大百分比")
    maxs.set("rpn", "rpnvalue=mo.getCustomSpeed/100.0")
    maxs.set("format","接口%(title)s当前进流量:%(val)s超过设定的最大带宽利用率:%(max)s%%!")
    dp0.addThreshold(maxs)
    
    dp01 = DataPoint("ifOutOctets")
    dp01.set("oid", "1.3.6.1.2.1.2.2.1.16")
    dp01.set("type", "DERIVE")
    dp01.set("unit","Bit")
    maxi=MaxThreshold("maxOutOctets")
    maxi.set("max",20)
    maxi.set("severity", 3)
    maxi.set("zname", "最大出流量")
    maxi.set("description","接口当前出流量占自定义带宽的最大百分比")
    maxi.set("rpn", "rpnvalue=mo.getCustomSpeed/100.0")
    maxi.set("format","接口%(title)s当前出流量:%(val)s超过设定的最大带宽利用率:%(max)s%%!")
    dp01.addThreshold(maxi)
    
    ds.addDataPoint(dp0)
    ds.addDataPoint(dp01)
    t.addDataSource(ds)
    
    #数据源包数
    ds1 = SnmpDataSource("Packets")
    ds1.set("execCycle", 60)
    dp1 = DataPoint("ifInUcastPackets")
    dp1.set("oid", "1.3.6.1.2.1.2.2.1.11")
    dp1.set("type", "DERIVE")
    dp11 = DataPoint("ifOutUcastPackets")
    dp11.set("oid", "1.3.6.1.2.1.2.2.1.17")
    dp11.set("type", "DERIVE")
    
    ds1.addDataPoint(dp1)
    ds1.addDataPoint(dp11)
    t.addDataSource(ds1)
    
    #数据源错包
    ds2 = SnmpDataSource("Errors")
    ds2.set("execCycle", 60)
    dp2 = DataPoint("ifInErrors")
    dp2.set("oid", "1.3.6.1.2.1.2.2.1.14")
    dp2.set("type", "DERIVE")
    dp21 = DataPoint("ifOutErrors")
    dp21.set("oid", "1.3.6.1.2.1.2.2.1.20")
    dp21.set("type", "DERIVE")
    
    ds2.addDataPoint(dp2)
    ds2.addDataPoint(dp21)
    t.addDataSource(ds2)
    
    #数据源掉包
    dsd = SnmpDataSource("Discards")
    dsd.set("execCycle", 60)
    dpi = DataPoint("ifInDiscards")
    dpi.set("oid", "1.3.6.1.2.1.2.2.1.13")
    dpi.set("type", "DERIVE")
    dpo = DataPoint("ifOutDiscards")
    dpo.set("oid", "1.3.6.1.2.1.2.2.1.19")
    dpo.set("type", "DERIVE")
    
    dsd.addDataPoint(dpi)
    dsd.addDataPoint(dpo)
    t.addDataSource(dsd)
    
    ds3 = SnmpDataSource("Status")
    ds3.set("execCycle", 60)
    dp3 = DataPoint("ifOperStatus")
    dp3.set("oid", "1.3.6.1.2.1.2.2.1.8")
    dp3.set("type", "GUAGE")
    statusi=StatusThreshold("status")
    statusi.set("status",1)
    statusi.set("severity", 5)
    statusi.set("zname", "接口状态")
    statusi.set("description","接口的状态，接口是否掉线")
    statusi.set("format","接口%(title)s已掉线!")
    dp3.addThreshold(statusi)
    
    ds3.addDataPoint(dp3)
    t.addDataSource(ds3)
    return t

def createFileSystemTemplate():
    """
    创建文件系统模板
    """
    t = Template("FileSystem")
    t.isBaseTpl = True
    t._saveObj()

    #数据源已用块
    ds = SnmpDataSource("Used")
    ds.set("execCycle", 60)
    dp0 = DataPoint("usedBlocks")
    dp0.set("oid", "1.3.6.1.2.1.25.2.3.1.6")
    dp0.set("type", "GUAGE")
    ds.addDataPoint(dp0)
    t.addDataSource(ds)
    #磁盘利用率
    dds=SnmpDataSource("Disk")
    dds.set("execCycle", 60)
    ddp = DataPoint("Disk")
    ddp.set("oid", "1.3.6.1.2.1.25.2.3.1.6")
    ddp.set("type", "RPN")
    ddp.set("rpn","value=float(r.pv('Used','usedBlocks', 100000))/r.mattr('totalBlocks',1000000)")
    
    maxc=MaxThreshold("HighDisk")
    maxc.set("max", 90)
    maxc.set("severity", 4)
    maxc.set("zname", "磁盘利用率")
    maxc.set("description","磁盘的使用百分比的最大值")
    maxc.set("format","磁盘%(title)s当前利用率:%(val)s超过设定的最大阀值:%(max)s%%")
    
    ddp.addThreshold(maxc)
    dds.addDataPoint(ddp)
    t.addDataSource(dds)
    return t
    
def createProcessTemplate():
    """
    创建进程模板
    """
    t = Template("OSProcess")
    t.isBaseTpl = True
    t._saveObj()

    #数据源CPU
    ds = SnmpDataSource("ps")
    ds.set("execCycle", 60)
    dp1 = DataPoint("cpu")
    dp1.set("type", "DERIVE")
    cmaxt=MaxThreshold("maxCpu")
    cmaxt.set("max", 90)
    cmaxt.set("zname", "最大CPU使用率")
    cmaxt.set("description","进程使用的CPU资源占系统CPU总资源的最大百分比")
    cmaxt.set("format","设备%(title)sCPU最大值为%(max)s")
    dp1.addThreshold(cmaxt)
    dp2 = DataPoint("mem")
    dp2.set("type", "GUAGE")
    dp3 = DataPoint("count")
    dp3.set("type", "GUAGE")
    ds.addDataPoint(dp1)
    ds.addDataPoint(dp2)
    ds.addDataPoint(dp3)
    t.addDataSource(ds)
    return t


def createComponentTemplate():
    """
    创建组件模板
    """
    createInterfaceTemplate()
    createFileSystemTemplate()
    createProcessTemplate()

if __name__=="__main__":
    createComponentTemplate()

