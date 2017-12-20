#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,StatusThreshold
"""
$$$ifInErrors    1.3.6.1.4.1.14331.5.5.1.5.1.14    DERIVE
~~~ifInOctets    1.3.6.1.4.1.14331.5.5.1.5.1.12    DERIVE
@@@ifInUcastPackets    1.3.6.1.4.1.14331.5.5.1.5.1.11    DERIVE
!!!ifOperStatus    1.3.6.1.4.1.14331.5.5.1.5.1.9    GAUGE
$$$ifOutErrors    1.3.6.1.4.1.14331.5.5.1.5.1.21    DERIVE
~~~ifOutOctets    1.3.6.1.4.1.14331.5.5.1.5.1.19    DERIVE
@@@ifOutUcastPackets    1.3.6.1.4.1.14331.5.5.1.5.1.18    DERIVE

每个数据点的含义见这个包下的  __init__.py文件说明
"""
def createTopSecNG32100Interface():
    """
    创建接口模板
    """
    t = Template("TopSecNG32100Interface")
    t.isBaseTpl = True
    t._saveObj()

    ds = SnmpDataSource("Throughs")
    ds.set("execCycle", 60)
    dp0 = DataPoint("ifInOctets")
    dp0.set("oid", "1.3.6.1.4.1.14331.5.5.1.5.1.12")
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
    dp01.set("oid", "1.3.6.1.4.1.14331.5.5.1.5.1.19")
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
    dp1.set("oid", "1.3.6.1.4.1.14331.5.5.1.5.1.11")
    dp1.set("type", "DERIVE")
    dp11 = DataPoint("ifOutUcastPackets")
    dp11.set("oid", "1.3.6.1.4.1.14331.5.5.1.5.1.18")
    dp11.set("type", "DERIVE")
    
    ds1.addDataPoint(dp1)
    ds1.addDataPoint(dp11)
    t.addDataSource(ds1)
    
    #数据源错包
    ds2 = SnmpDataSource("Errors")
    ds2.set("execCycle", 60)
    dp2 = DataPoint("ifInErrors")
    dp2.set("oid", "1.3.6.1.4.1.14331.5.5.1.5.1.14")
    dp2.set("type", "DERIVE")
    dp21 = DataPoint("ifOutErrors")
    dp21.set("oid", "1.3.6.1.4.1.14331.5.5.1.5.1.21")
    dp21.set("type", "DERIVE")
    
    ds2.addDataPoint(dp2)
    ds2.addDataPoint(dp21)
    t.addDataSource(ds2)
    
    ds3 = SnmpDataSource("Status")
    ds3.set("execCycle", 60)
    dp3 = DataPoint("ifOperStatus")
    dp3.set("oid", "1.3.6.1.4.1.14331.5.5.1.5.1.9")
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

if __name__=="__main__":
    createTopSecNG32100Interface()