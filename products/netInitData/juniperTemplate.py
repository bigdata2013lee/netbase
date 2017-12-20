#coding: utf-8 
from products.netModel.templates.template import Template
from products.netModel.templates.ds import SnmpDataSource
from products.netModel.templates.dataPoint import DataPoint
from products.netModel.templates.threshold import MaxThreshold,MinThreshold,RangeThreshold
#cpu oids
cpuLastOids = dict(   
   agOid  = '1.3.6.1.4.1.3224.16.1.1.0',
   m1Oid  = '1.3.6.1.4.1.3224.16.1.2.0',
   m5Oid  = '1.3.6.1.4.1.3224.16.1.3.0',
   m15Oid = '1.3.6.1.4.1.3224.16.1.4.0'
    )
#mem oids
memOids = dict(
   memAllocateOid = '1.3.6.1.4.1.3224.16.2.1.0',
   memLeftOid     = '1.3.6.1.4.1.3224.16.2.2.0',
   memFragOid     = '1.3.6.1.4.1.3224.16.2.3.0'   
    )
#session oids
connOids = dict(
    sessAllocateOid = '1.3.6.1.4.1.3224.16.3.2.0',
    currentSession   = '1.3.6.1.4.1.3224.16.3.3.0',
    sessFailedOid   = '1.3.6.1.4.1.3224.16.3.4.0'
    )
#modtable oids
modOids = dict(
    modIdOid = '1.3.6.1.4.1.3224.16.4.1.1',
    )
#modCpu oids
modCpuOids=dict(
    modCpuIdOid = '1.3.6.1.4.1.3224.16.4.1.2',
    modCpuCurrOid = '1.3.6.1.4.1.3224.16.4.1.3',
    modCpu1MinOid = '1.3.6.1.4.1.3224.16.4.1.4',
    modCpu5MinOid = '1.3.6.1.4.1.3224.16.4.1.5',
    modCpu15MinOid= '1.3.6.1.4.1.3224.16.4.1.6'
        )
    #modMem oids
modMemOids=dict(
    modMemAllocateOid = '1.3.6.1.4.1.3224.16.4.1.7',
    modMemLeftOid = '1.3.6.1.4.1.3224.16.4.1.8'
    )
#modSession Oids
modSessOids = dict(
    modSessAllocateOid = '1.3.6.1.4.1.3224.16.4.1.9',
    modSessMaxiumOid ='1.3.6.1.4.1.3224.16.4.1.10',
    modSessFailedOid = '1.3.6.1.4.1.3224.16.4.1.11',
    )
#modThreadshold Oids
modThOids= dict(
                
    modThCpuOid = '1.3.6.1.4.1.3224.16.4.1.12',
    modThMemOid = '1.3.6.1.4.1.3224.16.4.1.13',
    modThSessOid = '1.3.6.1.4.1.3224.16.4.1.14'    
    )
#------juniper Fire Wall----------
def startCreateJuniperTemplate():
    
    t = Template('BaseTpl_JuniperFireWall')
    t.isBaseTpl = True
    t._medata["pluginSettings"] = dict(interface="InterfaceMap")
    t._saveObj() 
    #CPU
    addJuniperCpuDataSource(t)
    #内存
    addJuniperMemDataSource(t)
    #modId
    addJuniperModIdDataSource(t)
    #会话
    addJuniperSessDataSource(t)
    #modCpu
    addJuniperModCpuDataSource(t)
    #modsession
    addJuniperModSessDataSource(t)
    #modmem
    addJuniperMemDataSource(t)
    #modth
    addJuniperModThDataSource(t)
    return t
    
# --------------cpu--------
def addJuniperCpuDataSource(t,cpuLastOids=cpuLastOids):
    cds = SnmpDataSource('CPU')
    cds.set('execCycle', 60)  
     

    
    agdp = DataPoint('AvgLast')
    agdp.set('oid', cpuLastOids.get('agOid'))
    agdp.set('type', 'GUAGE')
    
    
    m1dp = DataPoint('CPU')
    m1dp.set('oid', cpuLastOids.get('m1Oid'))
    m1dp.set('type', 'GUAGE')
    
    
    m5dp = DataPoint('5MinLast')
    m5dp.set('oid', cpuLastOids.get('m5Oid'))
    m5dp.set('type', 'GUAGE')
        
    avdp = DataPoint("15MinLast")
    avdp.set('oid', cpuLastOids.get('m15Oid'))
    avdp.set("type", 'GUAGE')
   
    maxt = MaxThreshold('maxCpu')
    maxt.set('max', 50)
    maxt.set('format', '%(title)sCPU最大负载%(max)s')
    

    m1dp.addThreshold(maxt)

    

    cds.addDataPoint(agdp)
    cds.addDataPoint(m1dp)
    cds.addDataPoint(m5dp)
    cds.addDataPoint(avdp)
    
    
    t.addDataSource(cds)
    

#------创建数据通用方法
def createDataPoint(ds, dp_name, dpOid, dptype, thdValue={}, valueType=None):    
    """
    ds: 数据源
    dp_name: 数据点名字
    dpOid:  数据点oid
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
        rangt.set("format", dp_name +"%(title)s超过设定的范围阀值:%(min)s~%(max)s")
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
    
def addJuniperMemDataSource(t,memOids = memOids):
    '''
    内存数据源
    '''
    ds = SnmpDataSource('Mem')
    ds.set('execCycle', 60)
    createDataPoint(ds,'memFragOid',memOids.get('memFragOid'),'GUAGE',{})
    
    createDataPoint(ds,'MemLeft',memOids.get('memLeftOid'),'GUAGE',{})
    
    umdp = DataPoint('Mem')
    umdp.set('oid', memOids.get('memAllocateOid'))
    umdp.set('type',"RPN")
    rpn = "value=r.value*100/(r.value+r.pv('Mem','MemLeft',10000000))"
    umdp.set('rpn',rpn)
    
    rmaxt = MaxThreshold("MaxMem")
    rmaxt.set("max",80)
    rmaxt.set("format","设备%(title)s最大内存使用百分比：%(max)s")
    umdp.addThreshold(rmaxt)
    
    ds.addDataPoint(umdp)
    t.addDataSource(ds)
    
def addJuniperSessDataSource(t,sessOids=connOids):
    '''
    会话数据源
    '''
    sds = SnmpDataSource('Connections')
    sds.set('execCycle', 60)
        
    createDataPoint(sds,'SessAllocate',sessOids.get('sessAllocateOid'),'GUAGE',{})
    createDataPoint(sds,'currentSession',sessOids.get('currentSession'),'GUAGE',{})
    createDataPoint(sds,'SessFailed',sessOids.get('sessFailedOid'),'GUAGE',{})
        
    t.addDataSource(sds)
#--------ModCpu 数据源----------- 
  
def addJuniperModCpuDataSource(t,modCpuOids=modCpuOids):
    ds = SnmpDataSource('ModCpu')
    ds.set('execCycle', 60)
    
    createDataPoint(ds,'ModCpuId',modCpuOids.get('modCpuIdOid'),'GUAGE',{})
    createDataPoint(ds,'ModCpuCurr',modCpuOids.get('modCpuCurrOid'),'GUAGE',{'max':80})
    createDataPoint(ds,'ModCpu1Min',modCpuOids.get('modCpu1MinOid'),'GUAGE',{'max':80})
    createDataPoint(ds,'ModCpu5Min',modCpuOids.get('modCpu5MinOid'),'GUAGE',{'max':80})     
    createDataPoint(ds,'ModCpu15Min',modCpuOids.get('modCpu15MinOid'),'GUAGE',{'max':80})
    t.addDataSource(ds)
#------------modmemory 数据源 -------------------  
def addJuniperModMemDataSource(t,modMemOids=modMemOids):
    ds = SnmpDataSource('ModMemory')
    ds.set('execCycle', 60)

    createDataPoint(ds,'ModMemLeft',modMemOids.get('modMemLeftOid'),'GUAGE',{})
    umdp = DataPoint('ModMem')
    umdp.set('oid', modMemOids.get('modMemAllocateOid'))
    umdp.set('type', 'RPN')
    
    rpn = "value=r.value*100/(r.value+r.pv('ModMemory','MemLeft',10000000))"
    umdp.set('rpn', rpn)
    
    rmaxt = MaxThreshold("MaxMem")
    rmaxt.set("max",80)
    rmaxt.set("format","设备%(title)s内存最大使用百分比%(max)s")
    umdp.addThreshold(rmaxt)
    ds.addDataPoint(umdp)
    t.addDataSource(ds)
    
#---------------modSession 数据源------------
def addJuniperModSessDataSource(t,modSessOids=modSessOids):
    ds = SnmpDataSource('ModSession')
    ds.set('execCycle', 60)
    
    createDataPoint(ds,'ModSessAllocate',modOids.get('modSessAllocateOid'),'GUAGE',{})
    createDataPoint(ds,'ModSessMaxium',modOids.get('modSessMaxiumOid'),'GUAGE',{})
    createDataPoint(ds,'ModSessFailed',modOids.get('modSessFailedOid'),'GUAGE',{})
    
    t.addDataSource(ds)
    
#----------------modthreshold 数据源------------
def addJuniperModThDataSource(t,modThOids=modThOids):
    ds = SnmpDataSource('ModThreshold')
    ds.set('execCycle', 60)
    createDataPoint(ds,'ModThCpu',modThOids.get('modThCpuOid'),'GUAGE',{})
    createDataPoint(ds,'ModThMem',modThOids.get('modThMemOid'),'GUAGE',{})
    createDataPoint(ds,'ModThSess',modThOids.get('modThSessOid'),'GUAGE',{})
    
    t.addDataSource(ds)
     
#-----------mod数据源--------        
def addJuniperModIdDataSource(t,modOids = modOids):
    ds = SnmpDataSource('Model')
    ds.set('execCycle', 60)    
    createDataPoint(ds,'ModId',modOids.get('modIdOid'),'GUAGE',{})
    t.addDataSource(ds)
           
if __name__ == '__main__':
    startCreateJuniperTemplate()