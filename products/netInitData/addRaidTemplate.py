#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import CmdDataSource
from products.netModel.templates.dataPoint import DataPoint

def startCreatRaidTemplate():
    """
        创建Linux raid SSH模板
    """
    #创建模板
    t = Template("ExtendTpl_SshRaidLinux")
    t.isBaseTpl = False
    t.tplType = "extend"
    t.title = "监控Linux系统Raid信息"
    t._saveObj()
    
    #ssh命令所有信息数据源
    dsaif= CmdDataSource("raid")
    dsaif.set("cmd", "cmd='/opt/netbase4/libexec/raid.sh'")
    dsaif.set("execType","ssh")
    dsaif.set("parser","adpAllInfo")
    #解析productName下的地址数据点
    dppdn = DataPoint("productName")
    dppdn.set("type","GUAGE")
    dppdn.set("valueType","String")
    #解析SerialNo下的包数据点
    dpsn = DataPoint("serialNo")
    dpsn.set("type","GUAGE")
    dpsn.set("valueType","String")
    #解析memorySize下的包数据点
    dpmsz = DataPoint("memorySize")
    dpmsz.set("type","GUAGE")
    dpmsz.set("valueType","String")
    
    #解析vds onLineDisk下的包数据点
    dpvold = DataPoint("vdsOnLineDisk")
    dpvold.set("type","GUAGE")
    dpvold.set("valueType","Num")
    #解析vds RebuildDisk下的包数据点
    dpvrd = DataPoint("vdsRebuildDisk")
    dpvrd.set("type","GUAGE")
    dpvrd.set("valueType","Num")
    
    #解析vds CriticalDisks下的包数据点
    dpvcd = DataPoint("vdsCriticalDisks")
    dpvcd.set("type","GUAGE")
    dpvcd.set("valueType","Num")
    
    #解析pds Disks下的包数据点
    dppds = DataPoint("pdsDisks")
    dppds.set("type","GUAGE")
    dppds.set("valueType","Num")
    
    #解析pds Critical Disks下的包数据点
    dppcd = DataPoint("pdsCriticalDisks")
    dppcd.set("type","GUAGE")
    dppcd.set("valueType","Num")
    
    #解析pds Failed Disk下的包数据点
    dppfd = DataPoint("pdsFailedDisks")
    dppfd.set("type","GUAGE")
    dppfd.set("valueType","Num")
    
    #添加数据点到数据源
    dsaif.addDataPoint(dppdn)
    dsaif.addDataPoint(dpsn)
    dsaif.addDataPoint(dpmsz)
    dsaif.addDataPoint(dpvold)
    dsaif.addDataPoint(dpvrd)
    dsaif.addDataPoint(dpvcd)
    dsaif.addDataPoint(dppds)
    dsaif.addDataPoint(dppcd)
    dsaif.addDataPoint(dppfd)
    t.addDataSource(dsaif)
    
    return t

if __name__ == "__main__":
    startCreatRaidTemplate()
    
    

