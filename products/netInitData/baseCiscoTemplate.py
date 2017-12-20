#coding=utf-8
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold

##----------常用的思科Oid(不变的)-------------------------------------------------------------
#CPU 1分钟、5分钟，5秒钟 负载数据源
cpuLoadOids = dict(
    m1oid = ".1.3.6.1.4.1.9.2.1.57.0",
    m5oid = ".1.3.6.1.4.1.9.2.1.58.0",
    s5oid = ".1.3.6.1.4.1.9.2.1.56.0"
)


#Switch CPU USAGE
switchCpuOids = dict(
                   
    usageOid = "1.3.6.1.4.1.9.9.109.1.1.1.1.5.1"                                     
)

#内存相关Oids
memOids = dict(
    memFreeAOid = ".1.3.6.1.4.1.9.9.48.1.1.1.6.1",
    memFreeBOid = ".1.3.6.1.4.1.9.9.48.1.1.1.6.2",
    memUsedAOid = ".1.3.6.1.4.1.9.9.48.1.1.1.5.1",
    memUsedBOid = ".1.3.6.1.4.1.9.9.48.1.1.1.5.2"
)

#Switch Mem
switchMemOids = dict(
    memFreeOid = ".1.3.6.1.4.1.9.9.48.1.1.1.6.1",
    memUsedOid = ".1.3.6.1.4.1.9.9.48.1.1.1.5.1"
)

#缓存相关Oids
buffOids = dict(
    bufferFailOid = ".1.3.6.1.4.1.9.2.1.46.0",
    bufferHgCreateOid = ".1.3.6.1.4.1.9.2.1.69.0",
    bufferLgCreateOid = ".1.3.6.1.4.1.9.2.1.45.0",
    bufferBgCreateOid = ".1.3.6.1.4.1.9.2.1.37.0",
    bufferMdCreateOid = ".1.3.6.1.4.1.9.2.1.29.0", 
    bufferSmCreateOid = ".1.3.6.1.4.1.9.2.1.21.0" , 
    bufferElFreeOid = ".1.3.6.1.4.1.9.2.1.9.0",
    bufferElMaxOid = ".1.3.6.1.4.1.9.2.1.10.0",
    bufferElHitOid = ".1.3.6.1.4.1.9.2.1.11.0",
    bufferElMissOid = ".1.3.6.1.4.1.9.2.1.12.0",
    bufferElCreateOid = ".1.3.6.1.4.1.9.2.1.13.0",
    bufferNoMemOid = ".1.3.6.1.4.1.9.2.1.47.0"
)

#路由器IP路由
ipRouterOids = dict(
                    
    ipRouteNextHopOid = ".1.3.6.1.2.1.4.21.1.7",
    ipRouteMaskOid = ".1.3.6.1.2.1.4.21.1.11" 
)

#温度监测
TempStatusValueOids = dict(
                           
    tsvOid_1 = ".1.3.6.1.4.1.9.9.13.1.3.1.3.1", 
    tsvOid_2 = ".1.3.6.1.4.1.9.9.13.1.3.1.3.2",
    tsvOid_3 = ".1.3.6.1.4.1.9.9.13.1.3.1.3.3",
    tsvOid_4 = ".1.3.6.1.4.1.9.9.13.1.3.1.3.4",                           
)

#温度状态
TempStatusOids = dict(
                           
    tsOid_1 = ".1.3.6.1.4.1.9.9.13.1.3.1.6.1", 
    tsOid_2 = ".1.3.6.1.4.1.9.9.13.1.3.1.6.2",
    tsOid_3 = ".1.3.6.1.4.1.9.9.13.1.3.1.6.3",
    tsOid_4 = ".1.3.6.1.4.1.9.9.13.1.3.1.6.4",                           
)

#供电状态
SupplyStateOids = dict(
                       
    ssOid_1 = ".1.3.6.1.4.1.9.9.13.1.5.1.3.1",
    ssOid_2 = ".1.3.6.1.4.1.9.9.13.1.5.1.3.2"                                      
)

"""
tcpOids = dict(               
    tcpMaxConnOid = ".1.3.6.1.2.1.6.4.0",
    tcpInSegsOid = ".1.3.6.1.2.1.6.10.0",  
    tcpOutSegsOid = ".1.3.6.1.2.1.6.11.0",
    tcpActiveOpensOid = ".1.3.6.1.2.1.6.5.0",             
    tcpInErrsOid = ".1.3.6.1.2.1.6.14.0"     
)
"""

#fan
fanOids = dict(
    
    fan1Oid = ".1.3.6.1.4.1.9.9.13.1.4.1.3.1",
    fan2Oid = ".1.3.6.1.4.1.9.9.13.1.4.1.3.2",
    fan3Oid = ".1.3.6.1.4.1.9.9.13.1.4.1.3.3",
    fan4Oid = ".1.3.6.1.4.1.9.9.13.1.4.1.3.4",
)

#FrieWall Connection
connOids = dict(
                
    currentSession = ".1.3.6.1.4.1.9.9.392.1.3.1.0", 
    activeSession = ".1.3.6.1.4.1.9.9.491.1.1.1.6.0",
    currentSSL = ".1.3.6.1.4.1.3076.2.1.2.26.1.2.0"            
)

#FireWall IPSEC
ipsecOids = dict(
                 
    ipsecCount = ".1.3.6.1.4.1.9.9.171.1.3.1.1.0",
    ipsecInPackage = ".1.3.6.1.4.1.9.9.171.1.3.1.9.0",
    ipsecOutPackage = ".1.3.6.1.4.1.9.9.171.1.3.1.22.0",
    ipsecInStream = ".1.3.6.1.4.1.9.9.171.1.3.1.3.0",
    ipsecOutStream = ".1.3.6.1.4.1.9.9.171.1.3.1.16.0"             
)

#FireWall IKE

ikeOids = dict(
               
    ikeCount = ".1.3.6.1.4.1.9.9.171.1.2.1.1.0",
    ikeInPackage = ".1.3.6.1.4.1.9.9.171.1.2.1.12.0",
    ikeOutPackage = ".1.3.6.1.4.1.9.9.171.1.2.1.4.0",
    ikeInStream = ".1.3.6.1.4.1.9.9.171.1.2.1.3.0",
    ikeOutStream =".1.3.6.1.4.1.9.9.171.1.2.1.11.0"
               
)

#----创建模板------------------------------------------------------------------------------
def createBaseTemplate(tplName):
    t = Template(tplName)
    t.isBaseTpl = True
    t._saveObj()
    return t 


#---ipRouter----------------------------------------------------------------------------
def addIpRouterSnmpDataSource(t, ipRouterOids=ipRouterOids):
    ds = SnmpDataSource("IpRouter")
    ds.set("execCycle", 60)
    
    createDataPoint(ds, "RoutNextHop", ipRouterOids.get("ipRouteNextHopOid"), "GUAGE")
    createDataPoint(ds, "RouteMask", ipRouterOids.get("ipRouteMaskOid"), "GUAGE")
    t.addDataSource(ds)

#------TemperatureStateValue-------------------------------------------------------------
def addTempStateValueSnmpDataSource(t, TempStatusValueOids=TempStatusValueOids):
    
    ds = SnmpDataSource("TempStatusValue")
    ds.set("execCycle", 60)
    
    for k, v in TempStatusValueOids.items():
        createDataPoint(ds, k, v, "GUAGE", {max: 60})
    t.addDataSource(ds)   
        
        
#------TemperatureState------------------------------------------------------------------
def addTempStateSnmpDataSource(t, TempStatusOids=TempStatusOids):
    
    ds = SnmpDataSource("TempStatusValue")
    ds.set("execCycle", 60)
    
    for k, v in TempStatusOids.items():
        createDataPoint(ds,k, v, "GUAGE")
    t.addDataSource(ds)
    
    
#---SupplyState--------------------------------------------------------------------------------------

def addSupplyStateSnmpDataSource(t, SupplyStateOids=SupplyStateOids):
    
    ds = SnmpDataSource("SupplyState")
    ds.set("execCycle", 60)
    
    for k, v in SupplyStateOids.items():
        createDataPoint(ds, k, v, "GUAGE")
    t.addDataSource(ds)



#---获取防火墙连接数数据源----------------------------------------------------------------------
def addConnectionsSnmpDataSource(t, connOids=connOids):
    ds = SnmpDataSource("Connections")
    ds.set("execCycle", 60)
    for k, v in connOids.items():
        createDataPoint(ds, k, v , "GUAGE", {"max": 500})
    t.addDataSource(ds)
    
    
#-----添加CPU负载数据源---------------------------------------------------------------------
def addCpuLoadSnmpDataSource(t, cpuLoadOids=cpuLoadOids):
    ds = SnmpDataSource("CPU")
    ds.set("execCycle", 60)
    
    #1分钟负载数据点
    m1dp = DataPoint("1MinLoad")
    m1dp.set("oid",cpuLoadOids.get("m1oid"))
    m1dp.set("type", "GUAGE")
    
    #5分钟负载数据点
    m5dp = DataPoint("5MinLoad")
    m5dp.set("oid", cpuLoadOids.get("m5oid"))
    m5dp.set("type", "GUAGE")
    
    #5秒钟负载数据点
    s5dp = DataPoint("5SecLoad")
    s5dp.set("oid",cpuLoadOids.get("s5oid"))
    s5dp.set("type", "GUAGE")
    
    #最大负载阀值
    maxt = MaxThreshold("maxThread")
    maxt.set("max", 0.9)
    maxt.set("format", "%(title)sCPU最大负载%(max)s")
    
    #为数据点添加阀修值
    m1dp.addThreshold(maxt)
    m5dp.addThreshold(maxt)
    s5dp.addThreshold(maxt)
    
    #为数据源添加相应数据点
    ds.addDataPoint(m1dp)
    ds.addDataPoint(m5dp)
    ds.addDataPoint(s5dp)
    #为基础模板添加数据源
    t.addDataSource(ds)
    
    
#--------创建通用数据点方法--------------------------------------------------------------------------
def createDataPoint(ds, dp_name, dpOid, dptype, thdValue={}, valueType=None):    
    """
    @param ds: 数据源
    @param dp_name: 创建的数据点的名字
    @param dpOid: 数据点的OID
    @param thdValue:<{"max":maxVal | "min": minVal}> 最大阀值|最小阀值|范围阀值
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
    
#---------------------------------------------------

#------添加思科Memory数据源-----------------------------------------------------------------------    
def addMemorySnmpDataSource(t, memOids=memOids):
    ds = SnmpDataSource("Mem")
    ds.set("execCycle", 60)
    
    createDataPoint(ds, "MemFreeA", memOids.get("memFreeAOid"), "GUAGE", {})
    createDataPoint(ds, "MemFreeB", memOids.get("memFreeBOid"), "GUAGE", {})
    createDataPoint(ds, "MemUsedA", memOids.get("memUsedAOid"), "GUAGE", {})
    
    umdp = DataPoint("Mem")
    umdp.set("oid", memOids.get("memUsedBOid"))
    umdp.set("type", "RPN")
    rpn = "value=(r.value + r.pv('Mem', 'MemUsedA', 10000000))*100/float(r.pv('Mem', 'MemFreeA', 10000000)+ \
    r.pv('Mem', 'MemFreeB', 10000000)+r.pv('Mem', 'MemUsedA', 10000000) + r.value)"
    umdp.set("rpn", rpn)
    #umdp.set("rpn", "value=r.value*100/(r.value + r.pv('Mem', 'MemFree', 10000000))")
    
    rmaxt = MaxThreshold("MaxMem")
    rmaxt.set("max",80)
    rmaxt.set("format","设备%(title)s内存最大使用百分比%(max)s")
    umdp.addThreshold(rmaxt)

    ds.addDataPoint(umdp)
    t.addDataSource(ds)
    
#------添加思科路由器buffer数据源----------------------------------------------------------------------------    
def addBufferSnmpDataSource(t, buffOids=buffOids):
    rbds = SnmpDataSource("Buffer")
    rbds.set("execCycle", 60)
    createDataPoint(rbds, "BufferFail",     buffOids.get("bufferFailOid"),     "GUAGE", {"max": 50})
    createDataPoint(rbds, "BufferHgCreate", buffOids.get("bufferHgCreateOid"), "GUAGE", {"max": 60})
    createDataPoint(rbds, "BufferLgCreate", buffOids.get("bufferLgCreateOid"), "GUAGE", {"max": 30})
    createDataPoint(rbds, "BufferBgCreate", buffOids.get("bufferBgCreateOid"), "GUAGE", {"max": 30})
    createDataPoint(rbds, "BufferMdCreate", buffOids.get("bufferMdCreateOid"), "GUAGE", {"max": 30})
    createDataPoint(rbds, "BufferSmCreate", buffOids.get("bufferSmCreateOid"), "GUAGE", {"max": 30})
    createDataPoint(rbds, "BufferElFree",   buffOids.get("bufferElFreeOid"),   "GUAGE", {"max": 50})
    createDataPoint(rbds, "BufferElMax",    buffOids.get("bufferElMaxOid"),    "GUAGE", {"max": 60})
    createDataPoint(rbds, "BufferElHit",    buffOids.get("bufferElHitOid"),    "GUAGE", {"max": 30})
    createDataPoint(rbds, "BufferElMiss",   buffOids.get("bufferElMissOid"),   "GUAGE", {"max": 30})
    createDataPoint(rbds, "BufferElCreate", buffOids.get("bufferElCreateOid"), "GUAGE", {"max": 30})
    createDataPoint(rbds, "BufferNoMem",    buffOids.get("bufferNoMemOid"),    "GUAGE", {"max": 30})
    t.addDataSource(rbds)

    
#----检测温度数据源------------------------------------------------------------------------------------------------
def addTemperatureSnmpDataSource(t, temperatureOids):
    ds = SnmpDataSource("Temperature")
    ds.set("execCycle", 60)
    createDataPoint(ds, "TemperatureStatus", temperatureOids.get("temperatureStatus"), "GUAGE", {"max": 50})
    createDataPoint(ds, "TemperatureValue1", temperatureOids.get("temperatureValue1"), "GUAGE", {"max": 50})
    createDataPoint(ds, "TemperatureValue2", temperatureOids.get("temperatureValue2"), "GUAGE", {"max": 50})
    createDataPoint(ds, "TemperatureValue3", temperatureOids.get("temperatureValue3"), "GUAGE", {"max": 50})
    createDataPoint(ds, "TemperatureValue4", temperatureOids.get("temperatureValue4"), "GUAGE", {"max": 50})
    createDataPoint(ds, "TemperatureValue5", temperatureOids.get("temperatureValue5"), "GUAGE", {"max": 50})
    t.addDataSource(ds)
    
    
#------检测CPU风扇状态---------------------------------------------------------------------------------------------------    
def addFanSnmpDataSource(t,fanOids=fanOids):
    ds = SnmpDataSource("Temperature")
    ds.set("execCycle", 60)
    for k ,v in fanOids.items():
        createDataPoint(ds, k, v, "GUAGE", {"max": 50})
    t.addDataSource(ds)
    

#====思科交换机CPU =================================================================
def addSwitchCpuSnmpDataSource(t, switchCpuOids=switchCpuOids):
    ds = SnmpDataSource("SwitchCPU")
    ds.set("execCycle", 60)
    for k, v in switchCpuOids.items():
        createDataPoint(ds, k, v, "GUAGE", {max: 0.7})
    t.addDataSource(ds)
    
#====思科交换机Memory 数据源===============================================================
def addSwitchMemorySnmpDataSource(t, switchMemOids=switchMemOids):
    ds = SnmpDataSource("Memory")
    ds.set("execCycle", 60)
    
    createDataPoint(ds, "MemFree", switchMemOids.get("memFreeOid"), "GUAGE", {})
    
    umdp = DataPoint("Mem")
    umdp.set("oid", switchMemOids.get("memUsedOid"))
    umdp.set("type", "RPN")

    umdp.set("rpn", "value=r.value*100/(r.value + r.pv('Mem', 'MemFree', 10000000))")
    
    rmaxt = MaxThreshold("MaxMem")
    rmaxt.set("max",80)
    rmaxt.set("format","设备%(title)s内存最大使用百分比%(max)s")
    umdp.addThreshold(rmaxt)
    ds.addDataPoint(umdp)
    t.addDataSource(ds)

#=================================================================
#-------------------FireWall Method------------------------------#
#=================================================================

def addIPSECSnmpDataSource(t, ipsecOids=ipsecOids):
    
    ds = SnmpDataSource("IPSEC")
    ds.set("execCycle", 60)
    for k, v in ipsecOids.items():
        createDataPoint(ds, k, v, "GUAGE", {})
    t.addDataSource(ds)
    
    
def addIKESnmpDataSource(t, ikeOids=ikeOids):

    ds = SnmpDataSource("IKE")
    ds.set("execCycle", 60)
    for k, v in ikeOids.items():
        createDataPoint(ds, k, v, "GUAGE", {})
    t.addDataSource(ds)
    
    

if __name__ == "__main__":
    pass