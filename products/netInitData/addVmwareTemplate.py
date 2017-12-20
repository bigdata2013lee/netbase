#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import CmdDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold

def startVmhostTemplate():
    """
    创建vmware host模板
    """
    #创建模板
    t = Template("BaseTpl_Vmhost")
    t.isBaseTpl=True
    t._medata["pluginSettings"] = dict(virtualMachine="VirtualMachineMap")
    t._saveObj()
    #创建数据源
    ds= CmdDataSource("Vmhost")
    ds.set("cmd", "cmd=mo.getCmd()")
    ds.set("execType","script")
    ds.set("parser","vmParser")
    
    #创建数据点
    cpu = DataPoint("CPU")
    cpu.set("type","GUAGE")
    ds.addDataPoint(cpu)

    mem = DataPoint("Mem")
    mem.set("type","GUAGE")
    ds.addDataPoint(mem)
    
    upTime = DataPoint("upTime")
    upTime.set("type","GUAGE")
    ds.addDataPoint(upTime)
    
    memSize = DataPoint("memSize")
    memSize.set("type","GUAGE")
    ds.addDataPoint(memSize)
    
    numCpu = DataPoint("numCpu")
    numCpu.set("type","GUAGE")
    ds.addDataPoint(numCpu)
    
    totalCpu = DataPoint("totalCpu")
    totalCpu.set("type","totalCpu")
    ds.addDataPoint(totalCpu)
    
    effectCpu = DataPoint("effectCpu")
    effectCpu.set("type","GUAGE")
    ds.addDataPoint(effectCpu)
    
    totalMem = DataPoint("totalMem")
    totalMem.set("type","GUAGE")
    ds.addDataPoint(totalMem)
    
    effectMem = DataPoint("effectMem")
    effectMem.set("type","GUAGE")
    ds.addDataPoint(effectMem)
    
    name = DataPoint("name")
    name.set("type","GUAGE")
    name.set("valueType","String")
    ds.addDataPoint(name)
    
    status = DataPoint("Status")
    status.set("type","GUAGE")
    status.set("valueType","String")
    ds.addDataPoint(status)
    
    port = DataPoint("port")
    port.set("type","GUAGE")
    port.set("valueType","String")
    ds.addDataPoint(port)
    
    model = DataPoint("model")
    model.set("type","GUAGE")
    model.set("valueType","String")
    ds.addDataPoint(model)
    
    cpuModel = DataPoint("cpuModel")
    cpuModel.set("type","GUAGE")
    cpuModel.set("valueType","String")
    ds.addDataPoint(cpuModel)
    
    vendor = DataPoint("vendor")
    vendor.set("type","GUAGE")
    vendor.set("valueType","String")
    ds.addDataPoint(vendor)
    
    cpuMhz = DataPoint("cpuMhz")
    cpuMhz.set("type","GUAGE")
    cpuMhz.set("valueType","String")
    ds.addDataPoint(cpuMhz)
    #添加数据源到模板
    t.addDataSource(ds)
    return t
#status,totalCpu,effectCpu,totalMem,effectMem,name,port,cpuMhz,model,vendor


def startVmvirtualTemplate():
    """
    创建vmware host模板
    """
    #创建模板
    t = Template("BaseTpl_Vmvirtual")
    t.isBaseTpl=True
    t._saveObj()
    #创建数据源
    ds= CmdDataSource("Vmvirtual")
    ds.set("cmd", "cmd=mo.getCmd()")
    ds.set("execType","script")
    ds.set("parser","vmParser")
    
    #创建数据点
    cpu = DataPoint("CPU")
    cpu.set("type","GUAGE")
    ds.addDataPoint(cpu)

    mem = DataPoint("Mem")
    mem.set("type","GUAGE")
    ds.addDataPoint(mem)
    
    uptime = DataPoint("upTime")
    uptime.set("type","GUAGE")
    uptime.set("valueType","String")
    ds.addDataPoint(uptime)
    
    memSize = DataPoint("memSize")
    memSize.set("type","GUAGE")
    ds.addDataPoint(memSize)
    
    status = DataPoint("Status")
    status.set("type","GUAGE")
    status.set("valueType","String")
    ds.addDataPoint(status)


    #添加数据源到模板
    t.addDataSource(ds)
    return t
#Status,totalDisk,Disk,Mem,guestMem,CPU,upTime,maxCpu,maxMem

if __name__=="__main__":
    startVmhostTemplate()
    startVmvirtualTemplate()
