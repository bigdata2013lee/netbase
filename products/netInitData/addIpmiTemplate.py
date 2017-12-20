#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import CmdDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold
    
def startCreatIpmiTemplate():
    """
    创建命令行模板
    """
    #创建模板
    t = Template("ExtendTpl_IpmiLinux")
    t.isBaseTpl = False
    t.tplType = "extend"
    t.title = "Ipmi监控机箱温度与风扇运行状况(限于Linux系统)"
    t._saveObj()
    
    #ssh命令ipmi temp and fan数据源
    dsitp= CmdDataSource("ipmiTempAndFan")
    dsitp.set("cmd", "cmd='/opt/netbase4/libexec/ipmitf.sh'")
    dsitp.set("execType","ssh")
    dsitp.set("parser","tempAndFan")
    #解析Ambient Temp下的地址数据点
    dpabt = DataPoint("ambientTemp")
    dpabt.set("type","GUAGE")
    dpabt.set("valueType","Num")
    #机箱温度阀值
    maxt=MaxThreshold("maxTemp")
    maxt.set("max", 35)
    maxt.set("zname", "最高机箱温度")
    maxt.set("description","机箱的最高温度")
    maxt.set("format","设备%(title)s机箱温度最大值为%(max)s")
    dpabt.addThreshold(maxt)
    
    #解析ok Fan下的地址数据点
    dpokf = DataPoint("okFan")
    dpokf.set("type","GUAGE")
    dpokf.set("valueType","Num")
    #解析fail fan下的地址数据点
    dpffn = DataPoint("failFan")
    dpffn.set("type","GUAGE")
    dpffn.set("valueType","Num")
    #添加数据点到数据源
    dsitp.addDataPoint(dpabt)
    dsitp.addDataPoint(dpokf)
    dsitp.addDataPoint(dpffn)
    #添加数据源到模板
    t.addDataSource(dsitp)

    return t

if __name__ == "__main__":
        
    startCreatIpmiTemplate()
    
    

